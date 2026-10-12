/* ──────────── Simulacro de examen: 3 exámenes independientes ────────────
   A diferencia de los 3 Modos Maestro y de Repaso mezclado (práctica SIN
   presión: reintentas hasta acertar, sin límite de tiempo, con teoría y
   pistas siempre a mano), esto simula las condiciones del examen real:
   60 minutos, una pregunta por cada tema del curso completo, sin reintento
   ni feedback inmediato, código en solo lectura (sin depurador). La
   investigación de transferencia apropiada es clara: practicar en
   condiciones distintas a las del examen deja un hueco justo el día que
   más importa -- esta es la fase "hacer simulacro" del propio plan de
   aprendizaje del usuario.
   Reutiliza _quizPickOne/_shuffleMcOptions/esc/_logErrorJournal/
   _reportTopicName/autoLayout, todos ya en core.js -- ver ese archivo para
   el patrón original (Repaso mezclado hace algo parecido, sin cronómetro
   ni bloqueo de reintento). */
const EXAM_DURATION_SECS = 60 * 60; // 1 hora

let _examOn = false, _examMode = null, _examQuestions = [], _examPos = 0;
let _examTimerHandle = null, _examSecondsLeft = 0;
let _examShuffledCorrect = null, _examShuffledOrder = null, _examSelectedIdx = null;

/* Índices BASE de cada tema (1 cada 4, mismo patrón "topic × 4 preguntas
   aplanadas" usado en todo el proyecto) -- un examen toma UNA pregunta de
   cada tema, no las 4, para cubrir el temario completo sin que un examen
   de AO tenga 164 preguntas. */
function _examTopicBases(total) {
  const bases = [];
  for (let i = 0; i < total; i += 4) bases.push(i);
  return bases;
}
const EXAM_COURSES = { ao: { label: '🧬 AO' }, ra: { label: '🎲 RA' }, as: { label: '🤖 AS' } };
/* EX_AO/RA/AS y AO_QUIZ/RA_QUIZ/AS_QUIZ son `const` a nivel de módulo en sus
   respectivos master-*.js -- eso los deja accesibles por identificador
   normal a cualquier script cargado despues (mismo scope léxico de página),
   pero NO como propiedades de `window` (a diferencia de `function`/`var`),
   así que la búsqueda por nombre se hace con este switch, no con
   window[nombre]. */
function _examExArr(mode) { return mode === 'ao' ? EX_AO : mode === 'ra' ? EX_RA : EX_AS; }
function _examQuizArr(mode) { return mode === 'ao' ? AO_QUIZ : mode === 'ra' ? RA_QUIZ : AS_QUIZ; }

function toggleExamMode() {
  if (_examOn) { _examClose(); return; }
  if (typeof _masterOn !== 'undefined' && _masterOn) exitMasterMode();
  if (typeof _aoOn !== 'undefined' && _aoOn) exitMasterAo();
  if (typeof _mathOn !== 'undefined' && _mathOn) exitMasterMath();
  if (typeof _raOn !== 'undefined' && _raOn) exitMasterRa();
  if (typeof _asOn !== 'undefined' && _asOn) exitMasterAs();
  if (typeof _nsOn !== 'undefined' && _nsOn) exitMasterNs();
  if (typeof _rnOn !== 'undefined' && _rnOn) exitMasterRn();
  if (typeof _rfOn !== 'undefined' && _rfOn) exitMasterRf();
  if (typeof _reviewOn !== 'undefined' && _reviewOn) exitReviewMode();
  if (typeof _calOn !== 'undefined' && _calOn) _calClose();
  if (typeof _reportOn !== 'undefined' && _reportOn) _reportClose();
  if (typeof _errorsOn !== 'undefined' && _errorsOn) _errorsClose();
  if (typeof _marathonOn !== 'undefined' && _marathonOn) _marathonClosePanel();
  _examOn = true;
  document.getElementById('examBar').style.display = 'flex';
  document.querySelector('.main').style.display = 'none';
  const b = document.getElementById('bExam');
  if (b) { b.textContent = '📝 Simulacro de examen (activo)'; b.classList.add('btn-looping'); }
  _examShowSelectView();
  if (typeof autoLayout === 'function') autoLayout();
}
function _examClose() {
  _examStopTimer();
  _examOn = false;
  document.getElementById('examBar').style.display = 'none';
  document.querySelector('.main').style.display = 'flex';
  const b = document.getElementById('bExam');
  if (b) { b.textContent = '📝 Simulacro de examen'; b.classList.remove('btn-looping'); }
  if (typeof autoLayout === 'function') autoLayout();
}
function _examShowSelectView() {
  document.getElementById('examSelectView').style.display = 'block';
  document.getElementById('examInProgressView').style.display = 'none';
  document.getElementById('examResultsView').style.display = 'none';
  document.getElementById('examTimer').style.display = 'none';
  ['ao', 'ra', 'as'].forEach(mode => {
    const exArr = _examExArr(mode);
    const n = exArr ? _examTopicBases(exArr.length).length : 0;
    const el = document.getElementById('examCount' + mode[0].toUpperCase() + mode.slice(1));
    if (el) el.textContent = n + ' preguntas · 60 min';
  });
}

