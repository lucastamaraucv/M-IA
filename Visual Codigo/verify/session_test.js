// Arnés headless para la Sesión guiada de 60' (static/js/session.js, ver
// conversación 2026-08-13) — simula el avance de fases sin esperar minutos
// reales (se fuerza _sessionPhaseEndAt al pasado y se llama _sessionTick()
// directamente). Mismo patrón vm.runInContext que confidence_dontknow_test.js:
// let/const de nivel superior son bindings léxicos, no propiedades del
// sandbox -- todo se lee/llama con vm.runInContext('expr', sandbox), nunca
// sandbox.propiedad directo.
// Uso: node verify/session_test.js

const fs = require('fs');
const vm = require('vm');
const path = require('path');

let failures = 0;
function check(cond, label) {
  if (cond) { console.log('OK   ' + label); }
  else { console.error('FAIL ' + label); failures++; }
}
const V = (expr) => vm.runInContext(expr, sandbox);

function fakeElement(id) {
  const target = { id, value: '', textContent: '', innerHTML: '', style: {} };
  return new Proxy(target, {
    get(t, prop) { if (prop in t) return t[prop]; return () => {}; },
    set(t, prop, val) { t[prop] = val; return true; },
  });
}
const elCache = new Map();
const document = {
  getElementById(id) { if (!elCache.has(id)) elCache.set(id, fakeElement(id)); return elCache.get(id); },
};

const intervals = {};
let nextIntervalId = 1;
const fakeSetInterval = (fn) => { const id = nextIntervalId++; intervals[id] = fn; return id; };
const fakeClearInterval = (id) => { delete intervals[id]; };

const fetchCalls = [];
const fetch = (url, opts) => { fetchCalls.push({ url, opts }); return Promise.resolve({ json: () => Promise.resolve({ ok: true }) }); };

const calls = [];
const sandbox = {
  document, fetch,
  setInterval: fakeSetInterval, clearInterval: fakeClearInterval,
  console,
  autoLayout: () => {},
  toggleMasterAo: () => calls.push('toggleMasterAo'),
  toggleMasterRa: () => calls.push('toggleMasterRa'),
  toggleMasterAs: () => calls.push('toggleMasterAs'),
  toggleReviewMode: () => calls.push('toggleReviewMode'),
};
sandbox.window = sandbox;
vm.createContext(sandbox);

const src = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', 'session.js'), 'utf8');
vm.runInContext(src, sandbox, { filename: 'session.js' });

// 1) Estado inicial
check(V('_sessionActive') === false, 'estado inicial: _sessionActive=false');
check(V('SESSION_PHASES.length') === 5, 'SESSION_PHASES tiene 5 fases');
check(V('SESSION_PHASES.reduce((s,p)=>s+p.mins,0)') === 60, 'las 5 fases suman 60 minutos exactos');
check(V('JSON.stringify(SESSION_PHASES.map(p=>p.mins))') === JSON.stringify([10, 15, 20, 7, 8]),
  'reparto exacto 10/15/20/7/8 (no un Pomodoro genérico)');

// 2) Empezar sesión con AO
V(`_sessionStart('ao')`);
check(V('_sessionActive') === true, 'tras _sessionStart: _sessionActive=true');
check(V('_sessionCourse') === 'ao', 'tras _sessionStart: curso guardado (ao)');
check(V('_sessionPhaseIdx') === 0, 'tras _sessionStart: arranca en fase 0 (Recuperación)');

// 3) Forzar que la fase 0 ya venció y tickear -- debe avanzar a fase 1 (Teoría)
V('_sessionPhaseEndAt = Date.now() - 1000');
V('_sessionTick()');
check(V('_sessionPhaseIdx') === 1, 'al vencer la fase 0, avanza sola a fase 1 (Teoría)');
check(V('_sessionActive') === true, 'sigue activa tras avanzar de fase (no termina hasta la última)');

// 4) Saltar manualmente el resto de fases hasta el final
V('_sessionSkipPhase()'); // -> fase 2 (Práctica)
check(V('_sessionPhaseIdx') === 2, '_sessionSkipPhase avanza a fase 2 (Práctica)');
V('_sessionSkipPhase()'); // -> fase 3 (Explicación)
V('_sessionSkipPhase()'); // -> fase 4 (Reflexión)
check(V('_sessionPhaseIdx') === 4, 'tras 3 saltos desde fase 1, llega a fase 4 (Reflexión, la última)');
check(V('_sessionActive') === true, 'todavía activa en la última fase');

// 5) Saltar la última fase -> debe FINALIZAR
V('_sessionSkipPhase()');
check(V('_sessionActive') === false, 'al saltar la última fase, la sesión termina (_sessionActive=false)');
check(V('_sessionJustFinished') === true, '_sessionJustFinished queda marcado tras completar las 5 fases');

// 6) Navegación: los botones de fase deben llamar al panel real correcto
calls.length = 0;
V(`_sessionStart('ra')`);
V('_sessionOpenCourse()');
check(calls.includes('toggleMasterRa'), '_sessionOpenCourse con curso=ra llama a toggleMasterRa');
check(V('_sessionOn') === false, '_sessionOpenCourse cierra el panel de la sesión (_sessionOn=false)');
check(V('_sessionActive') === true, 'el cronómetro sigue activo aunque el panel se haya cerrado');
V('_sessionOpenReview()');
check(calls.includes('toggleReviewMode'), '_sessionOpenReview llama a toggleReviewMode');

// 7) Terminar manualmente antes de tiempo -- no debe quedar marcada como completada
V('_sessionStop()');
check(V('_sessionActive') === false, '_sessionStop: _sessionActive=false');
check(V('_sessionJustFinished') === false, "_sessionStop: NO se marca como completada (se cortó antes)");
check(V('_sessionCourse') === null, '_sessionStop: curso reseteado');
check(V('_sessionPhaseIdx') === 0, '_sessionStop: fase reseteada a 0');

// 8) Reflexión: guardar sin texto no debe llamar a fetch; con texto sí, con kind:'reflection'
fetchCalls.length = 0;
V(`_sessionStart('as')`);
V('_sessionPhaseIdx = 4'); // reflect
document.getElementById('sessionReflectText').value = '';
V('_sessionSaveReflection()');
check(fetchCalls.length === 0, 'reflexión vacía: NO llama a /save_note');
document.getElementById('sessionReflectText').value = 'Entendí bien la parte de complejidad.';
V('_sessionSaveReflection()');
check(fetchCalls.length === 1 && fetchCalls[0].url === '/save_note', 'reflexión con texto: llama a /save_note');
const body = JSON.parse(fetchCalls[0].opts.body);
check(body.kind === 'reflection', "el payload de /save_note lleva kind:'reflection'");
check(body.mode === 'session', "el payload de /save_note lleva mode:'session'");
check(body.text === 'Entendí bien la parte de complejidad.', 'el payload lleva el texto real escrito');

console.log(failures === 0 ? '\nTODO OK' : '\n' + failures + ' FALLO(S)');
process.exit(failures === 0 ? 0 : 1);
