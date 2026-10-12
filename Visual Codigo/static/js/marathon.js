/* ──────────── 🎯 Maratón de examen ────────────
   Plan de estudio por PRESUPUESTO DE TIEMPO, a través de 1-3 materias
   elegidas, pensado para preparar un examen: arma una cola de temas
   (primero nunca vistos, luego los que ya tocan repaso Leitner, luego el
   resto -- ver [[project-theory-gate-inductive-entry]] para el bloqueo de
   teoría que ya complementa esto) y va recorriéndola llamando al Modo
   Maestro REAL de cada materia (mismo patrón que el Modo enfocado,
   _focusOpenMaster/_focusGoTo en core.js:337-341) -- teoría, código, quiz,
   todo igual que siempre, sin un panel propio que lo tape.

   Arquitectura: a diferencia de Simulacro de examen (panel propio
   exclusivo que reemplaza .main) esto sigue el patrón de Sesión guiada
   (session.js) -- un panel `#marathonBar` SOLO para configurar/ver
   resumen, y una insignia flotante (#marathonFloatBadge) que persiste
   mientras el maratón está activo, sin importar qué panel de materia esté
   abierto debajo. _marathonOpenCourse(mode) NO cierra el panel de la
   materia si ya es la misma que estaba abierta (evita el parpadeo de
   toggleMasterXx() cerrando lo que ya estaba bien).

   Persistencia: localStorage (mismo patrón que _stats/_aoDone, ver
   core.js) -- MARATHON_KEY guarda materias/presupuesto/cola/posición/
   tiempo acumulado. Al reabrir la app y tocar "🎯 Maratón de examen" con
   un maratón sin terminar guardado, retoma DIRECTO en el mismo punto, sin
   volver a pedir materias/horas -- pedido explícito del usuario. */

const MARATHON_KEY = 'pyvizExamMarathonV1';
const MARATHON_MIN_ITEM_SECONDS = 25; // piso: nunca menos que esto, aunque el presupuesto ya esté agotado
const MARATHON_GRACE_SECONDS = 15;    // lectura de la solución tras un timeout, antes de avanzar solo
const MARATHON_COURSES = {
  ao: { label: '🧬 AO' }, ra: { label: '🎲 RA' }, as: { label: '🤖 AS' },
  ns: { label: '🧩 NS' }, rn: { label: '🧠 RN' }, rf: { label: '🕹️ RF' },
};

let _marathonOn = false;                 // panel de config/resumen abierto (NO implica maratón activo)
let _marathonSelected = [];              // materias tildadas en la pantalla de config (antes de arrancar)
let _marathonCourses = [];               // materias del maratón ACTIVO (ya arrancado)
let _marathonTotalSeconds = 0;
let _marathonQueue = [];                 // [{mode, idx}, ...]
let _marathonQueuePos = 0;
let _marathonAccumulatedMs = 0;          // tiempo activo ya consumido (persistido)
let _marathonResumedAt = 0;              // Date.now() de cuando arrancó el tramo activo actual (en memoria, no persiste)
let _marathonTimeoutCount = 0;
let _marathonTimerHandle = null;
let _marathonItemSecondsLeft = 0;
let _marathonGraceHandle = null;
let _marathonGraceSecondsLeft = 0;
// Estado del ítem actual (para saber qué pintar en la insignia, sin inferir
// de varias banderas sueltas): 'ticking' = cuenta regresiva normal en curso;
// 'manual' = ya respondió a tiempo, espera un click en "Siguiente"; 'grace'
// = se agotó el tiempo sin responder, leyendo la solución antes de avanzar solo.
let _marathonItemState = 'ticking';