/* Construye el set de preguntas (una por tema) y arranca el examen. */
function _examStart(mode) {
  const exArr = _examExArr(mode), quizArr = _examQuizArr(mode);
  if (!exArr || !quizArr) return;
  _examMode = mode;
  const bases = _examTopicBases(exArr.length);
  _examQuestions = bases.map(idx => ({
    idx,
    topicName: exArr[idx].name,
    code: exArr[idx].code,
    q: _quizPickOne(quizArr, idx),
    selected: null,     // índice mostrado (mc) o texto (numeric) elegido por el alumno
    answered: false,
  }));
  _examPos = 0;
  _examSecondsLeft = EXAM_DURATION_SECS;
  document.getElementById('examSelectView').style.display = 'none';
  document.getElementById('examInProgressView').style.display = 'block';
  document.getElementById('examResultsView').style.display = 'none';
  document.getElementById('examTimer').style.display = 'inline-block';
  _examRenderQuestion();
  _examStartTimer();
  if (typeof autoLayout === 'function') autoLayout();
}

function _examStartTimer() {
  _examStopTimer();
  _examUpdateTimerDisplay();
  _examTimerHandle = setInterval(() => {
    _examSecondsLeft--;
    _examUpdateTimerDisplay();
    if (_examSecondsLeft <= 0) _examFinish(true);
  }, 1000);
}
function _examStopTimer() {
  if (_examTimerHandle) { clearInterval(_examTimerHandle); _examTimerHandle = null; }
}
function _examUpdateTimerDisplay() {
  const el = document.getElementById('examTimer');
  if (!el) return;
  const s = Math.max(0, _examSecondsLeft);
  const mm = String(Math.floor(s / 60)).padStart(2, '0');
  const ss = String(s % 60).padStart(2, '0');
  el.textContent = mm + ':' + ss;
  el.className = 'exam-timer' + (s <= 300 ? ' exam-timer-urgent' : '');
}

function _examRenderQuestion() {
  const item = _examQuestions[_examPos];
  const q = item.q;
  _examSelectedIdx = null;
  document.getElementById('examProgress').textContent =
    'Pregunta ' + (_examPos + 1) + '/' + _examQuestions.length + ' — ' + esc(item.topicName);
  document.getElementById('examCode').textContent = item.code;
  document.getElementById('examQuestionBody').innerHTML = q.question;
  const optWrap = document.getElementById('examOptions');
  const numWrap = document.getElementById('examNumericWrap');
  const nextBtn = document.getElementById('examNextBtn');
  nextBtn.disabled = true;
  if (q.type === 'mc') {
    optWrap.style.display = 'grid';
    numWrap.style.display = 'none';
    const shuffled = _shuffleMcOptions(q);
    _examShuffledCorrect = shuffled.correct;
    _examShuffledOrder = shuffled.order;
    optWrap.innerHTML = shuffled.options.map((o, i) =>
      `<button class="math-option" onclick="_examSelectOption(${i})">${String.fromCharCode(97 + i)}) ${o}</button>`).join('');
  } else {
    optWrap.style.display = 'none';
    numWrap.style.display = 'flex';
    _examShuffledCorrect = null;
    _examShuffledOrder = null;
    const inp = document.getElementById('examNumericInput');
    inp.value = '';
    inp.oninput = () => { nextBtn.disabled = inp.value.trim() === ''; };
  }
}
/* A diferencia de _aoCheckQuizAnswer, aquí NO se revela si es correcta --
   solo se marca visualmente cuál quedó elegida (examen real: puedes
   cambiar de opción antes de pasar a la siguiente pregunta, pero no sabes
   si acertaste hasta entregar). */
