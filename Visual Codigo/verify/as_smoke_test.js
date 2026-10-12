// Arnés headless para el Modo Maestro AS: carga los archivos JS reales del
// cliente (core.js..review.js) con un stub minimo de document/localStorage,
// contra el servidor Flask REAL (para runCode()->/prepare), y recorre los
// 21 temas de EX_AS ejecutando su código, comprobando el quiz (respuesta
// correcta según su `correct`) y avanzando con asNext().
// Uso: BASE_URL=http://127.0.0.1:5099 node verify/as_smoke_test.js

const fs = require('fs');
const vm = require('vm');
const path = require('path');

process.on('unhandledRejection', e => { console.error('[unhandledRejection]', e); process.exitCode = 1; });
process.on('uncaughtException', e => { console.error('[uncaughtException]', e); process.exitCode = 1; });

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5099';
const JS_DIR = path.join(__dirname, '..', 'static', 'js');

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
      if (prop === 'appendChild' || prop === 'removeChild' || prop === 'focus' || prop === 'select') return () => {};
      return () => {};
    },
    set(t, prop, val) { t[prop] = val; return true; },
  });
}
const elCache = new Map();
const document = {
  getElementById(id) { if (!elCache.has(id)) elCache.set(id, fakeElement(id)); return elCache.get(id); },
  addEventListener() {}, createElement() { return fakeElement('__anon__'); },
  querySelector() { return fakeElement('__anon__'); }, querySelectorAll() { return []; },
  getElementsByClassName() { return []; }, getElementsByTagName() { return []; },
  body: fakeElement('body'),
};
let lsStore = {};
const localStorage = {
  getItem: k => (k in lsStore ? lsStore[k] : null),
  setItem: (k, v) => { lsStore[k] = String(v); },
  removeItem: k => { delete lsStore[k]; },
};
function makeCodeMirror() {
  function Editor(initialValue) {
    let val = initialValue || '';
    return {
      getValue: () => val, setValue: v => { val = v; }, setOption() {}, refresh() {},
      somethingSelected: () => false, indentSelection() {}, replaceSelection() {},
      getCursor: () => ({ line: 0, ch: 0 }), getTokenAt: () => ({ string: '', start: 0 }), getRange: () => '',
    };
  }
  return { fromTextArea(ta, _o) { return Editor(ta && ta.value); }, registerHelper() {}, hint: { anyword: () => ({ list: [] }) }, Pos: (l, c) => ({ line: l, ch: c }) };
}
const sandbox = {
  document, window: { addEventListener() {} }, localStorage, CodeMirror: makeCodeMirror(), console,
  navigator: { clipboard: null },
  fetch: (url, opts) => {
    const full = /^https?:\/\//.test(url) ? url : BASE_URL + url;
    return fetch(full, opts);
  },
  setTimeout, clearTimeout, setInterval, clearInterval, alert() {}, confirm: () => true,
};
vm.createContext(sandbox);

const files = ['core.js', 'viz-render.js', 'code-annotate.js', 'master-py.js', 'master-ao.js', 'master-math.js', 'master-ra.js', 'master-as.js', 'review.js'];
for (const f of files) {
  const src = fs.readFileSync(path.join(JS_DIR, f), 'utf8');
  vm.runInContext(src, sandbox, { filename: f });
}

const results = [];
function record(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log((ok ? 'OK  ' : 'FAIL') + ' — ' + name + (detail ? '\n     ' + detail : ''));
}

function waitFor(fn, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  return new Promise((resolve, reject) => {
    (function poll() {
      if (fn()) return resolve();
      if (Date.now() > deadline) return reject(new Error('timeout'));
      setTimeout(poll, 30);
    })();
  });
}

async function runCodeAndWait() {
  vm.runInContext(`runCode()`, sandbox);
  await waitFor(() => vm.runInContext(`steps && steps.length > 0`, sandbox), 8000);
}

async function main() {
  const nTopics = vm.runInContext(`EX_AS.length`, sandbox);
  const nQuiz = vm.runInContext(`AS_QUIZ.length`, sandbox);
  record('EX_AS y AS_QUIZ tienen la misma longitud', nTopics === nQuiz, `EX_AS=${nTopics} AS_QUIZ=${nQuiz}`);

  vm.runInContext(`toggleMasterAs()`, sandbox);
  const onAfterToggle = vm.runInContext(`_asOn`, sandbox);
  record('toggleMasterAs() activa _asOn', onAfterToggle === true);

  for (let i = 0; i < nTopics; i++) {
    vm.runInContext(`_asGoTo(${i})`, sandbox);
    try {
      await runCodeAndWait();
    } catch (e) {
      record(`Tema ${i}: runCode() completa (via /prepare real)`, false, String(e));
      continue;
    }
    const lastErr = vm.runInContext(`_lastRunError`, sandbox);
    const nSteps = vm.runInContext(`steps.length`, sandbox);
    record(`Tema ${i}: código ejecuta sin error de Python`, !lastErr, lastErr ? JSON.stringify(lastErr) : `steps=${nSteps}`);

    // Responder el quiz con la respuesta CORRECTA real (q.correct) y comprobar que el
    // mecanismo de feedback marca "Correcto".
    const q = vm.runInContext(`_asCurrentQuiz`, sandbox); // pregunta YA elegida por _asRenderQuiz (banco de varias por tema)
    if (q.type === 'mc') {
      const shuffledCorrect = vm.runInContext(`_asQuizShuffledCorrect`, sandbox);
      vm.runInContext(`_asCheckQuizAnswer(${shuffledCorrect})`, sandbox);
    } else {
      vm.runInContext(`document.getElementById('asQuizNumericInput').value = ${JSON.stringify(String(q.correct))};`, sandbox);
      vm.runInContext(`_asCheckQuizAnswer()`, sandbox);
    }
    const answered = vm.runInContext(`_asQuizAnswered`, sandbox);
    const fbText = vm.runInContext(`document.getElementById('asQuizFeedback').textContent`, sandbox);
    record(`Tema ${i}: quiz acepta la respuesta correcta real`, answered === true && fbText.includes('Correcto'),
      `type=${q.type} correct=${q.correct} fb="${fbText}"`);

    vm.runInContext(`asNext()`, sandbox);
  }

  const doneCount = vm.runInContext(`_asDone.size`, sandbox);
  record('Tras recorrer los 21 temas, _asDone tiene 21 entradas', doneCount === nTopics, `_asDone.size=${doneCount}`);

  vm.runInContext(`exitMasterAs()`, sandbox);
  record('exitMasterAs() desactiva _asOn', vm.runInContext(`_asOn`, sandbox) === false);

  const failed = results.filter(r => !r.ok);
  console.log('\n' + (failed.length ? failed.length + ' FALLA(S)' : 'TODAS LAS ' + results.length + ' COMPROBACIONES OK'));
  process.exit(failed.length ? 1 : 0);
}

main().catch(e => { console.error('ERROR en el arnés:', e); process.exit(1); });
