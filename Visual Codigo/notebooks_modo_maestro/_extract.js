// One-off extraction script: pulls the <select id="exSel"> option groups
// and the `const EX = [...]` examples array out of python_visualizer_flask.py
// by evaluating them as real JS, so escaping (e.g. \n, \d) resolves exactly
// like it does in the browser. Writes notebooks_modo_maestro/sessions.json.
const fs = require('fs');
const path = require('path');

const srcPath = path.join(__dirname, '..', 'python_visualizer_flask.py');
const text = fs.readFileSync(srcPath, 'utf8');

// ── 1. Parse the <select id="exSel"> block for group labels per option ──
const selStart = text.indexOf('<select class="hsel" id="exSel"');
const selEnd = text.indexOf('</select>', selStart);
const selBlock = text.slice(selStart, selEnd);

const groups = []; // {value, group, label}
let curGroup = null;
const lineRe = /<optgroup label="([^"]+)">|<option value="(\d+)">([^<]+)<\/option>/g;
let m;
while ((m = lineRe.exec(selBlock)) !== null) {
  if (m[1] !== undefined) {
    curGroup = m[1];
  } else {
    groups[Number(m[2])] = { value: Number(m[2]), group: curGroup, label: m[3] };
  }
}

// ── 2. Extract `const EX = [ ... ];` and eval it as real JS ──
const exStart = text.indexOf('const EX = [');
// find the matching "];" that closes the array (first "];" at column start after exStart works
// because no nested "];" sequence occurs inside the template literals used here)
const exEnd = text.indexOf('\n];', exStart) + 3;
const exSrc = text.slice(exStart, exEnd);

let EX;
try {
  EX = eval(exSrc.replace('const EX =', '(') .replace(/;\s*$/, ')'));
} catch (e) {
  console.error('EVAL FAILED:', e.message);
  process.exit(1);
}

if (EX.length !== groups.filter(Boolean).length) {
  console.error(`Mismatch: EX has ${EX.length} entries, <select> has ${groups.filter(Boolean).length} options`);
}

const sessions = EX.map((ex, i) => ({
  id: i,
  group: groups[i] ? groups[i].group : null,
  name: ex.name,
  code: ex.code,
  practica: ex.practica || null,
}));

fs.writeFileSync(
  path.join(__dirname, 'sessions.json'),
  JSON.stringify(sessions, null, 2),
  'utf8'
);
console.log(`Wrote ${sessions.length} sessions to sessions.json`);
