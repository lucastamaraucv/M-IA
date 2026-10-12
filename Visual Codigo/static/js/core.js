/* ──────────── State ──────────── */
let steps=[], cur=-1, prev=null;
let relations={};  // iterVar → sourceVar from AST
let explains={};   // lineno → {text, kind} from AST narrator
let bps=new Set(), selVar=null, selVal=null;
let autoTmr=null, loopTmr=null, lastOut='', dragging=false;
let _objSnapshot={name:null, val:null}; // last rendered Objects-panel value, for change-flash diffing
let _lastRunError=null; // set from /prepare's `error` field — shown instead of a misleading "terminado"
let _lastRunTruncated=false; // true = corte de seguridad (2000 pasos / 12s), NO un bug del código del alumno
let _knownRagged=new Set(); // variable names ever seen as a ragged list-of-lists — see renderObjects
let _listViewMode='auto'; // 'auto' (bars for numeric lists, cards otherwise) | 'bars' | 'cards'

/* kind → emoji icon for the narrator */
const NAR_ICO={assign:'📌',augassign:'➕',loop:'🔁',cond:'🔀',with:'🗂️',
  try:'🛡️',except:'⚠️',def:'🧩',class:'🏛️',return:'↩️',yield:'🌱',
  import:'📦',print:'🖨️',call:'⚙️',method:'🔧',expr:'🧮',assert:'✔️',
  raise:'🚨',pass:'⏭️',break:'⏹️',continue:'⏩',del:'🗑️',global:'🌐',done:'✅'};

/* ──────────── Edit ↔ Run view toggle (single code panel) ──────────── */
function setCodeView(running){
  const ed=document.getElementById('edView');
  const ex=document.getElementById('execScroll');
  const eb=document.getElementById('editBtn');
  if(ed) ed.style.display = running?'none':'flex';
  if(ex) ex.style.display = running?'block':'none';
  if(eb) eb.style.display = running?'inline-block':'none';
}
function editMode(){
  stopAuto();
  setCodeView(false);
  document.getElementById('pyHdrTxt').textContent='Python 3 · Editando';
  setSt('✏️ Modo edición — pega o escribe tu código y pulsa ▶ Run');
  const nb=document.getElementById('narrator');
  if(nb){ nb.className='narrator narrator-idle';
    document.getElementById('narIco').textContent='💡';
    document.getElementById('narTxt').textContent='El narrador explicará cada línea al avanzar paso a paso'; }
  renderLineNums();
  const ta=document.getElementById('codeInput'); if(ta) ta.focus();
}

/* Copia SOLO el código Python (el contenido real de #codeInput, la misma
   fuente de verdad tanto en modo edición como en modo ejecución paso a
   paso — nunca el output/narrador/paneles) al portapapeles. Un solo botón
   sirve para los 4 Modos Maestro y para código pegado a mano, porque
   todos pasan por el mismo #codeInput. */
function copyCode(){
  const code=document.getElementById('codeInput').value;
  if(!code.trim()) return;
  const btn=document.getElementById('copyCodeBtn');
  const flashOk=()=>{
    if(!btn) return;
    const prev=btn.textContent;
    btn.textContent='✅ Copiado';
    btn.classList.add('copy-btn-ok');
    setTimeout(()=>{ btn.textContent=prev; btn.classList.remove('copy-btn-ok'); }, 1200);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(code).then(flashOk).catch(()=>_copyCodeFallback(code, flashOk));
  } else {
    _copyCodeFallback(code, flashOk);
  }
}
/* Respaldo para navegadores/contextos sin Clipboard API moderna (o que la
   bloquean por permisos): textarea oculta + document.execCommand('copy'). */
function _copyCodeFallback(code, onOk){
  try{
    const ta=document.createElement('textarea');
    ta.value=code;
    ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    onOk();
  }catch(e){ setSt('❌ No se pudo copiar el código: '+e.message); }
}

/* ──────────── Run ──────────── */
function runCode(){
  stopAuto(); steps=[]; cur=-1; prev=null; lastOut=''; selVar=null; _autoSelected=false;
  _objSnapshot={name:null, val:null}; _listViewMode='auto'; _lastRunError=null; _lastRunTruncated=false; _knownRagged=new Set();
  clearTimeout(_debTimer);
  const code=document.getElementById('codeInput').value;
  if(!code.trim()){ setSt('⚠ Escribe o pega código Python primero'); showBanner(false); setCodeView(false); return; }
  setSt('⏳ Analizando…');
  showBanner(false);
  _narLastLine=null;
  const _nb=document.getElementById('narrator');
  if(_nb){ _nb.className='narrator narrator-idle';
    document.getElementById('narIco').textContent='💡';
    document.getElementById('narTxt').textContent='Analizando el código…'; }
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  fetch('/prepare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code})})
  .then(r=>r.json()).then(d=>{
    // The backend always appends one final sentinel step (line:-1) even on
    // total failure, so `d.steps` is never truly empty — checking length===0
    // here never fired, silently hiding syntax errors / immediate crashes /
    // exec timeouts behind a misleading "✓ Programa terminado". A run with
    // zero REAL steps (nothing but that sentinel) is exactly as much of a
    // hard failure as an empty array.
    if(d.error && (!d.steps || d.steps.length<=1)){
      // hard failure before anything could be traced (syntax error, the
      // very first line already blew up, or the 12s exec timeout with no
      // progress) — stay editable so it can be fixed. d.truncated distingue
      // "tu código tiene un bug" (❌/🚨) de "el código sigue corriendo, solo
      // se cortó por seguridad" (⏱️) -- ninguna de las dos deja pasos que
      // recorrer aquí, pero el mensaje no debería sonar a que el código está
      // roto cuando en realidad ni siquiera tuvo tiempo de arrancar bien.
      setSt((d.truncated?'⏱️ ':'❌ ')+d.error);
      setCodeView(false);
      const eb=document.getElementById('narrator');
      if(eb){ eb.className=d.truncated?'narrator narrator-idle':'narrator nar-k-raise';
        document.getElementById('narIco').textContent=d.truncated?'⏱️':'🚨';
        document.getElementById('narTxt').textContent=d.error; }
      document.getElementById('pyHdrTxt').textContent=d.truncated?'Python 3 · Truncado':'Python 3 · Error';
      return;
    }
    steps=d.steps;
    relations=d.relations||{};
    explains=d.explains||{};
    _lastRunError=d.error||null;
    _lastRunTruncated=!!d.truncated;
    const n=steps.length-1;
    if(d.error){
      // partial trace: something failed mid-run, but keep whatever steps
      // were already recorded so the user can still step through them.
      // truncado (2000 pasos / 12s) no es un bug del alumno, así que usa un
      // ícono/tono distinto del de un error real a mitad de ejecución.
      setSt(`${d.truncated?'✂️':'⚠'} ${n} pasos (detenido) — ${d.error}`);
    } else {
      setSt(`✓ ${n} pasos — pulsa Forward › o Espacio`);
    }
    selVar=null; _lastObjName=null;
    setCodeView(true);      // switch the panel to the step-through view
    go(0);
    updBtns();
    // Flash the Forward button to guide the user
    const fwd=document.getElementById('bFwd');
    fwd.style.background='#1177bb';
    fwd.style.transform='scale(1.08)';
    setTimeout(()=>{ fwd.style.background=''; fwd.style.transform=''; }, 600);
  }).catch(e=>setSt('❌ '+e.message));
}

/* ──────────── Navigation ──────────── */
function goFirst(){ stopAuto(); if(!steps.length)return; prev=null; go(0); }
function goBack() { stopAuto(); if(cur>0){ prev=cur>1?steps[cur-2]:null; go(cur-1); } }
function goFwd()  { stopAuto(); if(cur<steps.length-1) go(cur+1); }
function goLast() {
  if(autoTmr){ stopAuto(); return; }
  if(!steps.length) return;
  stopAuto(); // also cancels a running loop-play, only one playback timer at a time
  document.getElementById('bLast').textContent='⏸ Pause';
  autoTmr=setInterval(()=>{
    if(cur>=steps.length-1){ stopAuto(); return; }
    go(cur+1);
    if(bps.has(steps[cur].line)){ stopAuto(); setSt(`⏸ Breakpoint — línea ${steps[cur].line}`); }
  }, 200);
}
/* ── Loop play: replays the whole trace start→end→start forever, so
   1D/2D/3D/4D data (lists, ndarrays) can be watched animating without
   manually clicking Forward. Ignores breakpoints — the point is a
   continuous animation, not a step-debug run. Speed is user-controlled
   (see #loopSpeed) rather than a fixed/auto-computed pace, so a trace with
   many small moves (e.g. a local-search optimizer) can be slowed down
   enough to actually watch each one. ── */
function _loopInterval(){
  const sel=document.getElementById('loopSpeed');
  return sel ? parseInt(sel.value,10) : 350;
}
function toggleLoop(){
  if(loopTmr){ stopAuto(); return; }
  if(!steps.length) return;
  stopAuto(); // also cancels a running "Last" autoplay
  const b=document.getElementById('bLoop');
  if(b){ b.textContent='⏸ Pausar'; b.classList.add('btn-looping'); }
  setSt('🔁 Reproduciendo animación en bucle — pulsa ⏸ Pausar para detener');
  loopTmr=setInterval(()=>{
    if(cur>=steps.length-1){ prev=null; go(0); return; }
    go(cur+1);
  }, _loopInterval());
}
/* Changing the speed dropdown while already looping restarts the timer at
   the new interval immediately, instead of waiting for the next toggle. */
function _onSpeedChange(){
  if(!loopTmr) return;
  clearInterval(loopTmr);
  loopTmr=setInterval(()=>{
    if(cur>=steps.length-1){ prev=null; go(0); return; }
    go(cur+1);
  }, _loopInterval());
}
function stopAuto(){
  clearInterval(autoTmr); autoTmr=null;
  document.getElementById('bLast').textContent='Last ⟫';
  clearInterval(loopTmr); loopTmr=null;
  const b=document.getElementById('bLoop');
  if(b){ b.textContent='🔁 Loop'; b.classList.remove('btn-looping'); }
}
/* Desplegable "🎓 Cursos" (barra de estudio): agrupa los botones de Modo
   Maestro para que la barra no crezca un botón por cada curso nuevo -- los
   propios botones (#bMaster, #bMasterAo, ...) no se tocan, solo se abren/
   cierran dentro de #cursosMenu, así que toggleMasterAo() y el resto siguen
   funcionando exactamente igual que antes. */
function _toggleCursosMenu(e){
  if(e) e.stopPropagation(); // si no, el listener de document de abajo lo cerraría en el mismo clic
  const m=document.getElementById('cursosMenu');
  if(!m) return;
  m.style.display = (m.style.display==='flex') ? 'none' : 'flex';
}
document.addEventListener('click', e=>{
  const menu=document.getElementById('cursosMenu');
  if(!menu || menu.style.display!=='flex') return;
  if(!menu.contains(e.target) && e.target.id!=='bCursosToggle') menu.style.display='none';
});

/* ──────────── Estadísticas de fallos por tema (los 3 Modos Maestro) ────────────
   Ponderar el repaso por cuánto fallaste, no solo mezclarlo al azar (Karpicke &
   Roediger 2008 + Dunlosky 2013: seguir testeando lo ya "sabido" importa, y lo
   que fallaste importa más). Clave NUEVA e independiente de los 3 progresos
   `done` existentes — no se toca su formato. Guardado en localStorage (no
   SQLite: la app es deliberadamente un solo archivo sin backend con estado, y
   este dato cabe igual de bien aquí que en una tabla). */
const MASTER_STATS_KEY='pyvizMasterStats';
let _stats={py:{}, ao:{}, math:{}, aoclassify:{}, aocompare:{}, racompare:{}, ascompare:{},
  aolimits:{}, ralimits:{}, aslimits:{}, ra:{}, as:{}, ns:{}, rn:{}, rf:{},
  nscompare:{}, rncompare:{}, rfcompare:{}, nslimits:{}, rnlimits:{}, rflimits:{}};
/* Migración única (2026-08-12): AO/RA/AS pasaron de "1 tema = 1 pregunta"
   (41/35/21 temas) a que cada pregunta sea su PROPIO tema (164/140/84) —
   los índices de tema ya no corresponden a los mismos temas de antes, así
   que las estadísticas Leitner viejas (guardadas con los índices
   anteriores) quedarían mintiendo sobre qué se sabe y qué no. Se limpia
   SOLO ao/ra/as (py/math no cambiaron su temario) una única vez, marcada
   con una bandera para no volver a correr en cargas futuras. Los
   progresos `done` (MASTER_AO_KEY/RA/AS en master-ao.js/ra.js/as.js) se
   resetean aparte, cambiando el nombre de esas claves. */
(function _migrateFlattenReset(){
  const FLAG='pyvizFlattenMigration20260812';
  try{
    if(localStorage.getItem(FLAG)) return;
    const raw=localStorage.getItem(MASTER_STATS_KEY);
    if(raw){
      const s=JSON.parse(raw);
      s.ao={}; s.ra={}; s.as={};
      localStorage.setItem(MASTER_STATS_KEY, JSON.stringify(s));
    }
    localStorage.setItem(FLAG, '1');
  }catch(e){}
})();
/* Repaso espaciado (Leitner, 5 cajas): acertar sube de caja (el próximo
   repaso se aleja); fallar vuelve a la caja 1 (se repasa mañana). Es la
   técnica de MÁS evidencia según Dunlosky 2013 ("distributed practice"),
   junto con el practice-testing que el Repaso mezclado ya hacía — hasta
   ahora solo se pesaba por nº de fallos, sin fechas (ver review.js). Vive
   en el mismo objeto que `_stats` (mismo localStorage, sin clave nueva):
   cada entrada gana los campos `box` (1-5) y `due` (epoch ms del próximo
   repaso). Una entrada sin `due` (nunca pasada por Leitner, incluida
   cualquiera guardada ANTES de este cambio) se trata como vencida (0 =
   siempre en el pasado), así queda disponible para repaso inmediato en
   vez de perderse. */
const LEITNER_INTERVALS_DAYS=[1,3,7,14,30]; // índice = caja-1
/* Dificultad adaptativa: a partir de esta caja (dominado, ≥2 aciertos
   seguidos), una pregunta mc pasa de reconocimiento (4 alternativas) a
   recuerdo libre real -- ver _quizRenderAnswerArea. La caja ya mide qué tan
   sólido está el ítem; hasta ahora esa señal solo decidía el intervalo
   `due`, nunca el esfuerzo de recuperación exigido (Rowland 2014;
   Carpenter & DeLosh 2006: recall > recognition en retención a largo
   plazo, pero conviene exigirlo solo cuando la base ya es sólida). */
const QUIZ_RECALL_BOX_THRESHOLD=4;
function _loadStats(){
  try{
    const raw=localStorage.getItem(MASTER_STATS_KEY);
    if(raw) _stats=JSON.parse(raw);
  }catch(e){ _stats={py:{}, ao:{}, math:{}}; }
  if(!_stats.py) _stats.py={};
  if(!_stats.ao) _stats.ao={};
  if(!_stats.math) _stats.math={};
  if(!_stats.aoclassify) _stats.aoclassify={};
  if(!_stats.aocompare) _stats.aocompare={};
  if(!_stats.racompare) _stats.racompare={};
  if(!_stats.ascompare) _stats.ascompare={};
  if(!_stats.aolimits) _stats.aolimits={};
  if(!_stats.ralimits) _stats.ralimits={};
  if(!_stats.aslimits) _stats.aslimits={};
  if(!_stats.ra) _stats.ra={};
  if(!_stats.as) _stats.as={};
  if(!_stats.ns) _stats.ns={};
  if(!_stats.rn) _stats.rn={};
  if(!_stats.rf) _stats.rf={};
  if(!_stats.nscompare) _stats.nscompare={};
  if(!_stats.rncompare) _stats.rncompare={};
  if(!_stats.rfcompare) _stats.rfcompare={};
  if(!_stats.nslimits) _stats.nslimits={};
  if(!_stats.rnlimits) _stats.rnlimits={};
  if(!_stats.rflimits) _stats.rflimits={};
}
function _saveStats(){
  try{ localStorage.setItem(MASTER_STATS_KEY, JSON.stringify(_stats)); }catch(e){}
}
/* Nombre real del tema para el espejo en SQLite (stats_store.py) — solo
   AO/RA/AS entran al reporte (mismo alcance que Autoexplícate/confianza/
   "No sé"), resuelto en tiempo de llamada porque core.js carga ANTES que
   master-ao.js/ra.js/as.js. */
function _reportTopicName(mode, idx){
  if(mode==='ao') return (typeof EX_AO!=='undefined' && EX_AO[idx]) ? EX_AO[idx].name : null;
  if(mode==='ra') return (typeof EX_RA!=='undefined' && EX_RA[idx]) ? EX_RA[idx].name : null;
  if(mode==='as') return (typeof EX_AS!=='undefined' && EX_AS[idx]) ? EX_AS[idx].name : null;
  if(mode==='ns') return (typeof EX_NS!=='undefined' && EX_NS[idx]) ? EX_NS[idx].name : null;
  if(mode==='rn') return (typeof EX_RN!=='undefined' && EX_RN[idx]) ? EX_RN[idx].name : null;
  if(mode==='rf') return (typeof EX_RF!=='undefined' && EX_RF[idx]) ? EX_RF[idx].name : null;
  return null;
}
/* ──────────── Modo enfocado: refuerzo guiado de un bloque débil ────────────
   A diferencia de simplemente filtrar Repaso mezclado (mecanismo de quiz
   redirigido), esto navega el Modo Maestro REAL del curso -- teoría,
   Visualízalo, Aplicación real, código real, quiz, Autoexplícate, todo
   igual que siempre -- pero SOLO por los temas de un bloque débil detectado
   (ver _reportWeaknessClusters en report.js), en vez de todo el temario, y
   con un prompt de recuperación activa antes de cada tema. Aplica el
   protocolo de aprendizaje del usuario (recordar->comprender->aplicar->
   explicar->reflexionar) en vez de solo redirigir el mecanismo de quiz. */
let _focusMode=null, _focusTopicIdxs=[], _focusListPos=0, _focusLabel='';

function _focusCurrentIdx(mode){
  if(mode==='ao') return typeof _aoPos!=='undefined' ? _aoPos : null;
  if(mode==='ra') return typeof _raPos!=='undefined' ? _raPos : null;
  if(mode==='as') return typeof _asPos!=='undefined' ? _asPos : null;
  if(mode==='ns') return typeof _nsPos!=='undefined' ? _nsPos : null;
  if(mode==='rn') return typeof _rnPos!=='undefined' ? _rnPos : null;
  if(mode==='rf') return typeof _rfPos!=='undefined' ? _rfPos : null;
  return null;
}
function _focusGoTo(mode, idx){
  const fn={ao:'_aoGoTo', ra:'_raGoTo', as:'_asGoTo', ns:'_nsGoTo', rn:'_rnGoTo', rf:'_rfGoTo'}[mode];
  if(fn && typeof window[fn]==='function') window[fn](idx);
}
function _focusOpenMaster(mode){
  const fn={ao:'toggleMasterAo', ra:'toggleMasterRa', as:'toggleMasterAs',
    ns:'toggleMasterNs', rn:'toggleMasterRn', rf:'toggleMasterRf'}[mode];
  if(fn && typeof window[fn]==='function') window[fn]();
}
/* Se llama desde el Reporte al pulsar "Reforzar este bloque". */
function _focusStart(mode, topicIdxs, label){
  if(!topicIdxs || !topicIdxs.length) return;
  _focusMode=mode; _focusTopicIdxs=topicIdxs.slice(); _focusListPos=0; _focusLabel=label;
  _focusOpenMaster(mode);
  _focusGoTo(mode, _focusTopicIdxs[0]);
}
function _focusExit(){
  _focusMode=null; _focusTopicIdxs=[]; _focusListPos=0; _focusLabel='';
  ['ao','ra','as','ns','rn','rf'].forEach(_focusRenderRecallPrompt);
}
/* Llamado desde aoNext()/raNext()/asNext() EN VEZ de avanzar +1 al temario
   completo, cuando el modo enfocado está activo para ese curso. */
function _focusAdvance(mode){
  if(_focusListPos>=_focusTopicIdxs.length-1){ _focusFinish(); return; }
  _focusListPos++;
  _focusGoTo(mode, _focusTopicIdxs[_focusListPos]);
}
function _focusFinish(){
  const label=_focusLabel, mode=_focusMode;
  const ids={ao:'aoFocusBanner', ra:'raFocusBanner', as:'asFocusBanner'};
  const el=mode?document.getElementById(ids[mode]):null;
  if(el) el.innerHTML='✅ Terminaste de reforzar "'+esc(label)+'" — revisa tu 📓 Cuaderno de errores para lo que siga flojo. '+
    '<button class="master-btn" onclick="_focusExit()">Cerrar</button>';
  _focusMode=null; _focusTopicIdxs=[]; _focusListPos=0; _focusLabel='';
}
/* Pinta el prompt de recuerdo + el banner de progreso -- llamado junto a
   _xxRenderTheory() en cada _xxGoTo, para los 3 cursos. Sin bloquear nada:
   el bloque de teoría sigue ahí debajo, esto solo invita a pensar primero
   (mismo espíritu sin-fricción que Autoexplícate). */
function _focusRenderRecallPrompt(mode){
  const ids={
    ao:{recall:'aoFocusRecallBlock', text:'aoFocusRecallText', banner:'aoFocusBanner'},
    ra:{recall:'raFocusRecallBlock', text:'raFocusRecallText', banner:'raFocusBanner'},
    as:{recall:'asFocusRecallBlock', text:'asFocusRecallText', banner:'asFocusBanner'},
  }[mode];
  if(!ids) return;
  const recallEl=document.getElementById(ids.recall);
  const bannerEl=document.getElementById(ids.banner);
  if(_focusMode!==mode){
    if(recallEl) recallEl.style.display='none';
    if(bannerEl) bannerEl.style.display='none';
    return;
  }
  const idx=_focusCurrentIdx(mode);
  const topicName=_reportTopicName(mode, idx) || '';
  if(recallEl){
    recallEl.style.display='block';
    const textEl=document.getElementById(ids.text);
    if(textEl) textEl.textContent='¿Qué es y por qué funciona "'+topicName+'"? Intenta explicarlo de memoria antes de seguir.';
    const ta=recallEl.querySelector('textarea');
    if(ta) ta.value='';
  }
  if(bannerEl){
    bannerEl.style.display='inline-flex';
    bannerEl.innerHTML='🎯 Refuerzo: '+esc(_focusLabel)+' ('+(_focusListPos+1)+'/'+_focusTopicIdxs.length+')'+
      ' <button class="master-btn master-btn-exit" onclick="_focusExit()" title="Salir del refuerzo, volver al temario completo">✕</button>';
  }
}
function _focusDismissRecall(mode){
  const ids={ao:'aoFocusRecallBlock', ra:'raFocusRecallBlock', as:'asFocusRecallBlock'};
  const el=document.getElementById(ids[mode]);
  if(el) el.style.display='none';
}

/* Espejo en SQLite del evento que ya se guardó en localStorage — silencioso
   y en segundo plano (fire-and-forget): si el servidor no responde o el
   usuario está offline, el estudio sigue igual, localStorage sigue siendo
   la fuente de verdad para la app EN VIVO. El espejo solo alimenta el
   reporte visual (report.js) y queda disponible para consulta futura. */
function _mirrorAttemptToServer(mode, idx, result, box, dueMs){
  const topicName=_reportTopicName(mode, idx);
  if(!topicName) return; // fuera de alcance (py/math/aoclassify) o índice desconocido
  try{
    fetch('/record_attempt',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({mode, topic_idx:idx, topic_name:topicName, result, box, due_at:new Date(dueMs).toISOString()})}).catch(()=>{});
  }catch(e){}
}
function _mirrorConfidenceToServer(mode, idx, level, box, dueMs){
  if(!_reportTopicName(mode, idx)) return;
  try{
    fetch('/record_confidence',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({mode, topic_idx:idx, level, box, due_at:new Date(dueMs).toISOString()})}).catch(()=>{});
  }catch(e){}
}
function _mirrorReasoningToServer(mode, idx, doubtedOption, reasonTag){
  if(!_reportTopicName(mode, idx)) return;
  try{
    fetch('/record_reasoning',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({mode, topic_idx:idx, doubted_option:doubtedOption, reason_tag:reasonTag})}).catch(()=>{});
  }catch(e){}
}
/* Cuaderno de errores (plan de aprendizaje personal, sección 8): cada fallo
   real en una pregunta mc con whyNot queda registrado solo, sin fricción
   para el alumno -- la reflexión (regla personal) se hace despues, con
   calma, desde el panel "Cuaderno de errores", no en caliente durante el
   estudio. Mismo patron fire-and-forget que _mirrorAttemptToServer. */
