/* ──────────── Calendario del plan de estudio (AO → RA → AS) ──────────────
   No es un temario guiado más: es un panel de seguimiento. Muestra el plan
   de 21 días (10-30 agosto 2026) y, sobre todo, un banner SIEMPRE visible
   cuando hay temas pendientes para HOY, con un botón directo para ir a
   ellos. El progreso de los días de contenido (AO/RA/AS) NO se marca a
   mano: se lee directamente de los localStorage reales de cada Modo
   Maestro (pyvizMasterAoProgress/Ra/As), así que refleja lo que el alumno
   de verdad completó, no lo que dice haber hecho. Los días de repaso
   mezclado (sin temario propio) sí usan un check manual, guardado aparte.

   Rangos de índice recalculados (2026-08-12) tras aplanar el temario: cada
   pregunta pasó a ser su PROPIO tema (AO 41→164, RA 35→140, AS 21→84,
   ver [[project-master-ao-batches]] / [[project-razonamiento-aproximado]] /
   [[project-master-as]] en memoria) — cada rango viejo [a,b] se expande a
   [4a, 4b+3] para cubrir exactamente los mismos temas originales, ahora
   con sus 4 preguntas cada uno. Verificado sin huecos ni solapes. */
const CAL_PLAN = [
  {y:2026,m:7,d:10, phase:'ao', range:[0,35],   label:'Ordenación + AG1: Divide y Vencerás, Voraz, Backtracking, DP'},
  {y:2026,m:7,d:11, phase:'ao', range:[36,55],  label:'VC3: Programación lineal, TSP, caminos más cortos, A*, BFS/DFS'},
  {y:2026,m:7,d:12, phase:'ao', range:[56,71],  label:'Ramificación y Poda, Mochila, El gradiente, Descenso del gradiente'},
  {y:2026,m:7,d:13, phase:'ao', range:[72,87],  label:'Variantes del gradiente, P/NP, AG2: asignación de tareas y descenso práctico'},
  {y:2026,m:7,d:14, phase:'ao', range:[88,107], label:'VC5: heurística vs metaheurística, búsqueda aleatoria/local, tabú, recocido'},
  {y:2026,m:7,d:15, phase:'ao', range:[108,127],label:'VC5: multiarranque, GRASP, ACO + AG3: swiss42 y ACO-TSP'},
  {y:2026,m:7,d:16, phase:'ao', range:[128,147],label:'AG: representación, población, fitness, selección, cruce'},
  {y:2026,m:7,d:17, phase:'ao', range:[148,163],label:'AG: mutación, elitismo, Algoritmo Genético completo y aplicado a TSP'},
  {y:2026,m:7,d:18, phase:'rp', range:null,     label:'Repaso mezclado SOLO-AO (164 preguntas entrelazadas)'},

  {y:2026,m:7,d:19, phase:'ra', range:[0,35],   label:'Incertidumbre clásica: Bayes, Factores de Certeza, Dempster-Shafer'},
  {y:2026,m:7,d:20, phase:'ra', range:[36,51],  label:'Lógica Borrosa: conjuntos, soporte/núcleo, operadores, principio de extensión'},
  {y:2026,m:7,d:21, phase:'ra', range:[52,67],  label:'T-normas/T-conormas, relaciones, composición max-min, representación del conocimiento'},
  {y:2026,m:7,d:22, phase:'ra', range:[68,83],  label:'Cercas semánticas, razonamiento aproximado, Modus Ponens Generalizado, familias S/R/QL'},
  {y:2026,m:7,d:23, phase:'ra', range:[84,99],  label:'Modus Tollens, tipos de proposiciones borrosas, arquitectura de control, Mamdani'},
  {y:2026,m:7,d:24, phase:'ra', range:[100,119],label:'Desborrosificación, Takagi-Sugeno, CLIPS: sintaxis, coche, frutas'},
  {y:2026,m:7,d:25, phase:'ra', range:[120,139],label:'FuzzyCLIPS: Factores de Certeza, coche_cer, conjuntos borrosos, X1X2→Y, desborrosificación'},
  {y:2026,m:7,d:26, phase:'rp', range:null,     label:'Repaso mezclado SOLO-RA (140 preguntas entrelazadas)'},

  {y:2026,m:7,d:27, phase:'as', range:[0,27],   label:'Cap1: CRISP-DM, tipos de aprendizaje, normalización, outliers, imputación, selección de atributos'},
  {y:2026,m:7,d:28, phase:'as', range:[28,59],  label:'Cap2: validación, ajuste de parámetros, evaluación + tema3: variables, imagen, descriptores'},
  {y:2026,m:7,d:29, phase:'as', range:[60,99],  label:'Cap3/Cap4: regresión lineal/polinómica, KNN, logística, árboles, SVM, Series Temporales, Ensemble Learning (Random Forests/Boosting) + repaso SOLO-AS'},
  {y:2026,m:7,d:30, phase:'rp', range:null,     label:'Repaso mezclado FINAL — las 404 preguntas juntas'},

  // Pilotos nuevos (2026-08-18): 3 conceptos x 4 preguntas cada uno,
  // construidos leyendo Geron Cap.8-11 y Kelleher Cap.11 -- ver memoria
  // project-new-master-modes-pilot. Ampliables en tandas futuras.
  {y:2026,m:7,d:31, phase:'ns', range:[0,19],   label:'Piloto: sin etiquetas, K-Means, PCA, DBSCAN, Mezclas Gaussianas (Géron Cap.8-9)'},
  {y:2026,m:8,d:1,  phase:'rn', range:[0,19],   label:'Piloto: neurona artificial, capas no lineales, backpropagation, CNN, Dropout (Géron Cap.10-11,14)'},
  {y:2026,m:8,d:2,  phase:'rf', range:[0,19],   label:'Piloto: bandido multi-brazo, procesos de Markov, función de valor, Q-learning real, tabla vs. función (Kelleher Cap.11-12)'},
];
const CAL_PHASE_KEY = {ao:'pyvizMasterAoProgressV2', ra:'pyvizMasterRaProgressV2', as:'pyvizMasterAsProgressV2',
  ns:'pyvizMasterNsProgressV1', rn:'pyvizMasterRnProgressV1', rf:'pyvizMasterRfProgressV1'};