function _marathonExArr(mode){
  return { ao: typeof EX_AO!=='undefined'&&EX_AO, ra: typeof EX_RA!=='undefined'&&EX_RA,
    as: typeof EX_AS!=='undefined'&&EX_AS, ns: typeof EX_NS!=='undefined'&&EX_NS,
    rn: typeof EX_RN!=='undefined'&&EX_RN, rf: typeof EX_RF!=='undefined'&&EX_RF }[mode] || null;
}
function _marathonIsCourseOn(mode){
  if(mode==='ao') return typeof _aoOn!=='undefined' && _aoOn;
  if(mode==='ra') return typeof _raOn!=='undefined' && _raOn;
  if(mode==='as') return typeof _asOn!=='undefined' && _asOn;
  if(mode==='ns') return typeof _nsOn!=='undefined' && _nsOn;
  if(mode==='rn') return typeof _rnOn!=='undefined' && _rnOn;
  if(mode==='rf') return typeof _rfOn!=='undefined' && _rfOn;
  return false;
}
/* Abre la materia real SOLO si no está ya abierta (toggleMasterXx() es un
   toggle real -- llamarlo con la materia ya abierta la CERRARÍA). */
function _marathonOpenCourse(mode){
  if(_marathonIsCourseOn(mode)) return;
  if(typeof _focusOpenMaster==='function') _focusOpenMaster(mode);
}

/* ──────────── Persistencia (localStorage, mismo patrón que _stats) ──────────── */
function _marathonSave(){
  try{
    localStorage.setItem(MARATHON_KEY, JSON.stringify({
      courses: _marathonCourses, totalSeconds: _marathonTotalSeconds,
      queue: _marathonQueue, queuePos: _marathonQueuePos,
      accumulatedMs: _marathonAccumulatedMs, timeoutCount: _marathonTimeoutCount,
    }));
  }catch(e){}
}
function _marathonLoad(){
  try{
    const raw=localStorage.getItem(MARATHON_KEY);
    if(!raw) return null;
    return JSON.parse(raw);
  }catch(e){ return null; }
}
function _marathonClear(){
  try{ localStorage.removeItem(MARATHON_KEY); }catch(e){}
}
/* Cuenta como "tiempo usado" solo mientras el maratón está efectivamente
   corriendo (item activo, sin importar si el panel #marathonBar está
   abierto o cerrado) -- _marathonResumedAt marca el inicio del tramo en
   curso; al pausar (avance manual, cierre, fin) se vuelca a accumulatedMs. */
function _marathonFlushElapsed(){
  if(_marathonResumedAt){
    _marathonAccumulatedMs += Date.now()-_marathonResumedAt;
    _marathonResumedAt=0;
  }
}

/* ──────────── Nav / panel ──────────── */
function toggleMarathonMode(){
  if(_marathonOn){ _marathonClosePanel(); return; }
  // Cierra los paneles "utilitarios" mutuamente excluyentes -- A PROPÓSITO
  // NO cierra ningún Modo Maestro de materia: el maratón convive con el
  // panel de materia que esté guiando en ese momento.
  if(typeof _reviewOn!=='undefined' && _reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _errorsOn!=='undefined' && _errorsOn) _errorsClose();
  if(typeof _examOn!=='undefined' && _examOn) _examClose();
  if(typeof _sessionOn!=='undefined' && _sessionOn) _sessionClosePanel();
  _marathonOn=true;
  document.getElementById('marathonBar').style.display='flex';
  const b=document.getElementById('bMarathon');
  if(b){ b.classList.add('btn-looping'); }
  _marathonRenderPanel();
  if(typeof autoLayout==='function') autoLayout();
}
function _marathonClosePanel(){
  _marathonOn=false;
  const bar=document.getElementById('marathonBar');
  if(bar) bar.style.display='none';
  const b=document.getElementById('bMarathon');
  if(b) b.classList.remove('btn-looping');
  if(typeof autoLayout==='function') autoLayout();
}
/* Decide qué mostrar en #marathonBar al abrirlo: si hay un maratón GUARDADO
   sin terminar, retoma directo (sin pedir materias/horas de nuevo); si no,
   pantalla de configuración. */