function _logErrorJournal(mode, idx, topicName, question, chosenText, correctText, whyWrong){
  if(!whyWrong) return;
  try{
    fetch('/save_error',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({mode, topic_idx:idx, topic_name:topicName, question, chosen_text:chosenText, correct_text:correctText, why_wrong:whyWrong})}).catch(()=>{});
  }catch(e){}
}
function _recordAttempt(mode, idx, success, opts){
  _loadStats();
  const bucket=_stats[mode];
  const cur=bucket[idx] || {attempts:0, fails:0, dontKnow:0, box:1, due:0};
  cur.attempts+=1;
  let result;
  if(opts && opts.dontKnow){ cur.dontKnow=(cur.dontKnow||0)+1; cur.box=1; result='dont_know'; } // "No sé": a caja 1, sin contar como fallo
  else if(!success){ cur.fails+=1; cur.box=1; result='incorrect'; }           // vuelve a la caja 1
  else{ cur.box=Math.min((cur.box||1)+1, LEITNER_INTERVALS_DAYS.length); result='correct'; } // sube de caja
  const days=LEITNER_INTERVALS_DAYS[cur.box-1];
  cur.due=Date.now()+days*86400000;
  bucket[idx]=cur;
  _saveStats();
  _mirrorAttemptToServer(mode, idx, result, cur.box, cur.due);
}
/* Ajusta la caja Leitner ya calculada por _recordAttempt según cuánta
   confianza real tenías al acertar (Dunlosky 2013, calibración
   metacognitiva) — se llama SOLO tras un acierto, nunca tras un fallo o
   un "No sé" (esos ya fuerzan caja 1 por su cuenta). 'sure' deja el avance
   normal; 'unsure' retrocede un nivel (repaso más próximo que un acierto
   pleno); 'guess' fuerza caja 1, igual que si hubieras fallado — acertar
   adivinando no es saber. */
function _recordConfidence(mode, idx, level){
  _loadStats();
  const bucket=_stats[mode];
  const cur=bucket[idx];
  if(!cur) return;
  // Se guarda el nivel elegido (no solo su efecto en la caja) para poder
  // consultar después "¿en qué temas dudé aunque acerté?" — sin esto, un
  // 'unsure' era indistinguible de cualquier otro motivo de retroceso de
  // caja una vez guardado.
  if(level==='guess'){ cur.box=1; cur.guessCount=(cur.guessCount||0)+1; }
  else if(level==='unsure'){ cur.box=Math.max(1, (cur.box||1)-1); cur.unsureCount=(cur.unsureCount||0)+1; }
  else if(level==='sure'){ cur.sureCount=(cur.sureCount||0)+1; } // no se toca la caja, ya quedó bien tras _recordAttempt
  const days=LEITNER_INTERVALS_DAYS[cur.box-1];
  cur.due=Date.now()+days*86400000;
  bucket[idx]=cur;
  _saveStats();
  _mirrorConfidenceToServer(mode, idx, level, cur.box, cur.due);
}
function _statsFor(mode, idx){
  _loadStats();
  const s=_stats[mode][idx];
  if(!s) return {attempts:0, fails:0, dontKnow:0, box:1, due:0};
  // migración perezosa: estadísticas guardadas antes de que existiera Leitner/dontKnow
  if(s.box===undefined) s.box=1;
  if(s.due===undefined) s.due=0;
  if(s.dontKnow===undefined) s.dontKnow=0;
  return s;
}
/* Badges visibles en los 4 checklists para ver de un vistazo dónde vienes
   fallando o dónde de verdad no sabías (distinto de fallar: ver plan de
   "No sé" en la conversación), sin necesidad de entrar al Repaso mezclado. */
function _failsBadge(mode, idx){
  const f=_statsFor(mode, idx).fails;
  return f>0 ? `<span class="master-item-fails">⚠️ ${f}x</span>` : '';
}
function _dontKnowBadge(mode, idx){
  const d=_statsFor(mode, idx).dontKnow;
  return d>0 ? `<span class="master-item-dontknow">🤷 ${d}x</span>` : '';
}

/* Baraja las alternativas de una pregunta de opción múltiple cada vez que
   se renderiza. Se detectó (2026-08-10, reporte del usuario: "las
   correctas siempre estaban en la primera posición") que el autor de las
   preguntas puso casi siempre la respuesta correcta primero al escribir
   cada AO_QUIZ/RA_QUIZ/AS_QUIZ: RA y AS tenían el 100% en la posición 'a',
   AO el 68% — un alumno podía acertar sin saber nada, solo pulsando
   siempre la primera opción. Fisher-Yates; NO modifica el array original
   de la pregunta, solo el orden en que se muestra esta vez. */
function _shuffleMcOptions(q){
  const order=q.options.map((_,i)=>i);
  for(let i=order.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [order[i],order[j]]=[order[j],order[i]];
  }
  // `order` se devuelve tambien para poder traducir el indice MOSTRADO
  // (tras barajar) de vuelta al indice ORIGINAL de q.options/q.whyNot al
  // comprobar la respuesta -- ver _aoCheckQuizAnswer y equivalentes.
  return {options: order.map(i=>q.options[i]), correct: order.indexOf(q.correct), order};
}

/* AO_QUIZ/RA_QUIZ/AS_QUIZ pasaron de "1 pregunta por tema" a "banco de
   varias preguntas por tema" (2026-08-11, petición del usuario tras
   completar el plan de AO: quiere repasar cada tema con más profundidad,
   una pregunta al azar del banco cada vez que entra). bankArr[idx] es
   ahora un array de objetos-pregunta en vez de un objeto-pregunta suelto;
   esta función elige uno al azar. Debe llamarse UNA sola vez por
   renderizado y el resultado guardarse (no volver a llamarla al comprobar
   la respuesta), o la pregunta mostrada y la comprobada podrían no
   coincidir. */
function _quizPickOne(bankArr, idx){
  const bank=bankArr[idx];
  return bank[Math.floor(Math.random()*bank.length)];
}

/* "No sé / no contesto" + confianza al acertar: UNA sola implementación
   genérica reusada por los 4 quizzes (AO/RA/AS/Repaso mezclado) en vez de
   4 copias — el HTML/JS de cada modo ya es idéntico salvo el prefijo de
   ids, así que aquí solo se parametriza eso. `prefix` es 'ao'|'ra'|'as'|
   'review'. Las funciones _xxShowQuizSolution/_aoPos/_reviewItem/etc. se
   resuelven en tiempo de CLIC (no al cargar core.js, que va primero) —
   por eso todo acceso a ellas vive dentro del cuerpo de una función, nunca
   en el nivel superior del archivo. */
function _quizIds(prefix){
  const q = prefix==='review' ? '' : 'Quiz'; // ids viejos: ao/ra/as llevan "Quiz", review no
  return {
    options: prefix+q+'Options',
    numericInput: prefix+q+'NumericInput',
    numericWrap: prefix+q+'NumericWrap',
    feedback: prefix+q+'Feedback',
    solutionBtn: prefix+q+'SolutionBtn',
    dontKnowBtn: prefix+'QuizDontKnow',       // elementos NUEVOS: mismo esquema en los 4
    confidenceWrap: prefix+'QuizConfidence',
    reasonWrap: prefix+'QuizReason',
    copyBtn: prefix+q+'CopyBtn',
  };
}
/* Copia la pregunta COMPLETA (tema + código real + enunciado + opciones)
   al portapapeles, para pegarla en otra IA y pedirle una explicación --
   a diferencia de copyCode() (solo el código del editor), esto arma un
   bloque de texto autocontenido con todo el contexto de la pregunta.
   Reusa _copyCodeFallback ya que solo necesita un texto + callback. */
