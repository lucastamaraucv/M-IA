// Arnés headless (sin navegador) para verificar el criterio de aprobación del
// Reto de código en Modo Maestro (probarReto()) contra el servidor Flask
// REAL. Técnica documentada en la memoria del proyecto: vm.createContext +
// stub mínimo de document/CodeMirror + fetch real.
// Ver memoria "feedback-headless-verification-harness" para el porqué de
// cada truco (en particular: las variables `let`/`const` de nivel superior
// del script NO quedan como propiedades del sandbox — hay que leer/escribir
// su estado siempre vía vm.runInContext, nunca sandbox.nombre).
//
// Criterio vigente (desde 2026-07-31): el Reto aprueba si el código corre
// sin errores — YA NO se exige que la salida impresa coincida con una
// referencia capturada. _masterRefOutput y _outputDiff se eliminaron.
//
// Uso: arrancar python_visualizer_flask.py en un puerto de prueba (para no
// pisar una sesión real en :5000), luego:
//   BASE_URL=http://127.0.0.1:5099 node verify/master_mode_diff_harness.js

const fs = require('fs');
const vm = require('vm');
const path = require('path');

process.on('unhandledRejection', e => console.error('[unhandledRejection]', e));
process.on('uncaughtException', e => console.error('[uncaughtException]', e));

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5099';
const SRC = fs.readFileSync(path.join(__dirname, '..', 'python_visualizer_flask.py'), 'utf8');
const scriptMatch = SRC.match(/<script>\r?\n([\s\S]*?)\r?\n<\/script>/);
if (!scriptMatch) { console.error('No se encontró el bloque <script> inline.'); process.exit(1); }
// El script real dispara `setTimeout(runCode, 400)` al cargar (auto-run del
// ejemplo inicial de la vista principal). El servidor Flask de dev es de un
// solo hilo, así que esa petición compite por el mismo turno que las
// llamadas a /prepare que hace este arnés — se anula porque es ruido ajeno
// a lo que se está probando aquí (el Reto de código de Modo Maestro).
const clientCode = scriptMatch[1].replace(
  'setTimeout(runCode, 400);',
  '/* auto-run inicial deshabilitado por el arnés de verificación */'
);
if (!clientCode.includes('/* auto-run inicial deshabilitado')) {
  console.error('Aviso: no se encontró la línea del auto-run a anular (¿cambió el código fuente?).');
}

function fakeElement(id) {
  const target = {
    id, value: '', textContent: '', innerHTML: '', className: '',
    disabled: false, style: {},
    classList: { add() {}, remove() {}, contains() { return false; }, toggle() {} },
  };
  return new Proxy(target, {
    get(t, prop) {
      if (prop in t) return t[prop];
      if (prop === 'querySelectorAll' || prop === 'getElementsByClassName' || prop === 'getElementsByTagName')
        return () => [];
      if (prop === 'querySelector') return () => null;
      return () => {}; // cualquier otro método desconocido: no-op seguro
    },
    set(t, prop, val) { t[prop] = val; return true; },
  });
}
const elCache = new Map();
const document = {
  getElementById(id) {
    if (!elCache.has(id)) elCache.set(id, fakeElement(id));
    return elCache.get(id);
  },
  addEventListener() {},
  createElement() { return fakeElement('__anon__'); },
  querySelector() { return fakeElement('__anon__'); },
  querySelectorAll() { return []; },
  getElementsByClassName() { return []; },
  getElementsByTagName() { return []; },
};

let lsStore = {};
const localStorage = {
  getItem: k => (k in lsStore ? lsStore[k] : null),
  setItem: (k, v) => { lsStore[k] = String(v); },
  removeItem: k => { delete lsStore[k]; },
};

