// Arnés headless para AO_COMPARE / RA_COMPARE / AS_COMPARE (peldaño
// "Comparación" de la Escalera de Dominio, ver conversación 2026-08-13) —
// mismo espíritu de verificación que AO_CLASSIFY (project-ao-interleaving-
// classify): estructura de las preguntas, y que el gate por-par
// (_xxCompareUnlocked) solo desbloquea un par cuando AMBOS conceptos ya se
// completaron, nunca antes. No necesita un Flask real: solo evalúa los
// <script> de master-ao.js/master-ra.js/master-as.js.
// Uso: node verify/ao_compare_test.js

const fs = require('fs');
const path = require('path');

let failures = 0;
function check(cond, label) {
  if (cond) { console.log('OK   ' + label); }
  else { console.error('FAIL ' + label); failures++; }
}

function extractBracketed(src, startTag) {
  const start = src.indexOf(startTag);
  if (start < 0) return null;
  let i = start + startTag.length - 1, depth = 0;
  for (; i < src.length; i++) {
    const c = src[i];
    if (c === '[') depth++;
    else if (c === ']') { depth--; if (depth === 0) { i++; break; } }
    else if (c === '`') { i++; while (i < src.length && src[i] !== '`') { if (src[i] === '\\') i++; i++; } }
    else if (c === "'" || c === '"') { const q = c; i++; while (i < src.length && src[i] !== q) { if (src[i] === '\\') i++; i++; } }
  }
  return src.slice(start + startTag.length - 1, i);
}

const COURSES = [
  { mode: 'ao', file: 'master-ao.js', exVar: 'EX_AO', compareVar: 'AO_COMPARE', unlockedFn: '_aoCompareUnlocked' },
  { mode: 'ra', file: 'master-ra.js', exVar: 'EX_RA', compareVar: 'RA_COMPARE', unlockedFn: '_raCompareUnlocked' },
  { mode: 'as', file: 'master-as.js', exVar: 'EX_AS', compareVar: 'AS_COMPARE', unlockedFn: '_asCompareUnlocked' },
];

// LIMITS: mismo espíritu que COMPARE pero de un solo concepto ("concept",
// no "pair") -- peldaño "Limitación" (nivel 6, "¿cuándo NO funciona?").
const LIMITS_COURSES = [
  { mode: 'ao', file: 'master-ao.js', exVar: 'EX_AO', limitsVar: 'AO_LIMITS' },
  { mode: 'ra', file: 'master-ra.js', exVar: 'EX_RA', limitsVar: 'RA_LIMITS' },
  { mode: 'as', file: 'master-as.js', exVar: 'EX_AS', limitsVar: 'AS_LIMITS' },
];
let totalLimits = 0;
LIMITS_COURSES.forEach(({ mode, file, exVar, limitsVar }) => {
  const src = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', file), 'utf8');
  const EX = eval(extractBracketed(src, 'const ' + exVar + ' = ['));
  const limitsText = extractBracketed(src, 'const ' + limitsVar + '=[');
  check(!!limitsText, mode + ': ' + limitsVar + ' encontrado en ' + file);
  const LIMITS = eval(limitsText);
  totalLimits += LIMITS.length;
  check(LIMITS.length >= 5, mode + ': ' + limitsVar + ' tiene al menos 5 preguntas (' + LIMITS.length + ')');
  LIMITS.forEach((q, i) => {
    const c = q.concept;
    check(c % 4 === 0, mode + ' limits ' + i + ': concept es índice base (múltiplo de 4)');
    check(c >= 0 && c + 3 < EX.length, mode + ' limits ' + i + ': concept dentro de rango de ' + exVar);
    check(Array.isArray(q.options) && q.options.length === 4, mode + ' limits ' + i + ': 4 opciones');
    check(Number.isInteger(q.correct) && q.correct >= 0 && q.correct < 4, mode + ' limits ' + i + ': correct en rango 0-3');
    check(typeof q.question === 'string' && q.question.length > 20, mode + ' limits ' + i + ': enunciado no vacío');
    check(typeof q.solution === 'string' && q.solution.length > 20, mode + ' limits ' + i + ': solución no vacía');
  });
  function unlockedSim(doneSet, idx) {
    const c = LIMITS[idx].concept;
    return [c, c + 1, c + 2, c + 3].some(j => doneSet.has(j));
  }
  check(LIMITS.every((_, i) => !unlockedSim(new Set(), i)), mode + ' limits: con progreso vacío, nada desbloqueado');
  check(unlockedSim(new Set([LIMITS[0].concept + 1]), 0), mode + ' limits 0: desbloqueado con el concepto completado');
});