function _quizCopyQuestion(prefix){
  const mi=_quizCurrentModeIdx(prefix);
  if(!mi) return;
  let code=null, q=null;
  if(prefix==='ao'){ code=EX_AO[_aoPos].code; q=_aoCurrentQuiz; }
  else if(prefix==='ra'){ code=EX_RA[_raPos].code; q=_raCurrentQuiz; }
  else if(prefix==='as'){ code=EX_AS[_asPos].code; q=_asCurrentQuiz; }
  else if(prefix==='ns'){ code=EX_NS[_nsPos].code; q=_nsCurrentQuiz; }
  else if(prefix==='rn'){ code=EX_RN[_rnPos].code; q=_rnCurrentQuiz; }
  else if(prefix==='rf'){ code=EX_RF[_rfPos].code; q=_rfCurrentQuiz; }
  else if(prefix==='review'){ code=_reviewCodeSource(_reviewItem); q=_reviewCurrentSrc; }
  if(!q) return;
  const topicName=_reportTopicName(mi.mode, mi.idx);
  let text='TEMA: '+(topicName||'')+'\n\n';
  if(code) text+='CÓDIGO:\n'+code+'\n\n';
  text+='PREGUNTA:\n'+q.question;
  if(q.type==='mc' && q.options){
    text+='\n\nOPCIONES:\n'+q.options.map((o,i)=>String.fromCharCode(97+i)+') '+o).join('\n');
  } else {
    text+='\n\n(Respuesta numérica'+(q.decimals?', '+q.decimals+' decimales':'')+')';
  }
  const ids=_quizIds(prefix);
  const btn=document.getElementById(ids.copyBtn);
  const flashOk=()=>{
    if(!btn) return;
    const prev=btn.textContent;
    btn.textContent='✅ Copiado';
    btn.classList.add('copy-btn-ok');
    setTimeout(()=>{ btn.textContent=prev; btn.classList.remove('copy-btn-ok'); }, 1200);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(flashOk).catch(()=>_copyCodeFallback(text, flashOk));
  } else {
    _copyCodeFallback(text, flashOk);
  }
}
function _quizCurrentModeIdx(prefix){
  if(prefix==='ao') return (typeof _aoPos!=='undefined') ? {mode:'ao', idx:_aoPos} : null;
  if(prefix==='ra') return (typeof _raPos!=='undefined') ? {mode:'ra', idx:_raPos} : null;
  if(prefix==='as') return (typeof _asPos!=='undefined') ? {mode:'as', idx:_asPos} : null;
  if(prefix==='ns') return (typeof _nsPos!=='undefined') ? {mode:'ns', idx:_nsPos} : null;
  if(prefix==='rn') return (typeof _rnPos!=='undefined') ? {mode:'rn', idx:_rnPos} : null;
  if(prefix==='rf') return (typeof _rfPos!=='undefined') ? {mode:'rf', idx:_rfPos} : null;
  if(prefix==='review') return (typeof _reviewItem!=='undefined' && _reviewItem) ? {mode:_reviewItem.mode, idx:_reviewItem.idx} : null;
  return null;
}
function _quizMarkAnswered(prefix){
  if(prefix==='ao') _aoQuizAnswered=true;
  else if(prefix==='ra') _raQuizAnswered=true;
  else if(prefix==='as') _asQuizAnswered=true;
  else if(prefix==='ns') _nsQuizAnswered=true;
  else if(prefix==='rn') _rnQuizAnswered=true;
  else if(prefix==='rf') _rfQuizAnswered=true;
  else if(prefix==='review') _reviewAnswered=true;
}
function _quizIsAnswered(prefix){
  if(prefix==='ao') return typeof _aoQuizAnswered!=='undefined' && _aoQuizAnswered;
  if(prefix==='ra') return typeof _raQuizAnswered!=='undefined' && _raQuizAnswered;
  if(prefix==='as') return typeof _asQuizAnswered!=='undefined' && _asQuizAnswered;
  if(prefix==='ns') return typeof _nsQuizAnswered!=='undefined' && _nsQuizAnswered;
  if(prefix==='rn') return typeof _rnQuizAnswered!=='undefined' && _rnQuizAnswered;
  if(prefix==='rf') return typeof _rfQuizAnswered!=='undefined' && _rfQuizAnswered;
  if(prefix==='review') return typeof _reviewAnswered!=='undefined' && _reviewAnswered;
  return false;
}
function _quizCallShowSolution(prefix){
  const fnName={ao:'_aoShowQuizSolution', ra:'_raShowQuizSolution', as:'_asShowQuizSolution',
    ns:'_nsShowQuizSolution', rn:'_rnShowQuizSolution', rf:'_rfShowQuizSolution', review:'_reviewShowSolution'}[prefix];
  if(fnName && typeof window[fnName]==='function') window[fnName]();
}
/* Al pulsar "🤷 No sé": revela la solución al instante (como rendirse, no
   como fallar dos veces intentando) y manda el tema a caja 1 de Leitner
   SIN sumar a "fallos" — el checklist lo cuenta aparte (🤷 badge) porque
   "no supe" y "me equivoqué creyendo que sabía" son señales distintas. */
function _quizDontKnowClick(prefix){
  if(_quizIsAnswered(prefix)) return;
  const mi=_quizCurrentModeIdx(prefix);
  if(!mi) return;
  _quizMarkAnswered(prefix);
  const ids=_quizIds(prefix);
  document.querySelectorAll('#'+ids.options+' .math-option').forEach(btn=>{ btn.disabled=true; });
  const numInput=document.getElementById(ids.numericInput);
  if(numInput) numInput.disabled=true;
  const dkBtn=document.getElementById(ids.dontKnowBtn);
  if(dkBtn) dkBtn.disabled=true;
  _recordAttempt(mi.mode, mi.idx, false, {dontKnow:true});
  const fb=document.getElementById(ids.feedback);
  if(fb){
    fb.style.display='block';
    fb.className='math-feedback math-feedback-bad';
    fb.textContent='🤷 Caja 1 — aquí está la explicación. Este tema vuelve a aparecer mañana en tu repaso.';
  }
  const solBtn=document.getElementById(ids.solutionBtn);
  if(solBtn) solBtn.style.display='inline-block';
  _quizCallShowSolution(prefix);
  if(prefix==='review'){
    const nextBtn=document.getElementById('reviewNextBtn');
    if(nextBtn) nextBtn.style.display='inline-block';
  }
}
/* Tras un ACIERTO real (nunca tras un fallo ni un "No sé", que ya fuerzan
   caja 1 por su cuenta): pregunta cuánta confianza había, para que Leitner
   distinga un acierto sólido de uno adivinado (Dunlosky 2013, calibración
   metacognitiva — ver conversación para el porqué completo). */
function _quizRenderConfidencePrompt(prefix){
  const ids=_quizIds(prefix);
  const wrap=document.getElementById(ids.confidenceWrap);
  if(!wrap) return;
  wrap.style.display='flex';
  wrap.innerHTML=
    '<span class="quiz-confidence-label">¿Qué tan seguro estabas de esta respuesta?</span>'+
    `<button class="quiz-confidence-btn quiz-confidence-sure" onclick="_quizConfidenceClick('${prefix}','sure')">😎 Seguro</button>`+
    `<button class="quiz-confidence-btn quiz-confidence-unsure" onclick="_quizConfidenceClick('${prefix}','unsure')">🤔 Dudaba</button>`+
    `<button class="quiz-confidence-btn quiz-confidence-guess" onclick="_quizConfidenceClick('${prefix}','guess')">🎲 Adiviné</button>`;
  const dkBtn=document.getElementById(ids.dontKnowBtn);
  if(dkBtn) dkBtn.disabled=true; // ya acertaste, "No sé" ya no aplica a esta pregunta
}
function _quizConfidenceClick(prefix, level){
  const mi=_quizCurrentModeIdx(prefix);
  if(!mi) return;
  _recordConfidence(mi.mode, mi.idx, level);
  const ids=_quizIds(prefix);
  const wrap=document.getElementById(ids.confidenceWrap);
  if(wrap) wrap.innerHTML='<span class="quiz-confidence-done">✓ Registrado — Leitner ya lo tuvo en cuenta.</span>';
}
/* Captura de razonamiento por botones (sin texto libre), en TODAS las
   preguntas mc de los 3 Modos Maestro + Repaso mezclado: 2 clics, qué otra
   opción dudó y por qué eligió la suya -- se guarda en SQLite (attempts)
   para que /analyze_patterns pueda diagnosticar un patrón real de
   confusión más adelante, no una pregunta suelta. No bloquea el flujo:
   aparece junto al feedback ya existente, ignorarlo no rompe nada. */
let _quizReasonDoubted=null;
const QUIZ_REASON_TAGS=[
  {tag:'theory', label:'📖 Lo sabía por la teoría'},
  {tag:'elimination', label:'🔍 Descarté por eliminación'},
  {tag:'doubt_two', label:'🤔 Dudé entre esta y otra'},
  {tag:'guess', label:'🎲 Adiviné'},
  {tag:'confused', label:'🔀 Confundí este concepto con el de la opción que dudé'},
];
function _quizRenderReasonPrompt(prefix, otherOptionTexts){
  const ids=_quizIds(prefix);
  const wrap=document.getElementById(ids.reasonWrap);
  if(!wrap) return;
  _quizReasonDoubted=null;
  wrap.style.display='flex';
  let html='<span class="quiz-confidence-label">¿Había otra opción que dudaste?</span>';
  (otherOptionTexts||[]).forEach(t=>{
    const short=t.length>60 ? t.slice(0,57)+'…' : t;
    html+=`<button class="quiz-confidence-btn quiz-reason-btn" onclick="_quizReasonDoubtClick('${prefix}', ${JSON.stringify(t).replace(/'/g,"\\'")})" title="${esc(t)}">🤔 ${esc(short)}</button>`;
  });
  html+=`<button class="quiz-confidence-btn" onclick="_quizReasonDoubtClick('${prefix}', null)">Ninguna, estaba seguro</button>`;
  wrap.innerHTML=html;
}
function _quizReasonDoubtClick(prefix, doubtedText){
  _quizReasonDoubted=doubtedText;
  _quizRenderReasonTags(prefix);
}
function _quizRenderReasonTags(prefix){
  const ids=_quizIds(prefix);
  const wrap=document.getElementById(ids.reasonWrap);
  if(!wrap) return;
  let html='<span class="quiz-confidence-label">¿Por qué elegiste esa opción?</span>';
  QUIZ_REASON_TAGS.forEach(rt=>{
    html+=`<button class="quiz-confidence-btn quiz-reason-btn" onclick="_quizReasonTagClick('${prefix}','${rt.tag}')">${rt.label}</button>`;
  });
  wrap.innerHTML=html;
}
function _quizReasonTagClick(prefix, tag){
  const mi=_quizCurrentModeIdx(prefix);
  if(!mi) return;
  _mirrorReasoningToServer(mi.mode, mi.idx, _quizReasonDoubted, tag);
  const ids=_quizIds(prefix);
  const wrap=document.getElementById(ids.reasonWrap);
  if(wrap) wrap.innerHTML='<span class="quiz-confidence-done">✓ Registrado — ayuda a detectar patrones de confusión.</span>';
  _quizReasonDoubted=null;
}
/* Llamado al renderizar una pregunta nueva (_xxRenderQuiz/_reviewNext):
   reactiva el botón "No sé" y oculta cualquier prompt de confianza que
   hubiera quedado de la pregunta anterior. */
function _quizResetExtras(prefix){
  const ids=_quizIds(prefix);
  const dkBtn=document.getElementById(ids.dontKnowBtn);
  if(dkBtn){ dkBtn.disabled=false; dkBtn.style.display='inline-block'; }
  const wrap=document.getElementById(ids.confidenceWrap);
  if(wrap){ wrap.style.display='none'; wrap.innerHTML=''; }
  const reasonWrap=document.getElementById(ids.reasonWrap);
  if(reasonWrap){ reasonWrap.style.display='none'; reasonWrap.innerHTML=''; }
  _quizReasonDoubted=null;
}

/* Pregunta mc actual de cada modo -- mismo mapeo por prefix que
   _quizCurrentModeIdx, pero devolviendo el OBJETO pregunta en vez del
   mode/idx del tema (lo necesitan _quizRenderAnswerArea/_quizRevealFreeRecall
   para leer q.options/q.correct/q.solution). No se reusa dentro de
   _quizCopyQuestion (que ya tenía su propio switch idéntico) para no tocar
   una función existente que ya funciona, fuera del alcance de este cambio. */
function _quizCurrentQuestion(prefix){
  if(prefix==='ao') return (typeof _aoCurrentQuiz!=='undefined') ? _aoCurrentQuiz : null;
  if(prefix==='ra') return (typeof _raCurrentQuiz!=='undefined') ? _raCurrentQuiz : null;
  if(prefix==='as') return (typeof _asCurrentQuiz!=='undefined') ? _asCurrentQuiz : null;
  if(prefix==='ns') return (typeof _nsCurrentQuiz!=='undefined') ? _nsCurrentQuiz : null;
  if(prefix==='rn') return (typeof _rnCurrentQuiz!=='undefined') ? _rnCurrentQuiz : null;
  if(prefix==='rf') return (typeof _rfCurrentQuiz!=='undefined') ? _rfCurrentQuiz : null;
  if(prefix==='review') return (typeof _reviewCurrentSrc!=='undefined') ? _reviewCurrentSrc : null;
  return null;
}
/* Id del botón "siguiente pregunta del banco" (distinto de reviewNextBtn,
   que avanza de TEMA, no de pregunta dentro del mismo tema) y si de verdad
   queda otra pregunta en el banco de este tema -- mismo patrón bank[[pos]
   ya usado en cada _xxCheckQuizAnswer (AO_QUIZ[_aoPos].length-1, etc.),
   centralizado aquí para que _quizFreeRecallResult pueda decidir si
   mostrarlo sin duplicar este chequeo una vez más por modo. */
function _quizNextBtnId(prefix){
  return {ao:'aoQuizNextBtn', ra:'raQuizNextBtn', as:'asQuizNextBtn',
    ns:'nsQuizNextBtn', rn:'rnQuizNextBtn', rf:'rfQuizNextBtn', review:'reviewNextBtn'}[prefix];
}
function _quizHasMoreInBank(prefix){
  try{
    if(prefix==='ao') return _aoQuizSubPos<AO_QUIZ[_aoPos].length-1;
    if(prefix==='ra') return _raQuizSubPos<RA_QUIZ[_raPos].length-1;
    if(prefix==='as') return _asQuizSubPos<AS_QUIZ[_asPos].length-1;
    if(prefix==='ns') return _nsQuizSubPos<NS_QUIZ[_nsPos].length-1;
    if(prefix==='rn') return _rnQuizSubPos<RN_QUIZ[_rnPos].length-1;
    if(prefix==='rf') return _rfQuizSubPos<RF_QUIZ[_rfPos].length-1;
  }catch(e){ return false; } // variables/bancos aún no definidos en este modo
  return false; // 'review' no tiene "siguiente del mismo banco": cada pregunta es un tema distinto
}

/* Entrada inductiva: la teoría de un tema queda bloqueada SOLO la primera
   vez que se llega a él (_statsFor(mode,idx).attempts===0) -- el alumno
   intenta la pregunta del quiz a ciegas antes de leer la explicación
   (generación, ver "Make It Stick" cap. 2/4: intentar responder antes de
   que te enseñen deja una huella de memoria más fuerte que leer la
   explicación primero). En cuanto responde una vez (acierte o falle, lo
   que cuenta es el intento) attempts pasa a ser >=1 y la teoría se
   desbloquea para siempre en ese tema -- no se vuelve a bloquear en
   repasos futuros, para no ser molesto cada vez que se repite un tema ya
   visto. Un link de escape ("ya sé, mostrame la teoría igual") respeta la
   autonomía: la ayuda está disponible si se pide, no se impone. */
function _theoryIsLocked(prefix, mode, idx){
  if(window['_'+prefix+'TheoryForceUnlock_'+idx]) return false;
  return _statsFor(mode, idx).attempts===0;
}
function _theoryUnlockNow(prefix, idx, renderFn){
  window['_'+prefix+'TheoryForceUnlock_'+idx]=true;
  if(typeof window[renderFn]==='function') window[renderFn]();
}
function _theoryGateHtml(prefix, idx, renderFn){
  return '<div class="theory-locked-box">'+
    '<div class="theory-locked-title">🎯 Antes de la teoría</div>'+
    '<p>Respondé la pregunta de abajo, aunque no estés seguro. El objetivo es que tu cerebro intente predecir antes de que se lo expliquen — así se ancla mejor. Fallar acá es información, no una medida de tu capacidad.</p>'+
    `<button class="theory-locked-unlock-btn" onclick="_theoryUnlockNow('${prefix}', ${idx}, '${renderFn}')">Ya sé, mostrame la teoría igual</button>`+
    '</div>';
}
/* Dificultad adaptativa (ver QUIZ_RECALL_BOX_THRESHOLD arriba): sustituye
   el bloque de generar los botones .math-option, que hasta ahora vivía
   duplicado casi literal en cada _xxRenderQuiz/_reviewNext. SOLO se llama
   cuando q.type==='mc' (las preguntas numéricas quedan fuera de este
   cambio, su rama no se toca). Devuelve {shuffled} para que el caller siga
   fijando su propia variable _xxQuizShuffledCorrect/_xxQuizOrder (esas son
   `let` de módulo, no propiedades de window, así que no se pueden fijar
   desde aquí) -- shuffled es null en el tier de recuerdo libre, ya que ahí
   no hay índice de opción que comprobar. */