// Stub mínimo de CodeMirror: solo lo que _cmEnsure()/openChallenge() usan.
function makeCodeMirror() {
  function Editor(initialValue) {
    let val = initialValue || '';
    return {
      getValue: () => val,
      setValue: v => { val = v; },
      setOption() {}, refresh() {}, somethingSelected: () => false,
      indentSelection() {}, replaceSelection() {},
      getCursor: () => ({ line: 0, ch: 0 }),
      getTokenAt: () => ({ string: '', start: 0 }),
      getRange: () => '',
    };
  }
  return {
    fromTextArea(textarea, _opts) { return Editor(textarea && textarea.value); },
    registerHelper() {},
    hint: { anyword: () => ({ list: [] }) },
    Pos: (line, ch) => ({ line, ch }),
  };
}

const sandbox = {
  document, window: { addEventListener() {} }, localStorage,
  CodeMirror: makeCodeMirror(),
  console,
  fetch: (url, opts) => {
    const full = /^https?:\/\//.test(url) ? url : BASE_URL + url;
    if (process.env.DEBUG_HARNESS) console.error('[fetch]', full);
    return fetch(full, opts); // fetch global real de Node (>=18)
  },
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);
vm.runInContext(clientCode, sandbox, { filename: 'inline-script.js' });

const results = [];
function record(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : ''));
}

function setChallengeState(idx) {
  vm.runInContext(`
    _masterPos = ${idx};
    _masterChallenge[${idx}] = {challengeable:true, mode:'blank', prompt:'', stub:''};
    _masterDrafts[${idx}] = undefined;
  `, sandbox);
}

function setDraftCode(code) {
  vm.runInContext(`_cmEnsure().setValue(${JSON.stringify(code)});`, sandbox);
}

/* Pide /prepare para un código real, carga `explains` (global del script,
   normalmente poblada por runCode()) y deriva _masterHints[idx] con la
   función real _masterDeriveHint() — así las pruebas de pistaReto() usan
   datos reales del narrador AST, no un mock. */
async function primeHintsForTopic(idx, code) {
  const resp = await fetch(BASE_URL + '/prepare', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code }),
  });
  const d = await resp.json();
  vm.runInContext(`explains = ${JSON.stringify(d.explains || {})};`, sandbox);
  vm.runInContext(`_masterHints[${idx}] = _masterDeriveHint();`, sandbox);
  vm.runInContext(`_masterHintsRevealed[${idx}] = 0;`, sandbox);
  vm.runInContext(`_masterPos = ${idx};`, sandbox);
  return vm.runInContext(`_masterHints[${idx}].length`, sandbox);
}

function waitForStatusSettled(timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  return new Promise((resolve, reject) => {
    (function poll() {
      const txt = vm.runInContext(`document.getElementById('challengeStatus').textContent`, sandbox);
      if (txt && txt !== '⏳ Probando tu código…') return resolve();
      if (Date.now() > deadline) return reject(new Error('timeout esperando resultado de probarReto()'));
      setTimeout(poll, 50);
    })();
  });
}

async function runProbarRetoCase(idx) {
  vm.runInContext(`probarReto()`, sandbox);
  await waitForStatusSettled(8000);
  return {
    statusText: vm.runInContext(`document.getElementById('challengeStatus').textContent`, sandbox),
    statusClass: vm.runInContext(`document.getElementById('challengeStatus').className`, sandbox),
    diffText: vm.runInContext(`document.getElementById('challengeDiff').textContent`, sandbox),
    diffDisplay: vm.runInContext(`document.getElementById('challengeDiff').style.display`, sandbox),
  };
}