const CAL_PHASE_NAME = {ao:'AO', ra:'RA', as:'AS', rp:'Repaso', ns:'NS', rn:'RN', rf:'RF'};
const CAL_PHASE_MODE = {ao:'toggleMasterAo', ra:'toggleMasterRa', as:'toggleMasterAs', rp:'toggleReviewMode',
  ns:'toggleMasterNs', rn:'toggleMasterRn', rf:'toggleMasterRf'};
const CAL_REPASO_KEY = 'pyvizCalRepasoDoneV1';
const CAL_DISMISS_KEY = 'pyvizCalBannerDismissedV1';

let _calOn=false, _calSelected=null;

function _calDateKey(e){ return e.y+'-'+String(e.m+1).padStart(2,'0')+'-'+String(e.d).padStart(2,'0'); }
function _calTodayEntry(){
  const now=new Date();
  return CAL_PLAN.find(e=>e.y===now.getFullYear() && e.m===now.getMonth() && e.d===now.getDate());
}
function _calRangeDone(e){
  if(!e.range) return null;
  let doneArr=[];
  try{
    const raw=localStorage.getItem(CAL_PHASE_KEY[e.phase]);
    if(raw) doneArr=(JSON.parse(raw).done||[]);
  }catch(err){}
  const doneSet=new Set(doneArr);
  const [a,b]=e.range;
  let n=0; for(let i=a;i<=b;i++) if(doneSet.has(i)) n++;
  return {done:n, total:b-a+1};
}
function _calRepasoStore(){
  try{ return JSON.parse(localStorage.getItem(CAL_REPASO_KEY)||'{}'); }catch(e){ return {}; }
}
function _calRepasoDone(dateKey){ return !!_calRepasoStore()[dateKey]; }
function _calToggleRepaso(dateKey){
  const store=_calRepasoStore();
  store[dateKey]=!store[dateKey];
  try{ localStorage.setItem(CAL_REPASO_KEY, JSON.stringify(store)); }catch(e){}
}
function _calIsEntryDone(e){
  if(e.range){ const d=_calRangeDone(e); return d.done>=d.total; }
  return _calRepasoDone(_calDateKey(e));
}
function _calDismissedStore(){
  try{ return JSON.parse(localStorage.getItem(CAL_DISMISS_KEY)||'{}'); }catch(e){ return {}; }
}
function _calDismissToday(){
  const e=_calTodayEntry(); if(!e) return;
  const store=_calDismissedStore();
  store[_calDateKey(e)]=true;
  try{ localStorage.setItem(CAL_DISMISS_KEY, JSON.stringify(store)); }catch(err){}
  _calRenderBanner();
}