function _quizRenderAnswerArea(prefix, mode, idx, q){
  const ids=_quizIds(prefix);
  const optWrap=document.getElementById(ids.options);
  const box=_statsFor(mode, idx).box;
  if(box>=QUIZ_RECALL_BOX_THRESHOLD){
    optWrap.style.display='block';
    optWrap.innerHTML=
      '<div class="quiz-recall-block">'+
      '<div class="quiz-recall-label">🧠 Ya dominas este tema — escribe tu respuesta de memoria antes de revelarla:</div>'+
      '<textarea class="quiz-recall-textarea" id="'+ids.options+'Textarea" placeholder="Escribe tu respuesta aquí..."></textarea>'+
      `<button class="self-explain-ai-btn" onclick="_quizRevealFreeRecall('${prefix}')">Ver respuesta</button>`+
      '</div>';
    return {shuffled:null};
  }
  optWrap.style.display='grid';
  const checkFn={ao:'_aoCheckQuizAnswer', ra:'_raCheckQuizAnswer', as:'_asCheckQuizAnswer',
    ns:'_nsCheckQuizAnswer', rn:'_rnCheckQuizAnswer', rf:'_rfCheckQuizAnswer', review:'_reviewCheckAnswer'}[prefix];
  const shuffled=_shuffleMcOptions(q);
  optWrap.innerHTML=shuffled.options.map((o,i)=>
    `<button class="math-option" onclick="${checkFn}(${i})">${String.fromCharCode(97+i)}) ${o}</button>`).join('');
  return {shuffled};
}
/* Botón "Ver respuesta" del bloque de recuerdo libre: revela la respuesta
   sin comparar contra lo escrito (mismo criterio "sin veredicto automático
   de IA" que Autoexplícate/reflexión de sesión -- el alumno se autoevalúa),
   y ofrece los 2 botones de autocalificación. */
function _quizRevealFreeRecall(prefix){
  const ids=_quizIds(prefix);
  const q=_quizCurrentQuestion(prefix);
  const optWrap=document.getElementById(ids.options);
  if(!q || !optWrap) return;
  const answerText=(q.type==='mc' && q.options) ? esc(q.options[q.correct]) : esc(q.solution||'');
  optWrap.innerHTML=
    '<div class="quiz-recall-block">'+
    '<div class="quiz-recall-answer"><b>Respuesta:</b> '+answerText+'</div>'+
    '<div class="quiz-recall-selfgrade">¿Acertaste?'+
    `<button class="quiz-recall-ok-btn" onclick="_quizFreeRecallResult('${prefix}', true)">✅ Acerté</button>`+
    `<button class="quiz-recall-fail-btn" onclick="_quizFreeRecallResult('${prefix}', false)">❌ Fallé</button>`+
    '</div></div>';
}
/* Autocalificación del recuerdo libre: mismo destino que un acierto/fallo
   normal de opción múltiple (_recordAttempt, confianza, ver solución) --
   la caja Leitner no distingue CÓMO se llegó al resultado, solo si fue
   correcto, así que el resto del mecanismo (espaciado, badges de fallos)
   sigue funcionando igual sin ningún cambio en _recordAttempt. */
function _quizFreeRecallResult(prefix, success){
  if(_quizIsAnswered(prefix)) return;
  const mi=_quizCurrentModeIdx(prefix);
  if(!mi) return;
  _quizMarkAnswered(prefix);
  _recordAttempt(mi.mode, mi.idx, success);
  const ids=_quizIds(prefix);
  const fb=document.getElementById(ids.feedback);
  if(fb){
    fb.style.display='block';
    fb.className='math-feedback '+(success?'math-feedback-ok':'math-feedback-bad');
    fb.textContent=success ? '✅ Correcto — sigues en la caja de dominio.' : '❌ Incorrecto — vuelve a caja 1, se repasa pronto.';
  }
  const solBtn=document.getElementById(ids.solutionBtn);
  if(solBtn) solBtn.style.display='inline-block';
  _quizCallShowSolution(prefix);
  if(success){
    _quizRenderConfidencePrompt(prefix);
    const btnId=_quizNextBtnId(prefix);
    const nb=btnId && document.getElementById(btnId);
    if(nb && (prefix==='review' || _quizHasMoreInBank(prefix))) nb.style.display='inline-block';
  }
}
/* q.whyNot ya trae, por cada pregunta mc de EX_AO/RA/AS, una explicación
   propia de por qué CADA opción incorrecta está mal (no solo la que el
   alumno elige) -- pero hasta ahora _xxShowQuizSolution solo mostraba
   q.solution (por qué la correcta es correcta). Esto arma el bloque
   compartido con el resto, para que "ver solución" deje el mapa completo
   de discriminación entre las opciones confundibles, acierte o falle el
   alumno. `order` es el _xxQuizOrder de cada modo (posición mostrada ->
   índice original tras barajar) para etiquetar a),b),c)... como el alumno
   las vio en pantalla, no como están en el dato. */
function _quizWhyNotHtml(q, order){
  if(!q || q.type!=='mc' || !Array.isArray(q.whyNot) || !order) return '';
  const items=order.map((origIdx,dispIdx)=>{
    if(origIdx===q.correct) return '';
    const why=q.whyNot[origIdx];
    if(!why) return '';
    const letter=String.fromCharCode(97+dispIdx);
    return `<li><b>${letter}) ${esc(q.options[origIdx])}</b> — ${why}</li>`;
  }).filter(Boolean).join('');
  if(!items) return '';
  return '<div class="quiz-whynot-block"><div class="quiz-whynot-title">🔍 Por qué las demás opciones no son correctas</div>'+
    '<ul class="quiz-whynot-list">'+items+'</ul></div>';
}

/* q.steps (opcional, por ahora solo algunas preguntas de NS/RN/RF/AS): la
   traza de razonamiento que lleva a la respuesta, paso a paso, SIEMPRE
   visible al ver la solución -- acierte o falle el alumno -- a diferencia
   de whyNot (que solo cubre por qué las opciones incorrectas están mal),
   esto muestra el camino de ida hacia la correcta. Mismo criterio de
   "un solo bloque compartido" que _quizWhyNotHtml. */
function _quizStepsHtml(q){
  if(!q || !Array.isArray(q.steps) || !q.steps.length) return '';
  const items=q.steps.map(s=>`<li>${s}</li>`).join('');
  return '<div class="quiz-steps-block"><div class="quiz-steps-title">🧭 Cómo llegar a la respuesta, paso a paso</div>'+
    '<ol class="quiz-steps-list">'+items+'</ol></div>';
}

/* q.stakes (opcional, por ahora solo algunas preguntas de NS/RN/RF/AS): un
   puente breve y CONCRETO entre ESTA pregunta puntual y un caso real donde
   equivocarse con este concepto específico tiene una consecuencia -- a
   diferencia del `application` de cada tema (que describe dónde se usa el
   tema en general, siempre igual sin importar qué pregunta salió), esto es
   específico de la pregunta y aparece recién al ver la solución, en el
   momento de máxima atención tras responder. Mismo criterio de bloque
   compartido que _quizStepsHtml/_quizWhyNotHtml. */
function _quizStakesHtml(q){
  if(!q || !q.stakes) return '';
  return '<div class="quiz-stakes-block"><div class="quiz-stakes-title">💡 Por qué esto importa en la práctica</div>'+
    '<p class="quiz-stakes-body">'+q.stakes+'</p></div>';
}

/* Glosario por modo (GLOSSARY_NS/RN/RF/AS, ver cada master-*.js): pedido
   explícito del usuario ("que ningún término quede sin explicación") --
   distinto de `theory`/`steps`/`stakes` (que explican el POR QUÉ de un
   concepto o pregunta puntual), el glosario cubre el VOCABULARIO: cada
   palabra técnica que aparece en preguntas/teoría de ese modo, con su
   definición, buscable en cualquier momento (no hace falta acordarse en
   qué tema se explicó por primera vez). `list` ya viene ordenada
   alfabéticamente por term. `filterText` (opcional) filtra por substring
   sobre term+def, sin distinguir mayúsculas. */
function _glossaryHtml(list, filterText){
  if(!Array.isArray(list) || !list.length) return '<div class="master-glossary-empty">Sin términos.</div>';
  const f=(filterText||'').trim().toLowerCase();
  const items=list.filter(g=>!f || g.term.toLowerCase().includes(f) || g.def.toLowerCase().includes(f));
  if(!items.length) return '<div class="master-glossary-empty">Ningún término coincide con la búsqueda.</div>';
  return items.map(g=>`<div class="master-glossary-item"><div class="master-glossary-term">${esc(g.term)}</div>`+
    `<div class="master-glossary-def">${g.def}</div></div>`).join('');
}

/* Migración única: EX_AO (master-ao.js) se reordenó 2026-08-09 para seguir
   la cronología real del curso (Ordenación+AG1 primero, Algoritmos
   Genéticos al final — ver el comentario grande al inicio de ese archivo).
   Como el progreso guardado (`pyvizMasterAoProgress`, done por índice) y
   las estadísticas/Leitner (`pyvizMasterStats`.ao, por índice) se guardaban
   por ÍNDICE del array, no por nombre de tema, un reorden sin más dejaría
   los checkmarks de quien ya hubiera avanzado apuntando al tema
   equivocado. El mapeo es un simple intercambio de los dos bloques de 9:
   índices 0-8 (antes Algoritmos Genéticos) <-> 9-17 (antes Ordenación+AG1).
   Se ejecuta una sola vez por navegador (guardado con MIGRATION_KEY) y no
   hace nada si no hay progreso de AO que migrar. */
const AO_ORDER_MIGRATION_KEY='pyvizAoOrderMigratedV1';
function _migrateAoOrder(){
  try{
    if(localStorage.getItem(AO_ORDER_MIGRATION_KEY)) return; // ya migrado, no repetir
    const remap=i=> i<9 ? i+9 : i-9;

    const rawProgress=localStorage.getItem('pyvizMasterAoProgress');
    if(rawProgress){
      const d=JSON.parse(rawProgress);
      if(Array.isArray(d.done)) d.done=d.done.map(remap);
      localStorage.setItem('pyvizMasterAoProgress', JSON.stringify(d));
    }

    const rawStats=localStorage.getItem(MASTER_STATS_KEY);
    if(rawStats){
      const s=JSON.parse(rawStats);
      if(s.ao){
        const remapped={};
        for(const k in s.ao) remapped[remap(parseInt(k,10))]=s.ao[k];
        s.ao=remapped;
        localStorage.setItem(MASTER_STATS_KEY, JSON.stringify(s));
      }
    }

    localStorage.setItem(AO_ORDER_MIGRATION_KEY, '1');
  }catch(e){ /* localStorage inaccesible o corrupto: no migrar, no romper la carga */ }
}

/* Segunda migración única: 2026-08-09 se insertaron los batches 3-5 de AO
   (VC3, VC4, AG2, VC5, AG3 1ª parte — 23 temas nuevos) EN MEDIO del array,
   justo después de "Programación Dinámica" (índice 8) y antes de
   "Algoritmos Genéticos" (que hasta ahora empezaban en el índice 9). Quien
   ya hubiera avanzado en Algoritmos Genéticos bajo la numeración vieja
   (9-17, ya post-_migrateAoOrder) necesita que sus índices se corran +23
   (pasan a 32-40). Los índices 0-8 (Ordenación+AG1) no cambian. Se ejecuta
   DESPUÉS de _migrateAoOrder() (ver init.js) y una sola vez por navegador. */
const AO_BATCH345_MIGRATION_KEY='pyvizAoBatch345MigratedV1';
function _migrateAoBatch345Order(){
  try{
    if(localStorage.getItem(AO_BATCH345_MIGRATION_KEY)) return; // ya migrado, no repetir
    const remap=i=> i<9 ? i : i+23;

    const rawProgress=localStorage.getItem('pyvizMasterAoProgress');
    if(rawProgress){
      const d=JSON.parse(rawProgress);
      if(Array.isArray(d.done)) d.done=d.done.map(remap);
      localStorage.setItem('pyvizMasterAoProgress', JSON.stringify(d));
    }

    const rawStats=localStorage.getItem(MASTER_STATS_KEY);
    if(rawStats){
      const s=JSON.parse(rawStats);
      if(s.ao){
        const remapped={};
        for(const k in s.ao) remapped[remap(parseInt(k,10))]=s.ao[k];
        s.ao=remapped;
        localStorage.setItem(MASTER_STATS_KEY, JSON.stringify(s));
      }
    }

    localStorage.setItem(AO_BATCH345_MIGRATION_KEY, '1');
  }catch(e){ /* localStorage inaccesible o corrupto: no migrar, no romper la carga */ }
}


/* ── SVG relation arrows ── */
const NS='http://www.w3.org/2000/svg';
function _svg(tag,attrs){const e=document.createElementNS(NS,tag);
  for(const k in attrs)e.setAttribute(k,attrs[k]);return e;}

let _arrowSeq=0;
function drawArrows(){
  const svg=document.getElementById('relArrows');
  if(!svg) return;
  svg.innerHTML='';
  if(!steps[cur]||!Object.keys(relations).length) return;

  const curVars={};
  for(const fr of steps[cur].frames) Object.assign(curVars, fr.variables);

  const botWrap=document.querySelector('.bot-wrap');
  if(!botWrap) return;
  const botRect=botWrap.getBoundingClientRect();
  let drawn=0;

  for(const [iterVar, srcVar] of Object.entries(relations)){
    if(!(iterVar in curVars)||(selVar&&selVar!==srcVar)) continue;

    // Source: the iter var widget in Frames
    const iterEl=document.querySelector(`.vwidget[data-var="${CSS.escape(iterVar)}"]`);
    if(!iterEl) continue;

    // Target: active cell (list) or active row (dict) in Objects
    const targetEl=
      document.querySelector('.ob-cell-act')||
      document.querySelector('.ob-tr-act td:first-child');
    if(!targetEl) continue;

    const iR=iterEl.getBoundingClientRect();
    const tR=targetEl.getBoundingClientRect();

    // Anchor on source: right-middle of the iter widget
    const x1=iR.right-botRect.left;
    const y1=(iR.top+iR.bottom)/2-botRect.top;
    // Anchor on target: left-middle of the active cell
    const x2=tR.left-botRect.left-3;
    const y2=(tR.top+tR.bottom)/2-botRect.top;

    if(x2<=x1+10) continue; // panels not yet laid out

    // Control points pulled horizontally → smooth "cable" entering each side flat.
    const pull=Math.max(28,(x2-x1)*0.45);
    const c1x=x1+pull, c2x=x2-pull;
    const d=`M ${x1} ${y1} C ${c1x} ${y1}, ${c2x} ${y2}, ${x2} ${y2}`;
    const pid='relp'+(_arrowSeq++);

    // 1) faint base cable
    svg.appendChild(_svg('path',{d,'class':'rel-base'}));
    // 2) animated dashed path (with id for the particle to follow)
    svg.appendChild(_svg('path',{d,'class':'rel-path',id:pid}));

    // 3) origin pulse dot
    svg.appendChild(_svg('circle',{cx:x1,cy:y1,r:5,'class':'rel-dot'}));

    // 4) arrowhead — angle from true bezier tangent at t=1 : 3*(P3-P2)
    // arrowhead angle = bezier tangent at t=1 = 3*(P3-P2) = (x2-c2x, y2-y2)
    const tx=x2-c2x, tyt=y2-y2;       // tyt is 0 (flat entry by design)
    const ang=Math.atan2(tyt, tx||1);
    const sz=9, a1=ang+Math.PI-0.42, a2=ang+Math.PI+0.42;
    svg.appendChild(_svg('polygon',{'class':'rel-head',points:
      `${x2},${y2} ${x2+sz*Math.cos(a1)},${y2+sz*Math.sin(a1)} ${x2+sz*Math.cos(a2)},${y2+sz*Math.sin(a2)}`}));

    // 5) traveling particle: a glowing dot flowing source→target (the binding)
    [['rel-particle-glow',4.5],['rel-particle',2.6]].forEach(([cls,r])=>{
      const p=_svg('circle',{r,cx:0,cy:0,'class':cls});
      const mo=_svg('animateMotion',{dur:'1.1s',repeatCount:'indefinite',
        keyPoints:'0;1',keyTimes:'0;1',calcMode:'linear'});
      const mp=_svg('mpath',{});
      mp.setAttributeNS('http://www.w3.org/1999/xlink','href','#'+pid);
      mp.setAttribute('href','#'+pid);
      mo.appendChild(mp); p.appendChild(mo); svg.appendChild(p);
    });

    // 6) relationship label at the curve midpoint
    const {idx,key}=_activeIdxForVar(srcVar);
    let tag=esc(iterVar)+' →';
    if(idx!==null) tag=esc(iterVar)+' → ['+idx+']';
    else if(key!==null) tag=esc(iterVar)+" → '"+esc(String(key))+"'";
    const mx=(x1+x2)/2, my=(y1+y2)/2-12;
    const w=tag.length*6.3+12;
    svg.appendChild(_svg('rect',{x:mx-w/2,y:my-9,width:w,height:18,rx:7,'class':'rel-label-bg'}));
    const t=_svg('text',{x:mx,y:my,'class':'rel-label-tx'}); t.textContent=tag;
    svg.appendChild(t);
    drawn++;
  }
}

function _flashObjPanel(name, isNew){
  const pt=document.querySelector('.ptitle-ob');
  const ob=document.querySelector('.ob-wrap');
  if(pt) pt.textContent='Objects — '+name;
  if(ob && isNew){
    ob.style.transition='none';
    ob.style.boxShadow='0 0 0 2px #c77dbb';
    setTimeout(()=>{
      ob.style.transition='box-shadow .6s ease';
      ob.style.boxShadow='none';
    }, 50);
  }
}