function _examSelectOption(shownIdx) {
  _examSelectedIdx = shownIdx;
  document.querySelectorAll('#examOptions .math-option').forEach((btn, i) => {
    btn.classList.toggle('exam-option-selected', i === shownIdx);
  });
  document.getElementById('examNextBtn').disabled = false;
}
function _examNext() {
  const item = _examQuestions[_examPos];
  const q = item.q;
  if (q.type === 'mc') {
    item.selected = _examSelectedIdx;
    item.selectedOriginalIdx = (_examSelectedIdx !== null && _examShuffledOrder) ? _examShuffledOrder[_examSelectedIdx] : null;
    item.correct = item.selectedOriginalIdx === q.correct;
  } else {
    const raw = document.getElementById('examNumericInput').value.trim().replace(',', '.');
    const val = parseFloat(raw);
    item.selected = raw;
    const dec = q.decimals || 0;
    const p = Math.pow(10, dec);
    item.correct = !isNaN(val) && Math.round(val * p) === Math.round(q.correct * p);
  }
  item.answered = true;
  if (_examPos < _examQuestions.length - 1) {
    _examPos++;
    _examRenderQuestion();
  } else {
    _examFinish(false);
  }
}

/* Fin del examen (por completar todas las preguntas o por agotar el
   tiempo): calcula la nota, registra cada fallo mc con whyNot en el
   Cuaderno de errores (mismo _logErrorJournal que ya usan los 3 Modos
   Maestro y Repaso mezclado, ver core.js), y pinta los resultados. */
function _examFinish(byTimeout) {
  _examStopTimer();
  const total = _examQuestions.length;
  let correct = 0;
  const failedTopics = [];
  _examQuestions.forEach(item => {
    if (item.answered && item.correct) { correct++; return; }
    if (item.answered && !item.correct) {
      failedTopics.push(item);
      const q = item.q;
      if (q.type === 'mc' && q.whyNot && item.selectedOriginalIdx !== null && item.selectedOriginalIdx !== undefined) {
        const whyWrong = q.whyNot[item.selectedOriginalIdx];
        if (whyWrong) {
          const topicName = (typeof _reportTopicName === 'function' && _reportTopicName(_examMode, item.idx)) || item.topicName;
          _logErrorJournal(_examMode, item.idx, topicName, q.question, q.options[item.selectedOriginalIdx], q.options[q.correct], whyWrong);
        }
      }
    } else {
      failedTopics.push(item); // sin responder (tiempo agotado antes de llegar)
    }
  });
  const pct = total > 0 ? Math.round(correct / total * 100) : 0;
  const label = EXAM_COURSES[_examMode].label;

  let html = '<div class="exam-results-score">' + label + ' — ' + correct + '/' + total + ' (' + pct + '%)</div>';
  html += '<div class="exam-results-note">' + (byTimeout ? '⏱️ Entregado automáticamente al agotarse el tiempo.' : '✅ Examen completado.') + '</div>';
  if (failedTopics.length) {
    html += '<div class="exam-results-hdr">Temas a repasar (' + failedTopics.length + '):</div>';
    html += '<div class="exam-results-list">' + failedTopics.map(item =>
      '<div class="exam-results-item" onclick="_examGoToTopic(\'' + _examMode + '\',' + item.idx + ')">' +
        '<span>' + esc(item.topicName) + '</span><span class="exam-results-arrow">repasar →</span></div>'
    ).join('') + '</div>';
    html += '<div class="exam-results-note">Los fallos con explicación ya quedaron guardados en tu 📓 Cuaderno de errores.</div>';
  } else if (total > 0) {
    html += '<div class="exam-results-note">🎉 Respondiste bien todas las preguntas.</div>';
  }

  document.getElementById('examResultsBody').innerHTML = html;
  document.getElementById('examInProgressView').style.display = 'none';
  document.getElementById('examResultsView').style.display = 'block';
  document.getElementById('examTimer').style.display = 'none';
  if (typeof autoLayout === 'function') autoLayout();
}
function _examGoToTopic(mode, idx) {
  _examClose();
  const fn = { ao: 'toggleMasterAo', ra: 'toggleMasterRa', as: 'toggleMasterAs' }[mode];
  if (fn && typeof window[fn] === 'function') {
    window[fn]();
    const goFn = { ao: '_aoGoTo', ra: '_raGoTo', as: '_asGoTo' }[mode];
    if (goFn && typeof window[goFn] === 'function') window[goFn](idx);
  }
}