function _marathonRenderPanel(){
  const saved=_marathonLoad();
  if(saved && saved.queue && saved.queuePos < saved.queue.length){
    _marathonRenderProgressView(saved);
  } else {
    _marathonRenderSetupView();
  }
}
function _marathonRenderSetupView(){
  const body=document.getElementById('marathonBody');
  if(!body) return;
  const chips=Object.keys(MARATHON_COURSES).map(mode=>{
    const on=_marathonSelected.includes(mode);
    return `<button class="marathon-course-chip${on?' marathon-course-chip-on':''}" onclick="_marathonToggleCourse('${mode}')">${MARATHON_COURSES[mode].label}</button>`;
  }).join('');
  body.innerHTML =
    '<div class="marathon-setup">'+
    '<p class="marathon-setup-hint">Elegí de 1 a 3 materias y cuántas horas totales le vas a dedicar hoy. El tiempo se reparte solo entre los temas que falten, y se reajusta si te demorás en alguno.</p>'+
    '<div class="marathon-course-chips">'+chips+'</div>'+
    '<label class="marathon-hours-label">Horas totales: <input type="number" id="marathonHoursInput" min="0.5" step="0.5" value="4" class="marathon-hours-input"></label>'+
    '<button class="master-btn" onclick="_marathonStart()">🎯 Empezar el maratón</button>'+
    '</div>';
}
function _marathonToggleCourse(mode){
  const i=_marathonSelected.indexOf(mode);
  if(i>=0) _marathonSelected.splice(i,1);
  else if(_marathonSelected.length<3) _marathonSelected.push(mode);
  _marathonRenderSetupView();
}
function _marathonRenderProgressView(saved){
  const body=document.getElementById('marathonBody');
  if(!body) return;
  const pct=Math.round((saved.queuePos/saved.queue.length)*100);
  const perCourse=_marathonCoverageByCourse(saved);
  const rows=perCourse.map(c=>
    `<div class="marathon-progress-row"><span>${MARATHON_COURSES[c.mode].label}</span><span>${c.covered}/${c.total} temas</span></div>`
  ).join('');
  body.innerHTML =
    '<div class="marathon-progress-view">'+
    '<div class="marathon-progress-title">Maratón en curso — '+pct+'% de la cola recorrida</div>'+
    '<div class="marathon-progress-rows">'+rows+'</div>'+
    '<div class="marathon-progress-note">🤷 '+(saved.timeoutCount||0)+' tema(s) avanzados por tiempo agotado (marcados "no sé", ya en tu repaso).</div>'+
    '<button class="master-btn" onclick="_marathonResume()">▶ Continuar donde quedé</button> '+
    '<button class="master-btn master-btn-exit" onclick="_marathonConfirmAbandon()">Abandonar y empezar de nuevo</button>'+
    '</div>';
}
function _marathonCoverageByCourse(saved){
  return saved.courses.map(mode=>{
    const total=saved.queue.filter(it=>it.mode===mode).length;
    const covered=saved.queue.slice(0, saved.queuePos).filter(it=>it.mode===mode).length;
    return {mode, total, covered};
  });
}
function _marathonConfirmAbandon(){
  _marathonClear();
  _marathonQueue=[]; _marathonQueuePos=0; _marathonCourses=[]; _marathonSelected=[];
  _marathonRenderSetupView();
}

/* ──────────── Construcción de la cola ──────────── */
/* Bloque por materia (no intercalado, ver [[user-learning-profile]]): dentro
   de cada materia, nunca-intentado -> vencido para repaso -> el resto. */
function _marathonBuildQueue(courses){
  const now=Date.now();
  const queue=[];
  courses.forEach(mode=>{
    const arr=_marathonExArr(mode);
    if(!arr) return;
    const never=[], due=[], rest=[];
    for(let idx=0; idx<arr.length; idx++){
      const s=_statsFor(mode, idx);
      if(s.attempts===0) never.push(idx);
      else if(s.due<=now) due.push(idx);
      else rest.push(idx);
    }
    never.concat(due, rest).forEach(idx=>queue.push({mode, idx}));
  });
  return queue;
}