/* ── Banner "hoy toca" — siempre visible, no requiere abrir el panel ──
   Muestra DOS cosas independientes, cada una puede aparecer sola:
   (1) el contenido nuevo que toca hoy según CAL_PLAN (dismissible por hoy)
   (2) la "deuda de repaso" — temas ya completados que Leitner marca como
   vencidos (ver _reviewDueCount() en review.js). Esto NO se puede
   descartar con la (✕): con un plan tan ajustado hasta el 30 de agosto,
   terminar el contenido nuevo a tiempo pero dejar de repasar lo viejo es
   el riesgo real de llegar al examen habiendo "olvidado" temas ya vistos
   — por eso la deuda queda visible aunque el contenido de hoy esté hecho,
   descartado, o incluso fuera del rango 10-30 agosto. */
function _calRenderBanner(){
  const el=document.getElementById('planTodayBanner');
  if(!el) return;
  const reviewDue=typeof _reviewDueCount==='function' ? _reviewDueCount() : 0;

  const e=_calTodayEntry();
  let showPlan=false, progressTxt='';
  if(e){
    const dismissed=_calDismissedStore()[_calDateKey(e)];
    const done=_calIsEntryDone(e);
    showPlan = !dismissed && !done;
    if(e.range){ const d=_calRangeDone(e); progressTxt=d.done+'/'+d.total+' temas'; }
    else progressTxt='repaso pendiente';
  }

  if(!showPlan && reviewDue===0){ el.style.display='none'; return; }

  el.style.display='flex';
  el.className='plan-banner'+(showPlan ? ' plan-banner-'+e.phase : ' plan-banner-rp');
  let html='';
  if(showPlan){
    html+='<span class="plan-banner-txt">📌 Hoy toca ('+CAL_PHASE_NAME[e.phase]+'): '+e.label+
      ' <span class="plan-banner-pct">— '+progressTxt+'</span></span>'+
      '<button class="plan-banner-btn" onclick="_calGoToToday()">Ir a los temas de hoy →</button>';
  }
  if(reviewDue>0){
    html+='<span class="plan-banner-txt plan-banner-debt">🕐 '+reviewDue+' repaso'+(reviewDue===1?'':'s')+
      ' vencido'+(reviewDue===1?'':'s')+'</span>'+
      '<button class="plan-banner-btn plan-banner-debt-btn" onclick="toggleReviewMode()">Repasar ahora →</button>';
  }
  html+='<button class="plan-banner-btn plan-banner-cal" onclick="toggleCalendar()">📅 Ver plan</button>';
  if(showPlan) html+='<button class="plan-banner-x" onclick="_calDismissToday()" title="Ocultar el contenido de hoy (los repasos vencidos no se ocultan)">✕</button>';
  el.innerHTML=html;
}
function _calGoToToday(){
  const e=_calTodayEntry(); if(!e) return;
  const fn=window[CAL_PHASE_MODE[e.phase]];
  if(typeof fn==='function') fn();
}

