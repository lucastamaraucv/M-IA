// Arnés headless para el peldaño "Transferencia" (crea tu propia pregunta,
// ver conversación 2026-08-13) — comprueba el wiring estático (función JS,
// ruta Flask, ids del template) sin necesitar un navegador real. La lógica
// de notes_store.py (columna 'kind') se prueba aparte con Python directo.
// Uso: node verify/transfer_question_test.js

const fs = require('fs');
const path = require('path');

let failures = 0;
function check(cond, label) {
  if (cond) { console.log('OK   ' + label); }
  else { console.error('FAIL ' + label); failures++; }
}

const ROOT = path.join(__dirname, '..');
const math = fs.readFileSync(path.join(ROOT, 'static', 'js', 'master-math.js'), 'utf8');
check(math.includes('function _transferSaveQuestion(mode)'), 'master-math.js: _transferSaveQuestion definido');
check(math.includes("kind:'transfer'"), "master-math.js: /save_note se llama con kind:'transfer'");

const py = fs.readFileSync(path.join(ROOT, 'static', 'js', 'master-py.js'), 'utf8');
check(py.includes('transferIds'), 'master-py.js: _resetSelfExplain también limpia el textarea de transferencia');

const html = fs.readFileSync(path.join(ROOT, 'templates', 'index.html'), 'utf8');
['Ao', 'Ra', 'As'].forEach(suf => {
  check(html.includes('id="transferText' + suf + '"'), 'index.html: textarea transferText' + suf + ' presente');
  check(html.includes("_transferSaveQuestion('" + suf.toLowerCase() + "')"), 'index.html: botón llama a _transferSaveQuestion(\'' + suf.toLowerCase() + '\')');
  check(html.includes('id="transferSaved' + suf + '"'), 'index.html: span transferSaved' + suf + ' presente');
});

const flask = fs.readFileSync(path.join(ROOT, 'python_visualizer_flask.py'), 'utf8');
check(flask.includes("kind = data.get('kind') or 'note'"), 'python_visualizer_flask.py: /save_note lee kind del body');
check(flask.includes('save_note(mode, topic_idx, topic_name, text, feedback, kind)'), 'python_visualizer_flask.py: save_note() recibe kind');

const notesStore = fs.readFileSync(path.join(ROOT, 'notes_store.py'), 'utf8');
check(notesStore.includes("ADD COLUMN kind"), "notes_store.py: migración aditiva de 'kind'");
check(notesStore.includes("def save_note(mode, topic_idx, topic_name, text, feedback=None, kind='note')"), 'notes_store.py: save_note() acepta kind con default note');

console.log(failures === 0 ? '\nTODO OK' : '\n' + failures + ' FALLO(S)');
process.exit(failures === 0 ? 0 : 1);