async function main() {
  // H1: código que corre sin error -> aprueba.
  setChallengeState(0);
  setDraftCode("print(0)\nprint(1)\nprint(2)\n");
  let r = await runProbarRetoCase(0);
  record('H1 código que corre sin error -> aprueba',
    r.statusClass.includes('ok') && r.statusText.includes('¡Correcto!') && r.diffDisplay !== 'block',
    JSON.stringify(r));

  // H2: corre sin error pero con salida DISTINTA a cualquier referencia ->
  // también aprueba, porque ya no se compara la salida.
  setChallengeState(1);
  setDraftCode("print(0)\nprint(9)\nprint(2)\n");
  r = await runProbarRetoCase(1);
  record('H2 salida distinta pero sin error -> igual aprueba (ya no se compara output)',
    r.statusClass.includes('ok') && r.statusText.includes('¡Correcto!'),
    JSON.stringify(r));

  // H3: imprime menos que un hipotético ejemplo de referencia -> sigue
  // aprobando, mismo motivo que H2.
  setChallengeState(2);
  setDraftCode("print(0)\nprint(1)\n");
  r = await runProbarRetoCase(2);
  record('H3 imprime "de menos" pero sin error -> igual aprueba',
    r.statusClass.includes('ok'),
    JSON.stringify(r));

  // H4: NameError real del alumno -> falla, con hint mencionando la variable.
  setChallengeState(3);
  setDraftCode("print(0)\nprint(variable_que_no_existe)\n");
  r = await runProbarRetoCase(3);
  record('H4 NameError -> falla y muestra hint mencionando la variable exacta',
    r.statusClass.includes('fail') && r.statusText.includes('NameError') &&
    r.diffDisplay === 'block' && r.diffText.includes('variable_que_no_existe'),
    JSON.stringify(r));

  // H7: IndexError -> hint menciona "lista" (sin IA).
  setChallengeState(5);
  setDraftCode("lista=[1,2,3]\nprint(lista[10])\n");
  r = await runProbarRetoCase(5);
  record('H7 IndexError -> hint menciona la lista',
    r.statusClass.includes('fail') && r.diffDisplay === 'block' && r.diffText.toLowerCase().includes('lista'),
    JSON.stringify(r));

  // H8: TypeError (str + int) -> hint menciona los dos tipos involucrados.
  setChallengeState(6);
  setDraftCode('print("a" + 1)\n');
  r = await runProbarRetoCase(6);
  record('H8 TypeError -> hint menciona los tipos incompatibles',
    r.statusClass.includes('fail') && r.diffDisplay === 'block' && r.diffText.includes('str') && r.diffText.includes('int'),
    JSON.stringify(r));

  // H9: excepción NO cubierta por las reglas (OverflowError) -> sin hint, sin regresión.
  setChallengeState(7);
  setDraftCode("import math\nprint(math.exp(1000))\n");
  r = await runProbarRetoCase(7);
  record('H9 excepción no cubierta -> falla pero no muestra el bloque de hint',
    r.statusClass.includes('fail') && r.statusText.includes('OverflowError') && r.diffDisplay !== 'block',
    JSON.stringify(r));

  // H10: AssertionError con mensaje personalizado -> falla, el hint repite el mensaje.
  setChallengeState(8);
  setDraftCode('x = 3\nassert x == 5, "x deberia ser 5"\n');
  r = await runProbarRetoCase(8);
  record('H10 AssertionError con mensaje -> falla y el hint lo repite',
    r.statusClass.includes('fail') && r.diffDisplay === 'block' && r.diffText.includes('x deberia ser 5'),
    JSON.stringify(r));

  // H10b: AssertionError que SÍ se cumple -> aprueba (mismo criterio: sin error).
  setChallengeState(8);
  setDraftCode('x = 5\nassert x == 5, "x deberia ser 5"\n');
  r = await runProbarRetoCase(8);
  record('H10b assert que se cumple -> aprueba',
    r.statusClass.includes('ok'),
    JSON.stringify(r));

  // H11-H14: pistas progresivas ancladas a línea (sin relación con el criterio de aprobación).
  const hintTopic = 9;
  vm.runInContext(`EX[${hintTopic}] = EX[${hintTopic}] || {name:'test', code:'x=1'}`, sandbox);
  setChallengeState(hintTopic);
  const nHints = await primeHintsForTopic(hintTopic,
    "x = 5\ny = 10\nif x < y:\n    z = x + y\nelse:\n    z = x - y\nfor i in range(z):\n    pass\n");
  if (nHints < 2) {
    record('H11-H14 precondición: el ejemplo produce al menos 2 pistas', false, 'nHints=' + nHints);
  } else {
    vm.runInContext(`pistaReto()`, sandbox);
    let hintText = vm.runInContext(`document.getElementById('challengeHint').textContent`, sandbox);
    let btnText = vm.runInContext(`document.getElementById('cBtnPista').textContent`, sandbox);
    let lines1 = hintText.split('\n').filter(Boolean);
    record('H11 primer clic -> revela exactamente 1 pista con "Línea N:"',
      lines1.length === 1 && /^Línea \d+:/.test(lines1[0]) && btnText.includes(`1/${nHints}`),
      JSON.stringify({ hintText, btnText }));

    vm.runInContext(`pistaReto()`, sandbox);
    hintText = vm.runInContext(`document.getElementById('challengeHint').textContent`, sandbox);
    btnText = vm.runInContext(`document.getElementById('cBtnPista').textContent`, sandbox);
    const lines2 = hintText.split('\n').filter(Boolean);
    record('H12 segundo clic -> ahora 2 pistas, la primera se conserva',
      lines2.length === 2 && lines2[0] === lines1[0] && btnText.includes(`2/${nHints}`),
      JSON.stringify({ hintText, btnText }));

    for (let i = 0; i < nHints + 2; i++) vm.runInContext(`pistaReto()`, sandbox); // agotar + clics de más
    hintText = vm.runInContext(`document.getElementById('challengeHint').textContent`, sandbox);
    btnText = vm.runInContext(`document.getElementById('cBtnPista').textContent`, sandbox);
    const btnDisabled = vm.runInContext(`document.getElementById('cBtnPista').disabled`, sandbox);
    const linesAll = hintText.split('\n').filter(Boolean);
    record('H13 agotar todas las pistas -> no crece más allá de N, botón deshabilitado',
      linesAll.length === nHints && btnText.includes(`${nHints}/${nHints}`) && btnDisabled === true,
      JSON.stringify({ hintText, btnText, btnDisabled }));

    // H14: reabrir a mitad de camino conserva el progreso (2 de N reveladas).
    vm.runInContext(`_masterHintsRevealed[${hintTopic}] = 2;`, sandbox);
    vm.runInContext(`openChallenge()`, sandbox);
    hintText = vm.runInContext(`document.getElementById('challengeHint').textContent`, sandbox);
    btnText = vm.runInContext(`document.getElementById('cBtnPista').textContent`, sandbox);
    const linesReopen = hintText.split('\n').filter(Boolean);
    record('H14 reabrir el modal con 2/N reveladas -> las conserva, no arranca de 0',
      linesReopen.length === 2 && btnText.includes(`2/${nHints}`),
      JSON.stringify({ hintText, btnText }));
  }

  // H6: reabrir el Reto tras un fallo con hint visible -> el bloque se oculta de nuevo.
  vm.runInContext(`EX[1] = EX[1] || {name:'test', code:'print(1)'}`, sandbox); // por si el índice 1 no existiera
  setChallengeState(1);
  setDraftCode("print(0)\nprint(variable_que_no_existe)\n");
  await runProbarRetoCase(1); // deja el hint de error visible
  vm.runInContext(`openChallenge()`, sandbox);
  const diffDisplayAfterReopen = vm.runInContext(`document.getElementById('challengeDiff').style.display`, sandbox);
  record('H6 reabrir el modal oculta un hint de error viejo', diffDisplayAfterReopen === 'none',
    'display=' + diffDisplayAfterReopen);

  const failed = results.filter(r => !r.ok);
  console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS HIPÓTESIS OK'));
  process.exit(failed.length ? 1 : 0);
}

main().catch(e => { console.error('ERROR en el arnés:', e); process.exit(1); });