/* ──────────── Arranque / resume ──────────── */
function _marathonStart(){
  if(!_marathonSelected.length) return;
  const hoursInput=document.getElementById('marathonHoursInput');
  const hours=Math.max(0.5, parseFloat(hoursInput ? hoursInput.value : '4') || 4);
  _marathonCourses=_marathonSelected.slice();
  _marathonTotalSeconds=Math.round(hours*3600);
  _marathonQueue=_marathonBuildQueue(_marathonCourses);
  _marathonQueuePos=0;
  _marathonAccumulatedMs=0;
  _marathonTimeoutCount=0;
  _marathonSave();
  if(!_marathonQueue.length){
    const body=document.getElementById('marathonBody');
    if(body) body.innerHTML='<p class="marathon-setup-hint">Las materias elegidas no tienen temas cargados todavía.</p>';
    return;
  }
  _marathonRunFrom(0);
}
function _marathonResume(){
  const saved=_marathonLoad();
  if(!saved) return;
  _marathonCourses=saved.courses; _marathonTotalSeconds=saved.totalSeconds;
  _marathonQueue=saved.queue; _marathonQueuePos=saved.queuePos;
  _marathonAccumulatedMs=saved.accumulatedMs||0; _marathonTimeoutCount=saved.timeoutCount||0;
  _marathonRunFrom(_marathonQueuePos);
}
function _marathonRunFrom(pos){
  _marathonQueuePos=pos;
  if(_marathonQueuePos>=_marathonQueue.length){ _marathonFinish(); return; }
  _marathonClosePanel();
  const item=_marathonQueue[_marathonQueuePos];
  _marathonOpenCourse(item.mode);
  if(typeof _focusGoTo==='function') _focusGoTo(item.mode, item.idx);
  _marathonStartItemTimer();
  _marathonRenderBadge();
}
/* ──────────── Timer por ítem (recalculado en CADA ítem: presupuesto
   dinámico, ver el plan) ──────────── */
function _marathonStartItemTimer(){
  _marathonStopItemTimer();
  _marathonItemState='ticking';
  _marathonResumedAt=Date.now();
  const itemsLeft=Math.max(1, _marathonQueue.length-_marathonQueuePos);
  const usedSeconds=Math.round(_marathonAccumulatedMs/1000);
  const secondsLeft=Math.max(0, _marathonTotalSeconds-usedSeconds);
  _marathonItemSecondsLeft=Math.max(MARATHON_MIN_ITEM_SECONDS, Math.round(secondsLeft/itemsLeft));
  _marathonTimerHandle=setInterval(_marathonTick, 1000);
}
function _marathonStopItemTimer(){
  if(_marathonTimerHandle){ clearInterval(_marathonTimerHandle); _marathonTimerHandle=null; }
}
function _marathonTick(){
  if(_marathonItemState!=='ticking') return;
  const item=_marathonQueue[_marathonQueuePos];
  if(!item) return;
  const fb=document.getElementById(_quizIds(item.mode).feedback);
  if(fb && fb.style.display==='block'){
    // Ya respondió (acertó o falló) dentro del tiempo: se detiene el reloj y
    // queda a su criterio cuándo seguir -- análisis propio del error antes
    // de avanzar, no se le fuerza nada mientras estuvo activo a tiempo.
    _marathonPauseForManualAdvance();
    return;
  }
  _marathonItemSecondsLeft--;
  _marathonRenderBadge();
  if(_marathonItemSecondsLeft<=0) _marathonTimeoutAdvance();
}
function _marathonPauseForManualAdvance(){
  _marathonStopItemTimer();
  _marathonItemState='manual';
  _marathonFlushElapsed();
  _marathonSave();
  _marathonRenderBadge();
}
/* Timeout real (nunca respondió): dispara el mecanismo YA existente de
   "No sé" (_quizDontKnowClick, core.js) -- registra el intento como
   dontKnow (no como fallo), revela la solución, y dispara la gracia de
   lectura antes de avanzar solo. */
function _marathonTimeoutAdvance(){
  _marathonStopItemTimer();
  const item=_marathonQueue[_marathonQueuePos];
  if(item && typeof _quizDontKnowClick==='function' && !_quizIsAnswered(item.mode)){
    _quizDontKnowClick(item.mode);
    _marathonTimeoutCount++;
  }
  _marathonFlushElapsed();
  _marathonSave();
  _marathonStartGrace();
}
function _marathonStartGrace(){
  _marathonItemState='grace';
  _marathonGraceSecondsLeft=MARATHON_GRACE_SECONDS;
  _marathonRenderBadge();
  _marathonGraceHandle=setInterval(()=>{
    _marathonGraceSecondsLeft--;
    _marathonRenderBadge();
    if(_marathonGraceSecondsLeft<=0){
      clearInterval(_marathonGraceHandle); _marathonGraceHandle=null;
      _marathonAdvanceQueue();
    }
  }, 1000);
}
function _marathonStayLonger(){
  if(_marathonGraceHandle){ clearInterval(_marathonGraceHandle); _marathonGraceHandle=null; }
  _marathonItemState='manual';
  _marathonRenderBadge();
}
/* Botón manual "Siguiente tema del maratón" -- disponible tanto tras
   responder a tiempo como tras "quedarme un poco más" en la gracia. */