/* ── Panel completo del calendario ── */
function toggleCalendar(){
  if(_calOn){ _calClose(); return; }
  if(typeof _masterOn!=='undefined' && _masterOn) exitMasterMode();
  if(typeof _aoOn!=='undefined' && _aoOn) exitMasterAo();
  if(typeof _mathOn!=='undefined' && _mathOn) exitMasterMath();
  if(typeof _raOn!=='undefined' && _raOn) exitMasterRa();
  if(typeof _asOn!=='undefined' && _asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn) exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn) exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn) exitMasterRf();
  if(typeof _reviewOn!=='undefined' && _reviewOn) exitReviewMode();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _marathonOn!=='undefined' && _marathonOn) _marathonClosePanel();
  _calOn=true;
  document.getElementById('calendarBar').style.display='flex';
  const b=document.getElementById('bCalendar');
  if(b){ b.textContent='📅 Plan de estudio (activo)'; b.classList.add('btn-looping'); }
  _calRenderPanel();
  if(typeof autoLayout==='function') autoLayout();
}
function _calClose(){
  _calOn=false;
  document.getElementById('calendarBar').style.display='none';
  const b=document.getElementById('bCalendar');
  if(b){ b.textContent='📅 Plan de estudio'; b.classList.remove('btn-looping'); }
  if(typeof autoLayout==='function') autoLayout();
}