function go(n){
  if(n<0||n>=steps.length) return;
  const step=steps[n];
  const pLine= n>0 ? steps[n-1].line : -1;
  const diff = computeDiff(prev, step);
  cur=n;
  renderExec(pLine, step.line);
  renderNarrator(step.line, n, steps.length-1);
  renderFrames(step.frames, diff);
  setOutput(step.output);
  autoPickObj(step);
  requestAnimationFrame(drawArrows);
  const done=step.line===-1;
  if(done){
    // Reaching the sentinel step doesn't mean the run actually succeeded —
    // the backend appends it even after an error/timeout, so if one was
    // recorded, keep showing it instead of a falsely reassuring "terminado".
    // _lastRunTruncated distingue un corte de seguridad (2000 pasos / 12s,
    // el código del alumno NO tiene ningún bug) de un error real -- mismo
    // motivo por el que antes esto siempre decía "Python 3 · Error" incluso
    // cuando el único "problema" era un bucle simplemente largo.
    setSt(_lastRunError ? ((_lastRunTruncated?'✂️ ':'⚠ ')+_lastRunError) : '✓ Programa terminado');
    document.getElementById('pyHdrTxt').textContent=_lastRunError
      ? (_lastRunTruncated?'Python 3 · Truncado':'Python 3 · Error')
      : 'Python 3 · Programa terminado';
    stopAuto();
  } else {
    setSt(`L\xednea ${step.line} — paso ${n+1} de ${steps.length-1}`);
    document.getElementById('pyHdrTxt').textContent=`Python 3 · Paso ${n+1}/${steps.length-1}`;
  }
  prev=step; updBtns();
}

/* ──────────── Narrator (line explanation) ──────────── */
let _narLastLine=null;
function renderNarrator(line, stepIdx, total){
  const bar=document.getElementById('narrator');
  const ico=document.getElementById('narIco');
  const txt=document.getElementById('narTxt');
  const det=document.getElementById('narDetail');
  if(!bar) return;
  bar.className='narrator';  // reset kind classes
  bar.classList.remove('nar-flash');
  if(det) det.innerHTML='';

  if(line===-1){
    bar.classList.add('nar-k-done');
    ico.textContent=NAR_ICO.done;
    txt.innerHTML='<b>Programa terminado.</b> Todas las variables finales aparecen en Frames.';
    void bar.offsetWidth; bar.classList.add('nar-flash');
    _narLastLine=null;
    return;
  }
  const info=explains[line];
  if(!info){
    bar.classList.add('narrator-idle');
    ico.textContent='💡';
    txt.innerHTML=`Ejecutando la línea <span class="nar-var">${line}</span>`;
    return;
  }
  bar.classList.add('nar-k-'+info.kind);
  ico.textContent=NAR_ICO[info.kind]||'💡';
  // Highlight «names» as styled code spans
  const safe=esc(info.text).replace(/«([^»]+)»/g,'<span class="nar-var">$1</span>');
  txt.innerHTML=safe+`<span class="nar-step">L${line}</span>`;
  // Breakdown (cómo se evalúa) + efecto (qué cambió)
  if(det) det.innerHTML=_narDetailHTML(stepIdx);
  // Animate only when the line actually changed
  if(line!==_narLastLine){
    void bar.offsetWidth;      // force reflow to restart animation
    bar.classList.add('nar-flash');
  }
  _narLastLine=line;
}

/* breakdown (backend) + effect (diff to next step) shown under the narrator */
function _narDetailHTML(n){
  const step=steps[n]; if(!step) return '';
  const rows=[];
  if(step.eval && step.eval.length){
    step.eval.forEach(e=>{
      rows.push(`<div class="nar-ev"><span class="ev-expr">${esc(e.expr)}</span>`+
        `<span class="ev-arrow">→</span><span class="ev-val">${esc(e.val)}</span></div>`);
    });
  }
  const nx=steps[n+1];
  if(nx){ const fx=_lineEffect(step, nx); if(fx) rows.push(fx); }
  return rows.join('');
}

/* what the current line produced: a new/changed variable or printed output */
function _lineEffect(cur, nx){
  const pv={}, cv={};
  (cur.frames||[]).forEach(f=>Object.assign(pv,f.variables));
  (nx.frames||[]).forEach(f=>Object.assign(cv,f.variables));
  for(const k in cv){
    if(!(k in pv))
      return `<div class="nar-fx nar-fx-new">✓ <b>${esc(k)}</b> = ${esc(_fmtVal(cv[k]))} <span style="color:#5a6a8a">(nueva)</span></div>`;
  }
  for(const k in cv){
    if(k in pv && JSON.stringify(cv[k])!==JSON.stringify(pv[k]))
      return `<div class="nar-fx nar-fx-chg">✓ <b>${esc(k)}</b>: ${esc(_fmtVal(pv[k]))} <span class="ev-arrow">→</span> ${esc(_fmtVal(cv[k]))}</div>`;
  }
  const co=cur.output||'', no=nx.output||'';
  if(no.length>co.length){
    let added=no.slice(co.length).replace(/\n+$/,'');
    if(added.trim()){ if(added.length>44) added=added.slice(0,44)+'…';
      return `<div class="nar-fx nar-fx-out">🖨️ imprimió: ${esc(added)}</div>`; }
  }
  return '';
}

/* compact display of a serialized value for the narrator */
function _fmtVal(v){
  if(v===null||v===undefined) return 'None';
  if(typeof v==='boolean') return v?'True':'False';
  if(typeof v==='number') return String(v);
  if(typeof v==='string'){ let s="'"+v+"'"; return s.length>26?s.slice(0,25)+"…'":s; }
  if(Array.isArray(v)){ let s='['+v.map(_fmtValShort).join(', ')+']'; return s.length>30?s.slice(0,29)+'…]':s; }
  if(v.__set__) return '{'+(v.values||[]).slice(0,4).map(_fmtValShort).join(', ')+'}';
  if(v.__obj__) return v.type+'(…)';
  if(v.__matrix__) return 'matriz '+(v.shape||[]).join('×');
  if(v.__series__) return 'Series('+(v.len||'')+')';
  if(v.__df__) return 'DataFrame '+(v.shape||[]).join('×');
  if(typeof v==='object'){ const ks=Object.keys(v);
    return '{'+ks.slice(0,3).map(k=>k+': '+_fmtValShort(v[k])).join(', ')+(ks.length>3?', …':'')+'}'; }
  return String(v);
}
function _fmtValShort(v){
  if(v===null) return 'None';
  if(typeof v==='boolean') return v?'True':'False';
  if(typeof v==='string') return "'"+(v.length>10?v.slice(0,9)+'…':v)+"'";
  if(Array.isArray(v)) return '[…]';
  if(v&&typeof v==='object') return '{…}';
  return String(v);
}

/* ──────────── Executor render ──────────── */
function renderExec(pLine, nLine){
  const code=document.getElementById('codeInput').value;
  const lines=code.split('\n');
  let h='';
  lines.forEach((ln,i)=>{
    const n=i+1;
    const isPrev=n===pLine, isNext=n===nLine, isBP=bps.has(n);
    const cls=isNext?'r-next':isPrev?'r-prev':isBP?'r-bp':'';
    const arr=isPrev?'<span class="ap">➤</span>':isNext?'<span class="an">▶</span>':'';
    h+=`<div class="er ${cls}" id="er${n}">` +
       `<span class="eln">${isBP?'●':n}</span>` +
       `<span class="earr">${arr}</span>` +
       `<span class="ecode">${hl(ln)}</span></div>`;
  });
  const sc=document.getElementById('execScroll');
  sc.innerHTML=h;
  const tgt=nLine>0?nLine:pLine;
  if(tgt>0){ const el=document.getElementById('er'+tgt); if(el) el.scrollIntoView({block:'nearest',behavior:'smooth'}); }
}

/* ──────────── Syntax highlighter ──────────── */
const KW=new Set('if elif else for while def return import from class True False None and or not in is break continue pass lambda try except finally with as yield del global nonlocal raise assert'.split(' '));
const BI=new Set('print len range sum min max abs str int float list dict set tuple bool type input enumerate zip map filter sorted reversed any all round pow open format repr chr ord'.split(' '));

function hl(line){
  let o='', i=0, L=line.length;
  while(i<L){
    const c=line[i];
    if(c==='#'){ o+=`<span class="cmt">${esc(line.slice(i))}</span>`; break; }
    // f/b/r prefix
    let pfx='';
    if('fFbBrR'.includes(c)&&i+1<L&&(line[i+1]==='"'||line[i+1]==="'")){pfx=c;i++;}
    if(line[i]==='"'||line[i]==="'"){
      const q=line[i], tri=line.slice(i,i+3)===q.repeat(3);
      let j=tri?i+3:i+1;
      while(j<L){ if(line[j]==='\\'){j+=2;continue;} if(tri){if(line.slice(j,j+3)===q.repeat(3)){j+=3;break;}}else{if(line[j]===q){j++;break;}} j++; }
      o+=pfx+`<span class="str">${esc(line.slice(i,j))}</span>`; i=j; continue;
    }
    if(pfx){o+=esc(pfx);}
    if(/\d/.test(c)||(c==='.'&&i+1<L&&/\d/.test(line[i+1]))){
      let j=i; while(j<L&&/[\d.eExXoObBa-fA-F_]/.test(line[j]))j++;
      o+=`<span class="num">${esc(line.slice(i,j))}</span>`; i=j; continue;
    }
    if(/[a-zA-Z_]/.test(c)){
      let j=i; while(j<L&&/\w/.test(line[j]))j++;
      const w=line.slice(i,j);
      o+=KW.has(w)?`<span class="kw">${w}</span>`:BI.has(w)?`<span class="bi">${w}</span>`:esc(w);
      i=j; continue;
    }
    o+=esc(c); i++;
  }
  return o;
}

/* ──────────── Frames panel ──────────── */
function renderFrames(frames, diff){
  const el=document.getElementById('frBody');
  if(!frames||!frames.length){ el.innerHTML='<div class="ob-ph">No variables yet</div>'; autoLayout(); return; }
  let h='';
  frames.forEach(fr=>{
    const isGlob=fr.name==='<module>';
    const ico=isGlob?'🌍':'⚙';
    h+=`<div class="fgtitle"><span class="fgtitle-ico">${ico}</span>${isGlob?'Global frame':esc(fr.name)+'()'}<div class="fgtitle-line"></div></div>`;
    const entries=Object.entries(fr.variables);
    if(!entries.length){ h+='<div style="color:#555;font-size:11px;padding:3px 12px;font-style:italic">sin variables</div>'; }
    entries.forEach(([k,v])=>{
      const isNew=diff&&diff.nw.has(k), isCh=diff&&diff.ch.has(k)&&!isNew;
      h+=wgRender(k,v,isNew?'v-new':isCh?'v-changed':'');
    });
  });
  el.innerHTML=h;
  autoLayout();
}

/* ── Widget renderers by type ── */
function _linkBadge(k){
  const src=relations[k];
  if(!src) return '';
  return`<span class="vw-link"><span class="vw-link-arr">↩</span>${esc(src)}</span>`;
}

function wgRender(k,v,anim){
  if(v===null)             return wgNone(k,anim);
  if(typeof v==='boolean') return wgBool(k,v,anim);
  if(typeof v==='number'&&Number.isInteger(v)) return wgInt(k,v,anim);
  if(typeof v==='number')  return wgFloat(k,v,anim);
  if(typeof v==='string')  return wgStr(k,v,anim);
  if(Array.isArray(v))     return wgList(k,v,anim);
  if(typeof v==='object'&&v?.__set__)    return wgSet(k,v,anim);
  if(typeof v==='object'&&v?.__obj__)    return wgObj(k,v,anim);
  if(typeof v==='object'&&v?.__matrix__) return wgMatrix(k,v,anim);
  if(typeof v==='object'&&v?.__series__) return wgSeries(k,v,anim);
  if(typeof v==='object'&&v?.__df__)     return wgDataFrame(k,v,anim);
  if(typeof v==='object')  return wgDict(k,v,anim);
  return `<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr"><span class="vw-ico">📌</span><span class="vw-nm">${esc(k)}</span><span class="vw-val">${esc(String(v))}</span></div></div>`;
}

/* Small non-negative ints are shown with their binary form too — this is
   what makes bitmask-style code (unions of bits, popcount, etc.) readable
   instead of just a mysterious decimal number. */
function binHint(v){
  return (Number.isInteger(v) && v>=0 && v<=65535) ? v.toString(2) : null;
}

function wgInt(k,v,anim){
  const pct=Math.max(0,Math.min(Math.abs(v),100));
  const neg=v<0, col=neg?'nbar-neg':'';
  const link=_linkBadge(k);
  const bh=binHint(v);
  const binBadge=bh!==null?`<span class="vw-bin" title="Representación binaria">0b${bh}</span>`:'';
  const bitsBtn=bh!==null?`<button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 bits</button>`:'';
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">🔢</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-int">int</span>
    <span class="vw-val vnum">${v}</span>${binBadge}${link}${bitsBtn}</div>
    <div class="nbar"><div class="nbar-f ${col}" style="width:${pct}%"></div></div></div>`;}

function wgFloat(k,v,anim){
  const disp=parseFloat(v.toPrecision(6));
  const pct=Math.max(0,Math.min(Math.abs(v),100));
  const link=_linkBadge(k);
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">🔣</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-flt">float</span>
    <span class="vw-val vnum">${disp}</span>${link}</div>
    <div class="nbar"><div class="nbar-f" style="width:${pct}%;background:linear-gradient(90deg,#4fc3a1,#1abc9c)"></div></div></div>`;}

function wgStr(k,v,anim){
  const short=v.length>22?v.slice(0,19)+'…':v;
  const link=_linkBadge(k);
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">📝</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-str">str</span>
    <span class="vw-val vstr">"${esc(short)}"</span>
    <span style="font-size:9px;color:#666;margin-left:4px">${v.length}ch</span>${link}</div></div>`;}

function wgBool(k,v,anim){
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">${v?'✅':'❌'}</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-bool">bool</span>
    <div class="vw-tog ${v?'tog-on':'tog-off'}" style="margin-left:auto">
      <div class="tog-track"><div class="tog-knob"></div></div>
      <span class="tog-lbl">${v?'True':'False'}</span></div></div></div>`;}

function wgNone(k,anim){
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">∅</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-none">None</span>
    <span class="vw-val" style="color:#666">None</span></div></div>`;}

function wgList(k,v,anim){
  const MAX=8;
  const cells=v.slice(0,MAX).map((it,i)=>{
    const isN=typeof it==='number'||typeof it==='boolean';
    const d=typeof it==='string'?`"${esc(it.length>6?it.slice(0,5)+'…':it)}"`:esc(String(it));
    return`<div class="lmc" style="animation-delay:${i*35}ms"><div class="lmc-i">${i}</div><div class="lmc-v ${isN?'is-num':''}">${d}</div></div>`;
  }).join('');
  const more=v.length>MAX?`<span class="lmini-more">+${v.length-MAX}</span>`:'';
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">📋</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-list">list[${v.length}]</span>
    <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="lmini">${cells}${more}</div></div>`;}