function _marathonAdvanceQueue(){
  _marathonFlushElapsed();
  const usedSeconds=Math.round(_marathonAccumulatedMs/1000);
  if(usedSeconds>=_marathonTotalSeconds || _marathonQueuePos+1>=_marathonQueue.length){
    _marathonQueuePos++; _marathonSave();
    _marathonFinish();
    return;
  }
  _marathonRunFrom(_marathonQueuePos+1);
  _marathonSave();
}

/* ──────────── Insignia flotante (persiste con cualquier panel de materia
   abierto debajo, mismo patrón que #sessionFloatBadge) ──────────── */
function _marathonRenderBadge(){
  const b=document.getElementById('marathonFloatBadge');
  if(!b) return;
  if(!_marathonQueue.length || _marathonQueuePos>=_marathonQueue.length){ b.style.display='none'; return; }
  const item=_marathonQueue[_marathonQueuePos];
  const label=MARATHON_COURSES[item.mode] ? MARATHON_COURSES[item.mode].label : item.mode;
  b.style.display='flex';
  let timeHtml;
  if(_marathonItemState==='grace'){
    timeHtml=`<span class="marathon-badge-grace">⏭ avanzando en ${_marathonGraceSecondsLeft}s</span>`+
      `<button class="marathon-badge-btn" onclick="event.stopPropagation();_marathonStayLonger()">Quedarme más</button>`;
  } else if(_marathonItemState==='manual'){
    timeHtml=`<button class="marathon-badge-btn marathon-badge-btn-next" onclick="event.stopPropagation();_marathonAdvanceQueue()">Siguiente tema ⏭</button>`;
  } else {
    const mm=String(Math.floor(_marathonItemSecondsLeft/60)).padStart(2,'0');
    const ss=String(_marathonItemSecondsLeft%60).padStart(2,'0');
    timeHtml=`<span class="marathon-badge-time${_marathonItemSecondsLeft<=15?' marathon-badge-urgent':''}">${mm}:${ss}</span>`;
  }
  b.innerHTML=`<span class="marathon-badge-pos">🎯 ${label} · tema ${_marathonQueuePos+1}/${_marathonQueue.length}</span>`+timeHtml;
}

function _marathonFinish(){
  _marathonStopItemTimer();
  if(_marathonGraceHandle){ clearInterval(_marathonGraceHandle); _marathonGraceHandle=null; }
  _marathonFlushElapsed();
  _marathonSave();
  const b=document.getElementById('marathonFloatBadge');
  if(b) b.style.display='none';
  const saved={courses:_marathonCourses, queue:_marathonQueue, queuePos:_marathonQueuePos, timeoutCount:_marathonTimeoutCount};
  toggleMarathonMode();
  const body=document.getElementById('marathonBody');
  if(body){
    const perCourse=_marathonCoverageByCourse(saved);
    const rows=perCourse.map(c=>
      `<div class="marathon-progress-row"><span>${MARATHON_COURSES[c.mode].label}</span><span>${c.covered}/${c.total} temas</span></div>`
    ).join('');
    body.innerHTML='<div class="marathon-progress-view">'+
      '<div class="marathon-progress-title">🏁 Maratón terminado</div>'+
      '<div class="marathon-progress-rows">'+rows+'</div>'+
      '<div class="marathon-progress-note">🤷 '+_marathonTimeoutCount+' tema(s) avanzados por tiempo agotado — revisalos en tu 📓 Cuaderno de errores o en 🔀 Repaso mezclado.</div>'+
      '<button class="master-btn" onclick="_marathonConfirmAbandon()">Armar otro maratón</button>'+
      '</div>';
  }
  _marathonClear();
}