let totalPairs = 0;
COURSES.forEach(({ mode, file, exVar, compareVar }) => {
  const src = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', file), 'utf8');
  const EX = eval(extractBracketed(src, 'const ' + exVar + ' = ['));
  const compareText = extractBracketed(src, 'const ' + compareVar + '=[');
  check(!!compareText, mode + ': ' + compareVar + ' encontrado en ' + file);
  const COMPARE = eval(compareText);
  totalPairs += COMPARE.length;

  check(COMPARE.length >= 5, mode + ': ' + compareVar + ' tiene al menos 5 pares (' + COMPARE.length + ')');

  COMPARE.forEach((q, i) => {
    const [a, b] = q.pair;
    check(a % 4 === 0 && b % 4 === 0, mode + ' par ' + i + ': ambos índices son base (múltiplo de 4)');
    check(a >= 0 && a + 3 < EX.length && b >= 0 && b + 3 < EX.length, mode + ' par ' + i + ': índices dentro de rango de ' + exVar);
    check(a !== b, mode + ' par ' + i + ': compara dos conceptos DISTINTOS');
    check(Array.isArray(q.options) && q.options.length === 4, mode + ' par ' + i + ': 4 opciones');
    check(Number.isInteger(q.correct) && q.correct >= 0 && q.correct < 4, mode + ' par ' + i + ': correct en rango 0-3');
    check(typeof q.question === 'string' && q.question.length > 20, mode + ' par ' + i + ': enunciado no vacío');
    check(typeof q.solution === 'string' && q.solution.length > 20, mode + ' par ' + i + ': solución no vacía');
  });

  function unlockedSim(doneSet, pairIdx) {
    const [a, b] = COMPARE[pairIdx].pair;
    const done = x => [x, x + 1, x + 2, x + 3].some(j => doneSet.has(j));
    return done(a) && done(b);
  }

  check(COMPARE.every((_, i) => !unlockedSim(new Set(), i)), mode + ': con progreso vacío, ningún par desbloqueado');
  const [a0, b0] = COMPARE[0].pair;
  check(!unlockedSim(new Set([a0, a0 + 1]), 0), mode + ' par 0: bloqueado con solo UN lado completado');
  check(unlockedSim(new Set([a0, b0 + 2]), 0), mode + ' par 0: desbloqueado con AMBOS lados completados');
  const doneOnlyPair0 = new Set([a0, b0]);
  check(COMPARE.slice(1).every((_, i) => !unlockedSim(doneOnlyPair0, i + 1)), mode + ': completar el par 0 no desbloquea los demás');
});

// Integración en review.js / core.js / errors.js
const review = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', 'review.js'), 'utf8');
['AO_COMPARE', 'RA_COMPARE', 'AS_COMPARE', 'AO_LIMITS', 'RA_LIMITS', 'AS_LIMITS'].forEach(v => check(review.includes(v + '.forEach'), 'review.js: _reviewBuildPool empuja ' + v));
['aocompare', 'racompare', 'ascompare', 'aolimits', 'ralimits', 'aslimits'].forEach(m => check(review.includes("item.mode==='" + m + "'"), "review.js: _reviewSrc resuelve '" + m + "'"));
check(review.includes("aocompare:'⚖️ AO · Comparación'") && review.includes("racompare:'⚖️ RA · Comparación'") && review.includes("ascompare:'⚖️ AS · Comparación'"),
  'review.js: badges de los 3 orígenes *compare presentes');
check(review.includes("aolimits:'🚧 AO · Limitación'") && review.includes("ralimits:'🚧 RA · Limitación'") && review.includes("aslimits:'🚧 AS · Limitación'"),
  'review.js: badges de los 3 orígenes *limits presentes');

const core = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', 'core.js'), 'utf8');
['aocompare', 'racompare', 'ascompare', 'aolimits', 'ralimits', 'aslimits'].forEach(m => check(core.includes(m + ':{}'), "core.js: bucket '" + m + "' inicializado en _stats"));

const errorsJs = fs.readFileSync(path.join(__dirname, '..', 'static', 'js', 'errors.js'), 'utf8');
check(errorsJs.includes("aocompare:'⚖️ AO·Comp'") && errorsJs.includes("racompare:'⚖️ RA·Comp'") && errorsJs.includes("ascompare:'⚖️ AS·Comp'"),
  'errors.js: nombres de los 3 orígenes *compare presentes');
check(errorsJs.includes("aolimits:'🚧 AO·Lim'") && errorsJs.includes("ralimits:'🚧 RA·Lim'") && errorsJs.includes("aslimits:'🚧 AS·Lim'"),
  'errors.js: nombres de los 3 orígenes *limits presentes');

console.log(failures === 0 ? '\nTODO OK (' + (totalPairs * 7 + totalLimits * 6 + 30) + ' comprobaciones)' : '\n' + failures + ' FALLO(S)');
process.exit(failures === 0 ? 0 : 1);