function wgDict(k,v,anim){
  const entries=Object.entries(v), MAX=4;
  const rows=entries.slice(0,MAX).map(([dk,dv],i)=>{
    const isN=typeof dv==='number'||typeof dv==='boolean';
    const vd=typeof dv==='string'?`"${esc(dv.slice(0,12))}"`:esc(String(dv));
    return`<div class="drow" style="animation-delay:${i*30}ms"><span class="dk">"${esc(dk)}"</span><span class="dsep">:</span><span class="dv ${isN?'is-num':''}">${vd}</span></div>`;
  }).join('');
  const more=entries.length>MAX?`<div class="dmini-more">…+${entries.length-MAX} más</div>`:'';
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">📦</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-dict">dict[${entries.length}]</span>
    <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="dmini">${rows}${more}</div></div>`;}

function wgSet(k,v,anim){
  const items=(v.values||[]), MAX=6;
  const cells=items.slice(0,MAX).map((it,i)=>{
    const isN=typeof it==='number';
    const d=typeof it==='string'?`"${esc(it.slice(0,6))}"`:esc(String(it));
    return`<div class="lmc" style="animation-delay:${i*35}ms"><div class="lmc-i">{${i}}</div><div class="lmc-v ${isN?'is-num':''}">${d}</div></div>`;
  }).join('');
  const more=items.length>MAX?`<span class="lmini-more">+${items.length-MAX}</span>`:'';
  return`<div class="vwidget ${anim}" data-var="${esc(k)}"><div class="vw-hdr">
    <span class="vw-ico">🔵</span><span class="vw-nm">${esc(k)}</span>
    <span class="vw-ty ty-set">set[${items.length}]</span>
    <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="lmini">${cells}${more}</div></div>`;}

// ── Class instance widget ──
function wgObj(k,v,anim){
  const typename=v.type||'object';
  const attrs=Object.entries(v.attrs||{});
  const MAX=4;
  const rows=attrs.slice(0,MAX).map(([ak,av],i)=>{
    const isN=typeof av==='number';
    const vd=typeof av==='string'?`"${esc(String(av).slice(0,14))}"`:esc(String(av));
    return`<div class="drow" style="animation-delay:${i*30}ms">
      <span class="dk" style="color:#4ec9b0">.${esc(ak)}</span>
      <span class="dsep">=</span>
      <span class="dv ${isN?'is-num':''}">${vd}</span></div>`;
  }).join('');
  const more=attrs.length>MAX?`<div class="dmini-more">…+${attrs.length-MAX} attrs</div>`:'';
  return`<div class="vwidget ${anim}" data-var="${esc(k)}" style="border-color:#2a4a4a">
    <div class="vw-hdr">
      <span class="vw-ico">🔷</span><span class="vw-nm">${esc(k)}</span>
      <span class="vw-ty" style="background:#0d2a3a;color:#4ec9b0;border-color:#2a4a4a">${esc(typename)}</span>
      <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="dmini">${rows}${more}</div></div>`;}

// ── numpy matrix widget ──
function wgMatrix(k,v,anim){
  const shape=v.shape||[];
  let preview='';
  if(shape.length>=3){
    const dim=shape.length>=4?'4D':'3D';
    preview=`<div class="drow" style="font-size:10px;color:#9b8fff;font-family:monospace">${dim} ${shape.join('×')} — pulsa 🔍 ver</div>`;
  } else {
    const rows=(v.data||[]).slice(0,4);
    if(rows.length&&Array.isArray(rows[0])){
      preview=rows.map(r=>`<div class="drow" style="font-size:10px;color:#9b8fff;font-family:monospace">[${r.slice(0,6).join(', ')}${r.length>6?'…':''}]</div>`).join('');
    } else {
      preview=`<div class="drow" style="font-size:10px;color:#9b8fff;font-family:monospace">[${rows.slice(0,8).join(', ')}${rows.length>8?'…':''}]</div>`;
    }
  }
  return`<div class="vwidget ${anim}" data-var="${esc(k)}" style="border-color:#3a1a42">
    <div class="vw-hdr">
      <span class="vw-ico">📊</span><span class="vw-nm">${esc(k)}</span>
      <span class="vw-ty" style="background:#1a0a2a;color:#c77dbb">ndarray ${shape.join('×')}</span>
      <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="dmini">${preview}</div></div>`;}

// ── pandas Series widget ──
function wgSeries(k,v,anim){
  const vals=v.values||[];
  const idxs=v.index||[];
  const MAX=5;
  const rows=vals.slice(0,MAX).map((val,i)=>{
    const isN=typeof val==='number';
    return`<div class="drow" style="animation-delay:${i*25}ms">
      <span class="dk" style="color:#f0c060">${esc(String(idxs[i]??i))}</span>
      <span class="dsep">:</span>
      <span class="dv ${isN?'is-num':''}">${esc(String(val))}</span></div>`;
  }).join('');
  const more=vals.length>MAX?`<div class="dmini-more">…+${vals.length-MAX} más</div>`:'';
  return`<div class="vwidget ${anim}" data-var="${esc(k)}" style="border-color:#3a2a00">
    <div class="vw-hdr">
      <span class="vw-ico">📈</span><span class="vw-nm">${esc(k)}</span>
      <span class="vw-ty" style="background:#2a1a00;color:#f0c060">Series[${v.len??vals.length}]</span>
      <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="dmini">${rows}${more}</div></div>`;}

// ── pandas DataFrame widget ──
function wgDataFrame(k,v,anim){
  const cols=v.columns||[];
  const shape=v.shape||[0,0];
  const preview=cols.slice(0,4).map(c=>`<span class="dv" style="font-size:9px;color:#f0c060">${esc(String(c))}</span>`).join(' ');
  return`<div class="vwidget ${anim}" data-var="${esc(k)}" style="border-color:#3a2a00">
    <div class="vw-hdr">
      <span class="vw-ico">🗃️</span><span class="vw-nm">${esc(k)}</span>
      <span class="vw-ty" style="background:#2a1a00;color:#f0c060">DataFrame ${shape[0]}×${shape[1]}</span>
      <button class="obtn" onclick='pickObj(${JSON.stringify(k)})'>🔍 ver</button></div>
    <div class="dmini"><div class="drow" style="font-size:9px">${preview}${cols.length>4?'…':''}</div></div></div>`;}

function pickObj(name){
  const step=steps[cur]; if(!step) return;
  for(const fr of step.frames){
    if(name in fr.variables){
      selVar=name; _autoSelected=false; // a deliberate user pick always sticks
      renderObjects(name, fr.variables[name]);
      const pt=document.querySelector('.ptitle-ob');
      if(pt) pt.textContent='Objects — '+name;
      return;
    }
  }
}

/* ──────────── Objects panel (expanded view) ──────────── */
function obTypeInfo(v){
  if(v===null)             return{t:'None',cls:'is-bool',d:'None'};
  if(typeof v==='boolean') return{t:'bool',cls:'is-bool',d:v?'True':'False'};
  if(typeof v==='number'&&Number.isInteger(v)) return{t:'int', cls:'is-num',d:String(v),bin:binHint(v)};
  if(typeof v==='number')  return{t:'float',cls:'is-num',d:String(v)};
  if(typeof v==='string')  return{t:'str', cls:'is-str',d:`"${esc(v.length>16?v.slice(0,14)+'…':v)}"`};
  if(Array.isArray(v))     return{t:'list',cls:'',d:`[list·${v.length}]`};
  return{t:'?',cls:'',d:esc(String(v))};
}

function _activeIdxForVar(name){
  // Find integer index or string key from relations pointing at `name`
  if(!steps[cur]) return {idx:null, key:null};
  const curVars={};
  for(const fr of steps[cur].frames) Object.assign(curVars, fr.variables);
  let activeIdx=null, activeKey=null;
  for(const [iterVar,srcVar] of Object.entries(relations)){
    if(srcVar!==name || !(iterVar in curVars)) continue;
    const v=curVars[iterVar];
    if(typeof v==='number'&&Number.isInteger(v)) activeIdx=v;
    else if(typeof v==='string') activeKey=v;
  }
  return {idx:activeIdx, key:activeKey};
}

/* Indices of `name` the CURRENT line is actively reading, e.g. the i and
   i+1 in `if a[i] > a[i+1]:` — from the backend's per-line subscript map
   (step.idx), independent of any `for x in a` loop pattern. This is what
   lets the bar chart show a "claw" over exactly the elements being
   compared, for any sorting algorithm's index style (i/j, lo/hi, …). */
function _activeSubIdx(name){
  const st=steps[cur];
  return (st && st.idx && st.idx[name]) || [];
}

/* Toggle the numeric-list view between the bar chart and the plain card
   grid, then redraw whatever is currently pinned in the Objects panel. */
function toggleListView(){
  _listViewMode = (_listViewMode==='cards') ? 'bars' : 'cards';
  if(!selVar || !steps[cur]) return;
  for(const fr of steps[cur].frames){
    if(selVar in fr.variables){ renderObjects(selVar, fr.variables[selVar]); return; }
  }
}

/* ── N-dimensional ndarray renderer (2D grid / 3D planes / 4D blocks) ── */
function _matCell(v){
  if(typeof v==='number') return Number.isInteger(v)?String(v):String(+v.toFixed(4));
  if(v===null) return '·';
  if(typeof v==='boolean') return v?'T':'F';
  return esc(String(v));
}
/* Structural equality used only to detect "did this cell change between
   animation frames" — values here are already JSON-plain (server output),
   so stringify comparison is safe and cheap. */
function _deepEq(a,b){ return JSON.stringify(a)===JSON.stringify(b); }
/* Regular-shape detector for plain Python nested lists (matrices/tensors
   built without numpy). Returns the shape array (e.g. [2,3]) if `v` is a
   rectangular nesting of scalars, or null if ragged / holds non-scalars —
   in which case the caller falls back to the flat 1D card view. */
function _listShape(v){
  if(v===null || typeof v!=='object') return [];
  if(!Array.isArray(v)) return null;
  if(v.length===0) return [0];
  const subs=v.map(_listShape);
  if(subs.some(s=>s===null)) return null;
  const first=JSON.stringify(subs[0]);
  if(!subs.every(s=>JSON.stringify(s)===first)) return null;
  return [v.length, ...subs[0]];
}
/* Matches each element of `newArr` back to the index it occupied in
   `prevArr` (by value, consuming duplicates left-to-right), or -1 if the
   value didn't exist before. This is what lets a sort/reorder be shown as
   elements sliding to their new spot instead of the whole grid flashing. */
function _matchOldIndices(prevArr, newArr){
  const pool=new Map();
  prevArr.forEach((v,i)=>{
    const key=JSON.stringify(v);
    if(!pool.has(key)) pool.set(key, []);
    pool.get(key).push(i);
  });
  return newArr.map(v=>{
    const q=pool.get(JSON.stringify(v));
    return (q && q.length) ? q.shift() : -1;
  });
}
function _render2D(rows, prevRows){
  const norm=rows.map(r=>Array.isArray(r)?r:[r]);
  const prevNorm=Array.isArray(prevRows)?prevRows.map(r=>Array.isArray(r)?r:[r]):null;
  const ncol=Math.max(1,...norm.map(r=>r.length));
  let cells='';
  norm.forEach((r,ri)=>{
    r.forEach((v,ci)=>{
      const changed=prevNorm!=null && !_deepEq(v, prevNorm[ri]?.[ci]);
      const cls='omat-c'+(changed?' omat-c-diff':'');
      const dly=prevNorm==null?` style="animation-delay:${(ri*ncol+ci)*14}ms"`:'';
      cells+=`<div class="${cls}"${dly}>${_matCell(v)}</div>`;
    });
    for(let k=r.length;k<ncol;k++) cells+=`<div class="omat-c omat-pad">·</div>`;
  });
  return `<div class="omat" style="grid-template-columns:repeat(${ncol},minmax(30px,1fr))">${cells}</div>`;
}
/* ── Bitmask renderer: shows a non-negative int as a 1D array of bit
   cells (MSB→LSB), flashing the bits that flipped since the last frame —
   this is what turns "0b0101" from opaque text into an animated 1D vector. */
function _bitWidth(v){
  let w=4;
  while(v>=(1<<w) && w<16) w+=4;
  return w;
}
function _renderBitArray(val, prevVal){
  const bits=_bitWidth(Math.max(val, prevVal||0));
  let cells='';
  for(let i=bits-1;i>=0;i--){
    const bitVal=(val>>i)&1;
    const changed=prevVal!=null && bitVal!==((prevVal>>i)&1);
    const cls='bit-c '+(bitVal?'bit-on':'bit-off')+(changed?' bit-diff':'');
    const dly=prevVal==null?` style="animation-delay:${(bits-1-i)*20}ms"`:'';
    cells+=`<div class="${cls}"${dly}><div class="bit-i">${i}</div><div class="bit-v">${bitVal}</div></div>`;
  }
  return `<div class="bit-row">${cells}</div>`;
}
function _renderNdArray(data, shape, prevData){
  const nd=shape.length;
  const pd=Array.isArray(prevData)?prevData:null;
  if(nd<=2) return _render2D(nd===2?data:[data], nd===2?pd:(pd?[pd]:null));
  if(nd===3)
    return data.map((plane,p)=>
      `<div class="omat-plane"><div class="omat-lbl">▦ plano [${p}] · ${shape[1]}×${shape[2]}</div>${_render2D(plane, pd?pd[p]:null)}</div>`
    ).join('');
  if(nd===4)
    return data.map((block,b)=>
      `<div class="omat-block"><div class="omat-lbl omat-lbl-b">▣ bloque [${b}] · ${shape[1]}×${shape[2]}×${shape[3]}</div>`+
      block.map((plane,p)=>
        `<div class="omat-plane"><div class="omat-lbl">▦ [${b}][${p}]</div>${_render2D(plane, (pd&&pd[b])?pd[b][p]:null)}</div>`).join('')+
      `</div>`).join('');
  return `<pre class="omat-pre">${esc(JSON.stringify(data))}</pre>`;
}

function renderObjects(name,val){
  const el=document.getElementById('obBody');
  const {idx:activeIdx, key:activeKey}=_activeIdxForVar(name);
  // Diff against the last thing shown for this same variable, so the panel
  // reads as an animation (cells flash / slide on change) rather than a
  // static redraw — this is what makes stepping/looping through 1D/2D/3D/4D
  // data, and watching a sort reorder elements, legible frame-to-frame.
  const isSameVar=_objSnapshot.name===name;
  const prevVal=isSameVar?_objSnapshot.val:null;
  // Snapshot current cell positions BEFORE we overwrite the DOM — this is
  // the "First" of the FLIP technique, used below to slide reordered list
  // cells from their old spot to their new one instead of just popping in.
  let _oldCellRects=null;
  if(isSameVar){
    const oldCells=el.querySelectorAll('.ob-cell');
    if(oldCells.length) _oldCellRects=Array.from(oldCells).map(c=>c.getBoundingClientRect());
  }

  if(Array.isArray(val)){
    const shape=_listShape(val);
    const isListOfLists=val.length>0 && val.every(v=>Array.isArray(v));
    // A partition (e.g. "días") can coincidentally have equal-length groups
    // at some steps, which would otherwise look exactly like a regular
    // matrix and flip the view to a numeric grid right when it's most
    // interesting to watch as bins. Once a variable has been seen ragged
    // at least once, remember it and keep treating it as a partition —
    // sticky, so the view doesn't flicker between the two every step.
    if(isListOfLists && new Set(val.map(g=>g.length)).size>1) _knownRagged.add(name);
    const treatAsBins=isListOfLists && (_knownRagged.has(name) || !(shape && shape.length>=2));
    if(shape && shape.length>=2 && !treatAsBins){
      // ── Regular nested list (matrix/tensor built without numpy):
      //    reuse the same N-dim grid renderer as ndarrays ──
      const nd=shape.length;
      const dimWord=nd>=4?'4D':nd===3?'3D':'2D';
      const hdrTyp=`<span class="ob-hdr-type" style="background:#1a1542;color:#9b8fff">list</span>`;
      let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span>`+
        `<span class="ob-hdr-cnt">${dimWord} · ${shape.join('×')}</span></div>`;
      const prevData=Array.isArray(prevVal)?prevVal:null;
      h+=`<div class="ob-mat-wrap">${_renderNdArray(val, shape, prevData)}</div>`;
      el.innerHTML=h;
    } else if(treatAsBins){
      // ── List of variable-size groups (a partition — e.g. "días" in a
      //    bin-packing/scheduling search, buckets in a bucket sort, …):
      //    one column per group, items as chips that FLIP-slide between
      //    columns when the algorithm moves them. Generalizes "watch
      //    elements move" from a single array to grouped/partitioned data,
      //    reusing the exact same matching/slide machinery as the bars. ──
      const hdrTyp=`<span class="ob-hdr-type" style="background:#1a1542;color:#9b8fff">list</span>`;
      let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span><span class="ob-hdr-cnt">${val.length} grupos</span></div>`;
      const prevGroups=(Array.isArray(prevVal) && prevVal.length>0 && prevVal.every(v=>Array.isArray(v)))?prevVal:null;
      const flatOld=prevGroups?[].concat(...prevGroups):null;
      const flatNew=[].concat(...val);
      const srcIdx=flatOld?_matchOldIndices(flatOld,flatNew):null;
      const maxLen=Math.max(1,...val.map(g=>g.length));
      // Which group index(es) the CURRENT line is touching (e.g. dias[i],
      // dias[origen]) — same _active_subscripts machinery that draws the
      // sorting bars' claw, applied here to highlight the group(s) a
      // move/swap is comparing right now instead of a flat array's cells.
      const activeBins=new Set(_activeSubIdx(name));
      h+=`<div class="bins-wrap"><div class="bins-row">`;
      let flatPos=0;
      val.forEach((group,gi)=>{
        const binAct=activeBins.has(gi)?' bin-active':'';
        h+=`<div class="bin-col${binAct}">${activeBins.has(gi)?'<div class="bar-claw">▼</div>':''}`+
          `<div class="bin-hdr">Grupo ${gi} <span class="bin-cnt">(${group.length})</span></div>`+
          `<div class="bin-body" style="min-height:${Math.max(40,maxLen*30)}px">`;
        if(!group.length) h+=`<div class="bin-empty">vacío</div>`;
        group.forEach(item=>{
          const oldIdx=srcIdx?srcIdx[flatPos]:-1;
          const isMatched=oldIdx>=0;
          const isNew=flatOld!=null && !isMatched;
          const {cls,d}=obTypeInfo(item);
          const extraCls=isNew?' ob-cell-new':'';
          const styleAttr=isMatched?' style="animation:none"':
            (isNew?'':` style="animation-delay:${flatPos*25}ms"`);
          h+=`<div class="ob-cell bin-chip${extraCls}" data-srcidx="${oldIdx}"${styleAttr}><span class="${cls}">${d}</span></div>`;
          flatPos++;
        });
        h+=`</div></div>`;
      });
      h+=`</div></div>`;
      el.innerHTML=h;
    } else {
      // ── Flat / irregular list: bar chart (numeric — sorting-visualizer
      //    style, so you can watch ANY algorithm's comparisons/swaps) or
      //    a horizontal cells grid otherwise ──
      const allNum=val.length>0 && val.every(v=>typeof v==='number' && isFinite(v));
      const useBars=allNum && val.length<=40 && _listViewMode!=='cards';
      const hdrTyp=`<span class="ob-hdr-type" style="background:#1a1542;color:#9b8fff">list</span>`;
      const idxInfo=activeIdx!==null?`<span style="font-size:10px;color:#c77dbb;margin-left:6px">→ [${activeIdx}]</span>`:'';
      const viewBtn=allNum?`<button class="obtn" onclick="toggleListView()" title="Cambiar vista">${useBars?'🔢 tarjetas':'📊 barras'}</button>`:'';
      let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span><span class="ob-hdr-cnt">${val.length} elem</span>${idxInfo}${viewBtn}</div>`;
      if(val.length===0){
        h+=`<div class="ob-ph">Lista vacía []</div>`;
      } else {
        const prevArr=Array.isArray(prevVal)?prevVal:null;
        // Match each new element back to where it used to live (by value).
        // Matched → the same element, just relocated: no flash, it will
        // FLIP-slide to its new cell below. Unmatched (and a previous
        // render existed) → a genuinely new/changed value: pop + green flash.
        const srcIdx=prevArr?_matchOldIndices(prevArr,val):null;
        if(useBars){
          // Indices the current line is actively comparing/touching
          // (a[i], a[i+1], …), from the backend's per-line subscript map —
          // this is what draws the "claw" over the bars being compared.
          const activeSet=new Set(_activeSubIdx(name));
          const maxAbs=Math.max(1,...val.map(v=>Math.abs(v)));
          const MAXH=110;
          h+=`<div class="bars-wrap"><div class="bars-row">`;
          val.forEach((item,i)=>{
            const isAct=activeIdx===i||activeSet.has(i);
            const oldIdx=srcIdx?srcIdx[i]:-1;
            const isMatched=oldIdx>=0;
            const isNew=prevArr!=null && !isMatched;
            const barH=Math.max(6,Math.round(Math.abs(item)/maxAbs*MAXH));
            const extraCls=(isAct?' bar-active':'')+(isNew?' ob-cell-new':'')+(item<0?' bar-neg':'');
            const styleAttr=isMatched?' style="animation:none"':
              ((isAct||isNew)?'':` style="animation-delay:${i*30}ms"`);
            h+=`<div class="ob-cell bar-cell${extraCls}" data-idx="${i}" data-srcidx="${oldIdx}"${styleAttr}>
              ${isAct?'<div class="bar-claw">▼</div>':''}
              <div class="bar-val">${_matCell(item)}</div>
              <div class="bar-fill" style="height:${barH}px"></div>
              <div class="bar-idx">${i}</div></div>`;
          });
          h+=`</div>`;
          // Solo celebra una TRANSICION real a ordenado (no lo estaba en el
          // paso anterior de ESTA MISMA variable, y ahora si) -- un simple
          // "esta ordenada en este instante" salia en listas que nunca
          // tuvieron nada que ver con ordenar (fitness, distancias, feromona...)
          // con tal de que sus numeros ya vinieran en orden creciente.
          const isSorted=val.length>1 && val.every((v,i)=>i===0||val[i-1]<=v);
          const wasSorted=prevArr && prevArr.length>1 && prevArr.every((v,i)=>i===0||prevArr[i-1]<=v);
          if(isSorted && prevArr && !wasSorted) h+=`<div class="bars-sorted">✓ ¡Ordenado!</div>`;
          h+=`</div>`;
        } else {
          h+=`<div class="ob-grid">`;
          val.forEach((item,i)=>{
            const {t,cls,d,bin}=obTypeInfo(item);
            const isAct=activeIdx===i;
            const oldIdx=srcIdx?srcIdx[i]:-1;
            const isMatched=oldIdx>=0;
            const isNew=prevArr!=null && !isMatched;
            const extraCls=isAct?'ob-cell-act':(isNew?'ob-cell-new':'');
            const styleAttr=isMatched?' style="animation:none"':
              ((isAct||isNew)?'':` style="animation-delay:${i*40}ms"`);
            const binLine=bin!=null?`<div class="ob-ct" style="color:#7fb0e0">0b${bin}</div>`:'';
            h+=`<div class="ob-cell ${extraCls}" data-idx="${i}" data-srcidx="${oldIdx}"${styleAttr}>
              <div class="ob-ci">${isAct?'▶':''} [${i}]</div>
              <div class="ob-cv ${cls}">${d}</div>${binLine}
              <div class="ob-ct">${t}</div></div>`;
          });
          h+=`</div>`;
        }
      }
      el.innerHTML=h;
    }

  } else if(typeof val==='number' && Number.isInteger(val) && val>=0 && val<=65535){
    // ── Bitmask int: render as a 1D array of bits (MSB→LSB), flashing the
    //    bits that flipped since the last frame — e.g. mascara | ACTOR_n ──
    const hdrTyp=`<span class="ob-hdr-type" style="background:#0d1f33;color:#7fb0e0">bitmask</span>`;
    let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span>`+
      `<span class="ob-hdr-cnt">decimal ${val} · 0b${val.toString(2)}</span></div>`;
    const prevN=(isSameVar && typeof prevVal==='number')?prevVal:null;
    h+=`<div class="ob-mat-wrap">${_renderBitArray(val, prevN)}</div>`;
    el.innerHTML=h;

  } else if(typeof val==='object'&&val?.__set__){
    // ── Set: cells grid ──────────────────────────
    const items=val.values||[];
    const hdrTyp=`<span class="ob-hdr-type" style="background:#1a2a1a;color:#80c080">set</span>`;
    let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span><span class="ob-hdr-cnt">${items.length} elem</span></div>`;
    if(items.length===0){
      h+=`<div class="ob-ph">Set vacío {}</div>`;
    } else {
      h+=`<div class="ob-grid">`;
      items.forEach((item,i)=>{
        const {t,cls,d}=obTypeInfo(item);
        h+=`<div class="ob-cell" data-idx="${i}" style="animation-delay:${i*40}ms">
          <div class="ob-ci" style="background:linear-gradient(135deg,#27ae60,#1e8449)">{${i}}</div>
          <div class="ob-cv ${cls}">${d}</div>
          <div class="ob-ct">${t}</div></div>`;
      });
      h+=`</div>`;
    }
    el.innerHTML=h;

  } else if(typeof val==='object'&&val?.__matrix__){
    // ── ndarray: render by dimensions (2D grid, 3D planes, 4D blocks) ──
    const shape=val.shape||[], dtype=val.dtype||'';
    const hdrTyp=`<span class="ob-hdr-type" style="background:#1a0a2a;color:#c77dbb">ndarray</span>`;
    const nd=shape.length;
    const dimWord=nd>=4?'4D':nd===3?'3D':nd===2?'2D':nd+'D';
    let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span>`+
      `<span class="ob-hdr-cnt">${dimWord} · ${shape.join('×')} · ${esc(dtype)}</span></div>`;
    const prevData=(prevVal && prevVal.__matrix__)?prevVal.data:null;
    h+=`<div class="ob-mat-wrap">${_renderNdArray(val.data||[], shape, prevData)}</div>`;
    el.innerHTML=h;

  } else if(typeof val==='object'&&val?.__obj__){
    // ── Class instance: attribute list, with list/ndarray attributes
    //    rendered inline (e.g. self.matrix on a class) so their full
    //    1D/2D/3D/4D animated view is reachable even when the array lives
    //    inside an object instead of being a bare top-level variable. ──
    const attrs=Object.entries(val.attrs||{});
    const hdrTyp=`<span class="ob-hdr-type" style="background:#0d2a3a;color:#4ec9b0">${esc(val.type||'object')}</span>`;
    let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span><span class="ob-hdr-cnt">${attrs.length} attrs</span></div>`;
    if(!attrs.length){
      h+=`<div class="ob-ph">Sin atributos públicos</div>`;
    } else {
      const prevAttrs=(prevVal && prevVal.__obj__)?(prevVal.attrs||{}):null;
      h+='<div class="ob-attrs">';
      attrs.forEach(([ak,av])=>{
        h+=`<div class="ob-attr-row"><div class="ob-attr-k">.${esc(ak)}</div><div class="ob-attr-v">`;
        const shape=Array.isArray(av)?_listShape(av):null;
        if(shape && shape.length>=2){
          const pd=(prevAttrs && Array.isArray(prevAttrs[ak]))?prevAttrs[ak]:null;
          h+=`<div class="ob-mat-wrap ob-mat-wrap-nested">${_renderNdArray(av, shape, pd)}</div>`;
        } else if(av && typeof av==='object' && av.__matrix__){
          const pd=(prevAttrs && prevAttrs[ak] && prevAttrs[ak].__matrix__)?prevAttrs[ak].data:null;
          h+=`<div class="ob-mat-wrap ob-mat-wrap-nested">${_renderNdArray(av.data||[], av.shape||[], pd)}</div>`;
        } else if(av && typeof av==='object' && av.__obj__){
          h+=`<span class="ob-td-val">${esc(av.type||'object')}(…)</span>`;
        } else if(Array.isArray(av) || (av && typeof av==='object')){
          const n=Array.isArray(av)?av.length:Object.keys(av).length;
          h+=`<span class="ob-td-val">${Array.isArray(av)?'[list·'+n+']':'{dict·'+n+'}'}</span>`;
        } else {
          const {t,cls,d}=obTypeInfo(av);
          h+=`<span class="ob-td-val ${cls}">${d}</span><span class="ob-td-typ" style="margin-left:6px">${t}</span>`;
        }
        h+='</div></div>';
      });
      h+='</div>';
    }
    el.innerHTML=h;

  } else if(typeof val==='object'&&val!==null){
    // ── Dict: key → value table ───────────────────
    const entries=Object.entries(val);
    const hdrTyp=`<span class="ob-hdr-type" style="background:#2a1a00;color:#f0c060">dict</span>`;
    const keyInfo=activeKey!==null?`<span style="font-size:10px;color:#c77dbb;margin-left:6px">→ "${activeKey}"</span>`:'';
    let h=`<div class="ob-hdr">${hdrTyp}<span class="ob-hdr-name">${esc(name)}</span><span class="ob-hdr-cnt">${entries.length} entradas</span>${keyInfo}</div>`;
    h+=`<table class="ob-table"><thead><tr>
      <th style="width:14px">#</th><th>clave</th><th>valor</th><th>tipo</th>
    </tr></thead><tbody>`;
    const prevDict=(prevVal && typeof prevVal==='object' && !Array.isArray(prevVal) &&
      !prevVal.__matrix__ && !prevVal.__set__) ? prevVal : null;
    entries.forEach(([k,v],i)=>{
      const {t,cls,d,bin}=obTypeInfo(v);
      const isAct=activeKey===k||activeIdx===i;
      const changed=prevDict!=null && (k in prevDict) && !_deepEq(v, prevDict[k]);
      const binBadge=bin!=null?`<span class="ob-td-bin">0b${bin}</span>`:'';
      const rowCls=isAct?'ob-tr-act':(changed?'ob-tr-diff':'');
      h+=`<tr class="${rowCls}" data-key="${esc(k)}" style="animation-delay:${i*45}ms">
        <td class="ob-td-idx">${isAct?'▶':''} ${i}</td>
        <td class="ob-td-key">"${esc(k)}"</td>
        <td class="ob-td-val ${cls}">${d}${binBadge}</td>
        <td class="ob-td-typ">${t}</td></tr>`;
    });
    h+=`</tbody></table>`;
    el.innerHTML=h;

  } else {
    el.innerHTML=`<div class="ob-ph">${esc(String(val))}</div>`;
  }
  _objSnapshot={name, val};
  autoLayout();
  _flipCells(el, _oldCellRects);
}