function _calRenderPanel(){
  _calRenderStatus();
  _calRenderPhaseBars();
  _calRenderGrid();
  _calRenderDetail();
}
function _calRenderStatus(){
  const el=document.getElementById('calStatus');
  if(!el) return;
  const now=new Date();
  const start=new Date(2026,7,10), end=new Date(2026,7,30);
  const doneDays=CAL_PLAN.filter(_calIsEntryDone).length;
  let dayIdx, chipClass, chipTxt;
  if(now<start){ dayIdx='—'; chipClass='cal-chip-outside'; chipTxt='El plan empieza el 10 de agosto'; }
  else if(now>end){ dayIdx=21; chipClass=doneDays>=21?'cal-chip-ok':'cal-chip-behind';
    chipTxt=doneDays>=21?'Plan completado':'Plan cerrado — faltaron '+(21-doneDays)+' días'; }
  else{
    dayIdx=Math.floor((now-start)/86400000)+1;
    const expected=dayIdx;
    if(doneDays>=expected){ chipClass='cal-chip-ok'; chipTxt=doneDays>expected?'Adelantado':'Al día'; }
    else{ chipClass='cal-chip-behind'; chipTxt='Atrasado por '+(expected-doneDays)+' día'+((expected-doneDays)===1?'':'s'); }
  }
  const reviewDue=typeof _reviewDueCount==='function' ? _reviewDueCount() : 0;
  el.innerHTML=
    '<span class="cal-chip '+chipClass+'">'+chipTxt+'</span>'+
    '<span class="cal-chip '+(reviewDue>0?'cal-chip-behind':'cal-chip-ok')+'">'+
    (reviewDue>0 ? '🕐 '+reviewDue+' repaso'+(reviewDue===1?'':'s')+' vencido'+(reviewDue===1?'':'s') : '🕐 repasos al día')+
    '</span>'+
    '<span class="cal-stat">Día <b>'+dayIdx+'</b> de 21</span>'+
    '<span class="cal-stat"><b>'+doneDays+'</b>/21 días completados</span>';
}
function _calRenderPhaseBars(){
  const el=document.getElementById('calPhaseBars');
  if(!el) return;
  const order=[['ao','AO · 9 días'],['ra','RA · 8 días'],['as','AS · 4 días']];
  el.innerHTML=order.map(([ph,name])=>{
    const days=CAL_PLAN.filter(e=>e.phase===ph);
    const doneN=days.filter(_calIsEntryDone).length;
    const pct=Math.round((doneN/days.length)*100);
    return '<div class="cal-phase-row">'+
      '<span class="cal-phase-name cal-phase-'+ph+'">'+name+'</span>'+
      '<span class="cal-phase-track"><span class="cal-phase-seg cal-phase-seg-'+ph+'" style="width:'+pct+'%"></span></span>'+
      '<span class="cal-phase-count">'+doneN+'/'+days.length+'</span></div>';
  }).join('');
}
function _calRenderGrid(){
  const grid=document.getElementById('calGrid');
  if(!grid) return;
  const Y=2026, M=7; // agosto 2026
  const firstWeekday=new Date(Y,M,1).getDay();
  const daysInMonth=new Date(Y,M+1,0).getDate();
  const now=new Date();
  const byDay={}; CAL_PLAN.forEach(e=>{ byDay[e.d]=e; });

  let html='';
  for(let i=0;i<firstWeekday;i++) html+='<div class="cal-day cal-day-empty"></div>';
  for(let d=1; d<=daysInMonth; d++){
    const e=byDay[d];
    const isToday = now.getFullYear()===Y && now.getMonth()===M && now.getDate()===d;
    const isPast = new Date(Y,M,d) < new Date(now.getFullYear(),now.getMonth(),now.getDate());
    let cls='cal-day';
    if(e) cls+=' cal-day-phase-'+e.phase;
    if(isToday) cls+=' cal-day-today';
    if(_calSelected===d) cls+=' cal-day-selected';
    if(e && isPast && !_calIsEntryDone(e)) cls+=' cal-day-overdue';
    let inner='<div class="cal-day-num">'+d+'</div>';
    if(e){
      inner+='<div class="cal-day-tag">'+CAL_PHASE_NAME[e.phase]+'</div>';
      if(e.range){ const dn=_calRangeDone(e); inner+='<div class="cal-day-count">'+dn.done+'/'+dn.total+'</div>'; }
      else inner+='<div class="cal-day-count">'+(_calRepasoDone(_calDateKey(e))?'✓ hecho':'repaso')+'</div>';
    }
    html+='<button type="button" class="'+cls+'" onclick="_calSelectDay('+d+')">'+inner+'</button>';
  }
  grid.innerHTML=html;
}
function _calSelectDay(d){ _calSelected=d; _calRenderGrid(); _calRenderDetail(); }
function _calRenderDetail(){
  const el=document.getElementById('calDetail');
  if(!el) return;
  const e=_calSelected!=null ? CAL_PLAN.find(x=>x.d===_calSelected) : null;
  if(!e){ el.innerHTML='<p class="cal-detail-empty">Toca un día del calendario para ver el detalle.</p>'; return; }
  const dateKey=_calDateKey(e);
  let progress, actionBtn='';
  if(e.range){
    const dn=_calRangeDone(e);
    progress=dn.done+'/'+dn.total+' temas completados';
    const fn=CAL_PHASE_MODE[e.phase];
    actionBtn='<button class="master-btn" onclick="'+fn+'()">Ir a estos temas →</button>';
  }else{
    const done=_calRepasoDone(dateKey);
    progress=done?'Marcado como hecho':'Repaso mezclado, sin temario propio';
    actionBtn='<button class="master-btn" onclick="_calToggleRepaso(\''+dateKey+'\');_calRenderPanel();">'+
      (done?'✓ Desmarcar':'Marcar como hecho')+'</button>'+
      ' <button class="master-btn" onclick="toggleReviewMode()">Abrir Repaso mezclado →</button>';
  }
  el.innerHTML=
    '<div class="cal-detail-eyebrow cal-phase-'+e.phase+'">'+CAL_PHASE_NAME[e.phase]+' · '+e.d+' de agosto</div>'+
    '<p class="cal-detail-title">'+e.label+'</p>'+
    '<div class="cal-detail-meta">'+progress+'</div>'+
    '<div class="cal-detail-actions">'+actionBtn+'</div>';
}