/* "Invert + Play" half of FLIP: for every new cell carrying a data-srcidx,
   jump it back to where its old counterpart was (via an un-transitioned
   transform), then release the transform with a transition — the browser
   renders that as the cell sliding from its old grid position to its new
   one. This is what makes a sort/reorder look like elements moving instead
   of the grid just repainting. */
function _flipCells(el, oldRects){
  if(!oldRects) return;
  requestAnimationFrame(()=>{
    el.querySelectorAll('.ob-cell[data-srcidx]').forEach(cellEl=>{
      const oldIdx=parseInt(cellEl.getAttribute('data-srcidx'),10);
      if(oldIdx<0 || !oldRects[oldIdx]) return;
      const newRect=cellEl.getBoundingClientRect();
      const oldRect=oldRects[oldIdx];
      const dx=oldRect.left-newRect.left, dy=oldRect.top-newRect.top;
      if(Math.abs(dx)<1 && Math.abs(dy)<1) return;
      cellEl.style.transition='none';
      cellEl.style.transform=`translate(${dx}px,${dy}px)`;
      void cellEl.getBoundingClientRect(); // force reflow before releasing
      requestAnimationFrame(()=>{
        cellEl.style.transition='transform .5s cubic-bezier(.22,.8,.25,1)';
        cellEl.style.transform='translate(0,0)';
        cellEl.addEventListener('transitionend',()=>{
          cellEl.style.transition=''; cellEl.style.transform='';
        },{once:true});
      });
    });
  });
}

/* ──────────── Output panel (classified) ──────────── */
/* ── Smart output parser ── */
function _tryParseNumList(s){
  // "[1, 2, 3]" or "(1, 2, 3)" → [1,2,3] if all numeric
  const m=s.match(/^[\[\(](.*?)[\]\)]$/s);
  if(!m) return null;
  const parts=m[1].split(',').map(p=>p.trim()).filter(p=>p.length>0);
  if(parts.length===0) return null;
  const nums=parts.map(p=>parseFloat(p));
  if(nums.some(isNaN)) return null;
  return nums;
}

function _tryParseStrList(s){
  // ["a","b","c"] or ['a','b'] → ['a','b','c']
  const m=s.match(/^[\[\(](.*?)[\]\)]$/s);
  if(!m) return null;
  const raw=m[1].trim();
  if(!raw) return [];
  // Check first item starts with quote
  if(!/^['"]/.test(raw)) return null;
  const parts=[];
  const re=/['"]([^'"]*)['"]/g; let mx;
  while((mx=re.exec(raw))!==null) parts.push(mx[1]);
  return parts.length>0?parts:null;
}

function _tryParseDict(s){
  // {'key': val, ...} → [{k,v},...] where v is number or string
  const m=s.match(/^\{(.*)\}$/s);
  if(!m) return null;
  const pairs=[];
  const re=/['"]?(\w[\w\s]*)['"]?\s*:\s*(-?\d+(?:\.\d+)?|['"][^'"]*['"])/g;
  let mx;
  while((mx=re.exec(m[1]))!==null){
    const kk=mx[1].trim();
    const vv=mx[2].trim();
    const num=parseFloat(vv);
    pairs.push({k:kk, v:isNaN(num)?vv.replace(/['"]/g,''):num, isNum:!isNaN(num)});
  }
  return pairs.length>0?pairs:null;
}

function _renderVizCard(line, isNew, idx){
  const t=line.trim();
  const anim=isNew?'':`style="animation:none"`;
  const typeTag=(label,bg,fg)=>
    `<span class="oviz-type" style="background:${bg};color:${fg}">${label}</span>`;
  const rawBar=(raw)=>
    `<div class="oviz-raw">${esc(raw.length>80?raw.slice(0,80)+'…':raw)}</div>`;

  if(!t) return ''; // skip blank lines

  // ── Boolean ──
  if(t==='True')
    return `<div class="oviz" ${anim} style="border-color:#27ae60">
      ${rawBar(line)}<div class="oviz-bool" style="background:#0d1e0d">
        <div class="oviz-bool-dot" style="background:#27ae60;box-shadow:0 0 8px #27ae60"></div>
        <span class="oviz-bool-lbl" style="color:#27ae60">True</span>
        ${typeTag('bool','#0d3a0d','#27ae60')}</div></div>`;
  if(t==='False')
    return `<div class="oviz" ${anim} style="border-color:#c0392b">
      ${rawBar(line)}<div class="oviz-bool" style="background:#1e0d0d">
        <div class="oviz-bool-dot" style="background:#c0392b;box-shadow:0 0 8px #c0392b"></div>
        <span class="oviz-bool-lbl" style="color:#c0392b">False</span>
        ${typeTag('bool','#3a0d0d','#c0392b')}</div></div>`;
  if(t==='None')
    return `<div class="oviz" ${anim} style="border-color:#555">
      ${rawBar(line)}<div class="oviz-text" style="background:#111"><span style="color:#666;font-size:14px;font-family:monospace">None ∅</span></div></div>`;

  // ── Pure number (int or float) ──
  const numMatch=t.match(/^(-?\d+(?:\.\d+)?)$/);
  if(numMatch){
    const n=parseFloat(numMatch[1]);
    const isInt=Number.isInteger(n);
    const col=isInt?'#4ec9b0':'#4fc3a1';
    const pct=Math.min(Math.abs(n)/100*100,100);
    return `<div class="oviz" ${anim} style="border-color:${col}">
      ${rawBar(line)}<div class="oviz-num">
        ${typeTag(isInt?'int':'float',isInt?'#0d3a47':'#1a3a2a',col)}
        <span class="oviz-numval" style="color:${col}">${n}</span>
        <div class="oviz-numbar" style="width:${pct}%;background:linear-gradient(90deg,${col},${col}88)"></div>
      </div></div>`;
  }

  // ── Inline numbers (space-separated: "1 3 5 7 9") ──
  const spacedNums=t.split(/\s+/).map(p=>parseFloat(p));
  if(spacedNums.length>1&&spacedNums.every(n=>!isNaN(n))){
    const max=Math.max(...spacedNums.map(Math.abs))||1;
    const colors=['#667eea','#c77dbb','#4ec9b0','#f0c060','#e06c75','#4fc3a1'];
    const bars=spacedNums.map((n,i)=>{
      const pct=Math.abs(n)/max*100;
      const c=colors[i%colors.length];
      return `<div class="ovb-col" style="animation-delay:${i*35}ms">
        <span class="ovb-val" style="color:${c}">${n}</span>
        <div class="ovb-bar" style="height:${pct}%;background:${c};animation-delay:${i*35}ms"></div>
        <span class="ovb-lbl">${i}</span></div>`;
    }).join('');
    return `<div class="oviz" ${anim} style="border-color:#667eea">
      ${rawBar(line)}${typeTag('nums','#1a1542','#9b8fff')}
      <div class="oviz-bars">${bars}</div></div>`;
  }

  // ── List of numbers: [1,9,25,...] ──
  const numList=_tryParseNumList(t);
  if(numList&&numList.length>0){
    const max=Math.max(...numList.map(Math.abs))||1;
    const colors=['#667eea','#c77dbb','#4ec9b0','#f0c060','#e06c75','#4fc3a1','#569cd6','#ce9178'];
    const bars=numList.map((n,i)=>{
      const pct=Math.abs(n)/max*100;
      const c=colors[i%colors.length];
      return `<div class="ovb-col" style="animation-delay:${i*30}ms">
        <span class="ovb-val" style="color:${c}">${n}</span>
        <div class="ovb-bar" style="height:${pct}%;background:${c};animation-delay:${i*30}ms"></div>
        <span class="ovb-lbl">[${i}]</span></div>`;
    }).join('');
    return `<div class="oviz" ${anim} style="border-color:#667eea">
      ${rawBar(line)}${typeTag('list','#1a1542','#9b8fff')}
      <div class="oviz-bars">${bars}</div></div>`;
  }

  // ── List of strings: ['a','b',...] ──
  const strList=_tryParseStrList(t);
  if(strList){
    const chips=strList.map((s,i)=>
      `<span class="oviz-chip" style="animation-delay:${i*35}ms">
        <span class="oviz-chip-idx">[${i}]</span>${esc(s)}</span>`).join('');
    return `<div class="oviz" ${anim} style="border-color:#3b3470">
      ${rawBar(line)}${typeTag('list','#1a1542','#9b8fff')}
      <div class="oviz-chips">${chips}</div></div>`;
  }

  // ── Dict with numeric values → horiz bar chart ──
  const dictPairs=_tryParseDict(t);
  if(dictPairs&&dictPairs.some(p=>p.isNum)){
    const numPairs=dictPairs.filter(p=>p.isNum);
    const max=Math.max(...numPairs.map(p=>Math.abs(p.v)))||1;
    const rows=dictPairs.map((p,i)=>{
      const pct=p.isNum?Math.abs(p.v)/max*100:0;
      const col=`hsl(${200+i*37},70%,60%)`;
      return `<div class="ovhb-row" style="animation-delay:${i*40}ms">
        <span class="ovhb-key">${esc(String(p.k))}</span>
        <div class="ovhb-track">
          <div class="ovhb-fill" style="width:${pct}%;background:${col}"></div></div>
        <span class="ovhb-val">${esc(String(p.v))}</span></div>`;
    }).join('');
    return `<div class="oviz" ${anim} style="border-color:#f0c060">
      ${rawBar(line)}${typeTag('dict','#2a1a00','#f0c060')}
      <div class="oviz-hbars">${rows}</div></div>`;
  }

  // ── Set: {1,2,3} ──
  if(/^\{[^:]+\}$/.test(t)&&!t.includes(':')){
    const items=t.slice(1,-1).split(',').map(s=>s.trim()).filter(Boolean);
    const chips=items.map((s,i)=>
      `<span class="oviz-setitem" style="animation-delay:${i*35}ms">${esc(s)}</span>`).join('');
    return `<div class="oviz" ${anim} style="border-color:#3a6060">
      ${rawBar(line)}${typeTag('set','#0d2020','#4ec9b0')}
      <div class="oviz-set">${chips}</div></div>`;
  }

  // ── Fallback: styled text ──
  // Try to color numbers inline
  const html=esc(line).replace(/(-?\d+(?:\.\d+)?)/g,
    '<span style="color:#4ec9b0;font-weight:600">$1</span>');
  const isNumMix=/\d/.test(t);
  const bc=isNumMix?'#2a2a3a':'#1e1e2e';
  return `<div class="oviz" ${anim} style="border-color:${bc}">
    <div class="oviz-fallback">
      <span class="oviz-falltext">${html}</span></div></div>`;
}

/* bracket balance of a string ('[' +1, ']' -1) */
function _bal(s){ let b=0; for(const c of s){ if(c==='[')b++; else if(c===']')b--; } return b; }

/* Group raw output lines into blocks: normal lines + multi-line matrix blocks
   (numpy prints 2D arrays across several lines). A matrix block keeps ALL its
   rows together so every element is shown, not fragmented into separate cards. */
function _groupOutput(lines){
  const blocks=[];
  for(let i=0;i<lines.length;i++){
    const ln=lines[i];
    const pos=ln.indexOf('[[');
    if(pos>=0){
      const prefix=ln.slice(0,pos).trim();
      let buf=ln.slice(pos), bal=_bal(buf), j=i;
      while(bal>0 && j+1<lines.length){ j++; buf+='\n'+lines[j]; bal+=_bal(lines[j]); }
      if(prefix) blocks.push({type:'line', text:prefix});
      blocks.push({type:'matrix', text:buf});
      i=j;
    } else {
      blocks.push({type:'line', text:ln});
    }
  }
  return blocks;
}

/* Render a numpy 2D array block as one grid card showing every element. */
function _renderMatrixCard(text, isNew){
  const anim=isNew?'':`style="animation:none"`;
  // 3D+ array: keep numpy's structured layout (shows planes/blocks, all elems)
  if(text.indexOf('[[[')>=0){
    return `<div class="oviz" ${anim} style="border-color:#3a6ea5">
      <div class="oviz-raw">array N-D — todos los elementos</div>
      <pre class="omat-pre">${esc(text)}</pre></div>`;
  }
  const rowMatches=[...text.matchAll(/\[([^\[\]]+)\]/g)];
  const rows=rowMatches.map(m=>m[1].trim().split(/[\s,]+/).filter(x=>x!==''));
  if(!rows.length || rows.some(r=>r.length===0)){
    return `<div class="oviz" ${anim} style="border-color:#3a6ea5">
      <div class="oviz-raw">matriz</div>
      <pre class="omat-pre">${esc(text)}</pre></div>`;
  }
  const ncol=Math.max(...rows.map(r=>r.length));
  let cells='';
  rows.forEach((r,ri)=>{
    r.forEach((v,ci)=>{
      cells+=`<div class="omat-c" style="animation-delay:${(ri*ncol+ci)*22}ms">${esc(v)}</div>`;
    });
    for(let k=r.length;k<ncol;k++) cells+=`<div class="omat-c omat-pad">·</div>`;
  });
  return `<div class="oviz" ${anim} style="border-color:#3a6ea5">
    <div class="oviz-raw">matriz ${rows.length}×${ncol} — todos los elementos</div>
    <div class="omat" style="grid-template-columns:repeat(${ncol},minmax(28px,1fr))">${cells}</div></div>`;
}

function setOutput(out){
  const el=document.getElementById('outBody');
  if(!out||!out.trim()){
    el.innerHTML='<div class="out-empty">Sin output todavía...</div>';
    lastOut=''; autoLayout(); return;
  }
  if(out===lastOut) return;
  const prevLines=lastOut?lastOut.split('\n').filter(l=>l!==''):[];
  const lines=out.split('\n').filter(l=>l!=='');
  const blocks=_groupOutput(lines);
  const prevBlocks=_groupOutput(prevLines).length;
  el.innerHTML=blocks.map((b,i)=> b.type==='matrix'
      ? _renderMatrixCard(b.text, i>=prevBlocks)
      : _renderVizCard(b.text, i>=prevBlocks, i)).join('');
  el.scrollTop=el.scrollHeight;
  lastOut=out;
  autoLayout();
}

/* ──────────── Auto layout ──────────── */
function autoLayout(){
  const right = document.querySelector('.p-right');
  if(!right) return;
  // discount the fixed header, the narrator bar and the drag handle
  const expTitle = right.querySelector('.ptitle-exp');
  const narBar   = document.getElementById('narrator');
  const fixedH = (expTitle?expTitle.offsetHeight:0) + (narBar?narBar.offsetHeight:0) + 6;
  const totalH = right.clientHeight - fixedH;

  // ── Count content with CORRECT selectors ────────
  const outN  = document.getElementById('outBody').querySelectorAll('.oviz').length || 1;
  const frN   = document.getElementById('frBody').querySelectorAll('.vwidget').length  || 1;
  const frGrp = document.getElementById('frBody').querySelectorAll('.fgtitle').length  || 1;
  const obN   = document.getElementById('obBody').querySelectorAll('.ob-cell').length  || 0;
  const obTr  = document.getElementById('obBody').querySelectorAll('tbody tr').length  || 0;
  const hasObj = obN > 0 || obTr > 0 ||
                 document.getElementById('obBody').querySelectorAll('.ob-hdr').length > 0;

  const CARD=90, WGT=50, GRP=22, TITLE=30, PAD=8;

  // ── Ideal heights for each section ──────────────
  const outIdeal = TITLE + outN * CARD + PAD;
  const frIdeal  = TITLE + frGrp * GRP + frN * WGT + PAD;
  const obIdeal  = hasObj
    ? TITLE + (obN + obTr) * CARD + PAD
    : Math.max(80, Math.floor(frIdeal * 0.7));
  const botIdeal = Math.max(frIdeal, obIdeal);

  const desired = outIdeal + botIdeal;
  const MIN_OUT = TITLE + 30, MIN_BOT = TITLE + 50;

  // ── Vertical split (output vs bottom) ───────────
  let outH = desired <= totalH
    ? outIdeal
    : Math.round((outIdeal / desired) * totalH);

  outH = Math.max(MIN_OUT, Math.min(outH, Math.floor(totalH * 0.65)));
  if(totalH - outH < MIN_BOT) outH = totalH - MIN_BOT;
  outH = Math.max(MIN_OUT, outH);

  const ow = document.getElementById('outWrap');
  ow.style.height = outH + 'px';
}

window.addEventListener('resize', autoLayout);

/* ──────────── Diff ──────────── */
function computeDiff(prev, cur){
  const ch=new Set(), nw=new Set();
  if(!prev) return{ch,nw};
  const pv={};
  prev.frames.forEach(f=>Object.assign(pv,f.variables));
  cur.frames.forEach(f=>{
    Object.entries(f.variables).forEach(([k,v])=>{
      if(!(k in pv)) nw.add(k);
      else if(JSON.stringify(v)!==JSON.stringify(pv[k])) ch.add(k);
    });
  });
  return{ch,nw};
}

/* ──────────── Line numbers ──────────── */
function renderLineNums(){
  const lines=document.getElementById('codeInput').value.split('\n');
  document.getElementById('lineNums').innerHTML=
    lines.map((_,i)=>{
      const n=i+1, has=bps.has(n);
      return `<div class="ln-row ${has?'has-bp':''}" onclick="togBP(${n})">${has?'<span class="bp-dot"></span>':''}${n}</div>`;
    }).join('');
}

function togBP(n){
  bps.has(n)?bps.delete(n):bps.add(n);
  renderLineNums();
  // Re-render exec to reflect BP markers
  if(steps.length){
    const pLine=cur>0?steps[cur-1].line:-1;
    const nLine=cur>=0?steps[cur].line:(steps[0]?.line??-1);
    renderExec(pLine,nLine);
  }
}

/* ──────────── Draggable right divider (manual override) ──────────── */
(()=>{
  const hd=document.getElementById('hDrag'), ow=document.getElementById('outWrap'), pr=document.querySelector('.p-right');
  let dragging=false, sy=0, sh=0;
  hd.addEventListener('mousedown',e=>{
    dragging=true; sy=e.clientY; sh=ow.getBoundingClientRect().height;
    ow.style.transition='none'; // disable smooth while dragging
    e.preventDefault();
  });
  document.addEventListener('mousemove',e=>{
    if(!dragging) return;
    const d=e.clientY-sy;
    const h=Math.max(60,Math.min(sh+d, pr.getBoundingClientRect().height-100));
    ow.style.height=h+'px';
  });
  document.addEventListener('mouseup',()=>{
    if(dragging){ dragging=false; ow.style.transition=''; }
  });
})();

/* ──────────── Sync line nums scroll ──────────── */
document.getElementById('codeInput').addEventListener('scroll',()=>{
  document.getElementById('lineNums').scrollTop=document.getElementById('codeInput').scrollTop;
});

/* ──────────── Auto-run on paste ──────────── */
document.getElementById('codeInput').addEventListener('paste',()=>{
  setTimeout(()=>{ renderLineNums(); runCode(); }, 150);
});

/* ──────────── Debounce on typing → show banner ──────────── */
let _debTimer=null;
document.getElementById('codeInput').addEventListener('input',()=>{
  renderLineNums();
  // If code changed after a run, mark as stale
  if(steps.length){ markStale(); }
  clearTimeout(_debTimer);
  _debTimer=setTimeout(()=>{
    if(document.getElementById('codeInput').value.trim()) runCode();
  }, 1800);
});

function markStale(){
  steps=[]; cur=-1; prev=null;
  showBanner(true);
  updBtns();
}

function showBanner(show){
  const b=document.getElementById('runBanner');
  const btn=document.getElementById('bFwd').closest ? document.getElementById('bFwd') : null;
  const runBtn=document.querySelector('.btn-run');
  b.style.display=show?'flex':'none';
  if(show){ runBtn.classList.add('btn-run-pulse'); }
  else     { runBtn.classList.remove('btn-run-pulse'); }
}

/* ──────────── Keyboard ──────────── */
document.addEventListener('keydown',e=>{
  // Ctrl+Enter runs the code from anywhere (global)
  if(e.ctrlKey&&e.key==='Enter'){e.preventDefault();runCode();return;}
  const ae=document.activeElement;
  const inTA=ae&&ae.id==='codeInput';
  if(inTA){
    if(e.key==='Tab'){e.preventDefault();const t=e.target,s=t.selectionStart;t.value=t.value.slice(0,s)+'    '+t.value.slice(t.selectionEnd);t.selectionStart=t.selectionEnd=s+4;renderLineNums();}
    if(e.ctrlKey&&e.key==='b'){e.preventDefault();const ln=t_curLine();if(ln)togBP(ln);}
    return;
  }
  // Don't hijack typing/navigation keys while a form control has focus
  const tag=ae?ae.tagName:'';
  if(tag==='INPUT'||tag==='SELECT'||tag==='TEXTAREA'||(ae&&ae.isContentEditable)) return;
  if(e.code==='Space'){e.preventDefault();goFwd();}
  if(e.code==='Backspace'){e.preventDefault();goBack();}
  if(e.ctrlKey&&e.code==='Home'){e.preventDefault();goFirst();}
  if(e.ctrlKey&&e.code==='End'){e.preventDefault();goLast();}
});

function t_curLine(){
  const t=document.getElementById('codeInput');
  return t.value.slice(0,t.selectionStart).split('\n').length;
}

/* ──────────── Misc ──────────── */
function updBtns(){
  const none=!steps.length, atS=cur<=0, atE=cur>=steps.length-1;
  document.getElementById('bFirst').disabled=none||atS;
  document.getElementById('bBack').disabled=none||atS;
  document.getElementById('bFwd').disabled=none||atE;
  document.getElementById('bLast').disabled=none||atE;
  document.getElementById('bLoop').disabled=none;
}
function setSt(t){document.getElementById('cstatus').textContent=t;}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

function loadEx(){
  const idx=parseInt(document.getElementById('exSel').value);
  document.getElementById('codeInput').value=EX[idx].code;
  renderLineNums();
  document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
  // Auto-run the selected example immediately
  runCode();
  _masterSyncFromDropdown(idx);
}

