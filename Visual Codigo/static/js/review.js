/* ──────────── Repaso mezclado: 4º modo, ponderado por fallos ────────────
   No es un temario secuencial — cada vez que se pide "otro repaso" se sortea
   un tema entre TODOS los ya completados de los 3 modos, con más probabilidad
   para los que más se fallaron (Karpicke & Roediger 2008 + Dunlosky 2013).
   Los temas de origen 'ao'/'math'/'ra'/'as' muestran una tarjeta de pregunta
   igual que sus modos de origen; los de origen 'py' no tienen pregunta tipo
   quiz, así que abren directo el Reto de código ya existente. Un origen
   extra, 'aoclassify' (ver AO_CLASSIFY en master-ao.js), mezcla preguntas de
   CLASIFICACIÓN de técnica entre varios temas de AO ya vistos —
   interleaving para entrenar el reconocimiento rápido de patrón (Chi,
   Feltovich y Glaser 1981), no solo el recuerdo de un tema aislado. Se
   desbloquea solo, mediante _aoClassifyUnlocked(), cuando ya se completó
   al menos un tema de cada familia de técnica. Otro origen extra,
   'aocompare' (ver AO_COMPARE en master-ao.js), es más fino: compara UN PAR
   concreto de técnicas confundibles ("¿en qué se diferencian Dijkstra y
   A*?"), peldaño "Comparación" de la Escalera de Dominio — cada par se
   desbloquea por separado, con _aoCompareUnlocked(i), en cuanto AMBOS
   conceptos del par ya se completaron. */
let _reviewOn=false, _reviewItem=null, _reviewAnswered=false, _reviewQuizShuffledCorrect=null, _reviewCurrentSrc=null, _reviewQuizOrder=null;
function toggleReviewMode(){
  if(_reviewOn){ exitReviewMode(); return; }
  if(_masterOn) exitMasterMode();
  if(_aoOn) exitMasterAo();
  if(_mathOn) exitMasterMath();
  if(_raOn) exitMasterRa();
  if(_asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn) exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn) exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn) exitMasterRf();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _sessionOn!=='undefined' && _sessionOn) _sessionClosePanel();
  if(typeof _marathonOn!=='undefined' && _marathonOn) _marathonClosePanel();
  _reviewOn=true;
  _loadMasterProgress(); _loadAoProgress(); _loadMathProgress(); _loadRaProgress(); _loadAsProgress();
  if(typeof _loadNsProgress==='function') _loadNsProgress();
  if(typeof _loadRnProgress==='function') _loadRnProgress();
  if(typeof _loadRfProgress==='function') _loadRfProgress();
  // .main (código+ejecución) se muestra/oculta POR PREGUNTA en _reviewNext,
  // no aquí -- Repaso mezclado alterna orígenes con y sin código real.
  document.getElementById('reviewPanel').style.display='flex';
  document.getElementById('reviewBar').style.display='flex';
  const b=document.getElementById('bReview');
  if(b){ b.textContent='🔀 Repaso mezclado (activo)'; b.classList.add('btn-looping'); }
  _reviewNext();
}
function exitReviewMode(){
  _reviewOn=false;
  document.getElementById('reviewBar').style.display='none';
  document.getElementById('reviewPanel').style.display='none';
  document.querySelector('.main').style.display='flex';
  const b=document.getElementById('bReview');
  if(b){ b.textContent='🔀 Repaso mezclado'; b.classList.remove('btn-looping'); }
}
function _reviewBuildPool(){
  const pool=[];
  _masterDone.forEach(i=>pool.push({mode:'py', idx:i}));
  _aoDone.forEach(i=>pool.push({mode:'ao', idx:i}));
  _mathDone.forEach(i=>pool.push({mode:'math', idx:i}));
  if(typeof _raDone!=='undefined') _raDone.forEach(i=>pool.push({mode:'ra', idx:i}));
  if(typeof _asDone!=='undefined') _asDone.forEach(i=>pool.push({mode:'as', idx:i}));
  if(typeof _nsDone!=='undefined') _nsDone.forEach(i=>pool.push({mode:'ns', idx:i}));
  if(typeof _rnDone!=='undefined') _rnDone.forEach(i=>pool.push({mode:'rn', idx:i}));
  if(typeof _rfDone!=='undefined') _rfDone.forEach(i=>pool.push({mode:'rf', idx:i}));
  // No dependen de un progreso "done" propio (no son un tema con su propio
  // recorrido guiado): entran todas de golpe en cuanto se desbloquean.
  if(typeof _aoClassifyUnlocked==='function' && _aoClassifyUnlocked()){
    AO_CLASSIFY.forEach((_,i)=>pool.push({mode:'aoclassify', idx:i}));
  }
  if(typeof AO_COMPARE!=='undefined' && typeof _aoCompareUnlocked==='function'){
    AO_COMPARE.forEach((_,i)=>{ if(_aoCompareUnlocked(i)) pool.push({mode:'aocompare', idx:i}); });
  }
  if(typeof RA_COMPARE!=='undefined' && typeof _raCompareUnlocked==='function'){
    RA_COMPARE.forEach((_,i)=>{ if(_raCompareUnlocked(i)) pool.push({mode:'racompare', idx:i}); });
  }
  if(typeof AS_COMPARE!=='undefined' && typeof _asCompareUnlocked==='function'){
    AS_COMPARE.forEach((_,i)=>{ if(_asCompareUnlocked(i)) pool.push({mode:'ascompare', idx:i}); });
  }
  if(typeof NS_COMPARE!=='undefined' && typeof _nsCompareUnlocked==='function'){
    NS_COMPARE.forEach((_,i)=>{ if(_nsCompareUnlocked(i)) pool.push({mode:'nscompare', idx:i}); });
  }
  if(typeof RN_COMPARE!=='undefined' && typeof _rnCompareUnlocked==='function'){
    RN_COMPARE.forEach((_,i)=>{ if(_rnCompareUnlocked(i)) pool.push({mode:'rncompare', idx:i}); });
  }
  if(typeof RF_COMPARE!=='undefined' && typeof _rfCompareUnlocked==='function'){
    RF_COMPARE.forEach((_,i)=>{ if(_rfCompareUnlocked(i)) pool.push({mode:'rfcompare', idx:i}); });
  }
  if(typeof AO_LIMITS!=='undefined' && typeof _aoLimitsUnlocked==='function'){
    AO_LIMITS.forEach((_,i)=>{ if(_aoLimitsUnlocked(i)) pool.push({mode:'aolimits', idx:i}); });
  }
  if(typeof RA_LIMITS!=='undefined' && typeof _raLimitsUnlocked==='function'){
    RA_LIMITS.forEach((_,i)=>{ if(_raLimitsUnlocked(i)) pool.push({mode:'ralimits', idx:i}); });
  }
  if(typeof AS_LIMITS!=='undefined' && typeof _asLimitsUnlocked==='function'){
    AS_LIMITS.forEach((_,i)=>{ if(_asLimitsUnlocked(i)) pool.push({mode:'aslimits', idx:i}); });
  }
  if(typeof NS_LIMITS!=='undefined' && typeof _nsLimitsUnlocked==='function'){
    NS_LIMITS.forEach((_,i)=>{ if(_nsLimitsUnlocked(i)) pool.push({mode:'nslimits', idx:i}); });
  }
  if(typeof RN_LIMITS!=='undefined' && typeof _rnLimitsUnlocked==='function'){
    RN_LIMITS.forEach((_,i)=>{ if(_rnLimitsUnlocked(i)) pool.push({mode:'rnlimits', idx:i}); });
  }
  if(typeof RF_LIMITS!=='undefined' && typeof _rfLimitsUnlocked==='function'){
    RF_LIMITS.forEach((_,i)=>{ if(_rfLimitsUnlocked(i)) pool.push({mode:'rflimits', idx:i}); });
  }
  return pool;
}
/* Fuente de la pregunta según el origen del ítem sorteado — centralizado
   aquí para no repetir el condicional de varias vías en cada función de
   abajo. AO_QUIZ/RA_QUIZ/AS_QUIZ son ahora un banco de varias preguntas
   por tema (ver _quizPickOne en core.js): esta función elige UNA al azar,
   así que solo debe llamarse una vez por pregunta mostrada — el resultado
   se cachea en _reviewCurrentSrc (ver _reviewNext) y _reviewCheckAnswer/
   _reviewShowSolution deben leer esa variable, no volver a llamar aquí. */
function _reviewSrc(item){
  if(item.mode==='ao') return _quizPickOne(AO_QUIZ, item.idx);
  if(item.mode==='aoclassify') return AO_CLASSIFY[item.idx];
  if(item.mode==='aocompare') return AO_COMPARE[item.idx];
  if(item.mode==='racompare') return RA_COMPARE[item.idx];
  if(item.mode==='ascompare') return AS_COMPARE[item.idx];
  if(item.mode==='nscompare') return NS_COMPARE[item.idx];
  if(item.mode==='rncompare') return RN_COMPARE[item.idx];
  if(item.mode==='rfcompare') return RF_COMPARE[item.idx];
  if(item.mode==='aolimits') return AO_LIMITS[item.idx];
  if(item.mode==='ralimits') return RA_LIMITS[item.idx];
  if(item.mode==='aslimits') return AS_LIMITS[item.idx];
  if(item.mode==='nslimits') return NS_LIMITS[item.idx];
  if(item.mode==='rnlimits') return RN_LIMITS[item.idx];
  if(item.mode==='rflimits') return RF_LIMITS[item.idx];
  if(item.mode==='ra') return _quizPickOne(RA_QUIZ, item.idx);
  if(item.mode==='as') return _quizPickOne(AS_QUIZ, item.idx);
  if(item.mode==='ns') return _quizPickOne(NS_QUIZ, item.idx);
  if(item.mode==='rn') return _quizPickOne(RN_QUIZ, item.idx);
  if(item.mode==='rf') return _quizPickOne(RF_QUIZ, item.idx);
  return EX_MATH[item.idx];
}
/* Código Python real detrás de la pregunta, para poder mostrarlo (y
   ejecutarlo) igual que en su Modo Maestro de origen -- ver _reviewNext.
   Solo ao/ra/as tienen un EX_*[idx].code 1:1 con el índice de la pregunta:
   math no tiene código (temario sin depurador), py ya abre su propio Reto
   completo aparte, y aoclassify no referencia un índice concreto de EX_AO
   (son enunciados libres de "qué técnica es esta"). */
function _reviewCodeSource(item){
  if(item.mode==='ao' && typeof EX_AO!=='undefined' && EX_AO[item.idx]) return EX_AO[item.idx].code;
  if(item.mode==='ra' && typeof EX_RA!=='undefined' && EX_RA[item.idx]) return EX_RA[item.idx].code;
  if(item.mode==='as' && typeof EX_AS!=='undefined' && EX_AS[item.idx]) return EX_AS[item.idx].code;
  if(item.mode==='ns' && typeof EX_NS!=='undefined' && EX_NS[item.idx]) return EX_NS[item.idx].code;
  if(item.mode==='rn' && typeof EX_RN!=='undefined' && EX_RN[item.idx]) return EX_RN[item.idx].code;
  if(item.mode==='rf' && typeof EX_RF!=='undefined' && EX_RF[item.idx]) return EX_RF[item.idx].code;
  return null;
}
/* Muestra/oculta .main (el depurador completo: código+pasos+frames+objetos+
   salida, compartido con AO/RA/AS -- ver _aoGoTo en master-ao.js) según si
   ESTA pregunta concreta tiene código real detrás. Se llama en cada
   pregunta, no solo al entrar a Repaso mezclado, porque mezcla orígenes con
   y sin código en la misma sesión. */
function _reviewSyncCodePanel(item){
  const code = _reviewCodeSource(item);
  const mainEl = document.querySelector('.main');
  if(code){
    document.getElementById('codeInput').value = code;
    if(typeof renderLineNums==='function') renderLineNums();
    document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
    document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
    document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
    mainEl.style.display='flex';
    runCode();
  } else {
    mainEl.style.display='none';
  }
  if(typeof autoLayout==='function') autoLayout();
}
/* Cada fallo triplica el peso base de un tema frente a uno nunca fallado —
   usado para variar ENTRE los temas vencidos (ver _reviewPickNext), no para
   decidir si un tema toca repasar o no (eso ahora lo decide Leitner/`due`,
   ver core.js). */
function _reviewWeight(mode, idx){
  return 1 + 2*_statsFor(mode, idx).fails;
}
/* Repaso espaciado (Leitner, ver core.js `_recordAttempt`/`LEITNER_INTERVALS_DAYS`):
   entre los temas ya completados, prioriza los que están VENCIDOS (due <=
   ahora) — si hay al menos uno, el sorteo ponderado por fallos se hace SOLO
   entre esos. Si nada está vencido todavía (racha reciente, o poco
   historial), se cae al sorteo sobre el pool completo de siempre, para que
   el Repaso mezclado nunca se quede "vacío" esperando fechas. */
function _reviewPickNext(){
  const pool=_reviewBuildPool().filter(it=>!_reviewItem || it.mode!==_reviewItem.mode || it.idx!==_reviewItem.idx);
  let fullPool=pool.length ? pool : _reviewBuildPool();
  if(!fullPool.length) return null;
  const now=Date.now();
  const duePool=fullPool.filter(it=>_statsFor(it.mode, it.idx).due<=now);
  if(duePool.length) fullPool=duePool;
  const weights=fullPool.map(it=>_reviewWeight(it.mode, it.idx));
  const total=weights.reduce((a,b)=>a+b,0);
  let r=Math.random()*total;
  for(let i=0;i<fullPool.length;i++){ r-=weights[i]; if(r<=0) return fullPool[i]; }
  return fullPool[fullPool.length-1];
}
/* Cuántos de los temas completados están vencidos AHORA MISMO — mostrado en
   el contador del Repaso mezclado (ver _reviewNext) para que el sistema de
   fechas sea visible, no una lógica invisible. */
function _reviewDueCount(){
  const now=Date.now();
  return _reviewBuildPool().filter(it=>_statsFor(it.mode, it.idx).due<=now).length;
}
function _reviewNext(){
  _reviewItem=_reviewPickNext();
  _reviewAnswered=false;
  document.getElementById('reviewEmptyCard').style.display='none';
  document.getElementById('reviewQuizCard').style.display='none';
  document.getElementById('reviewPyCard').style.display='none';
  if(!_reviewItem){
    document.getElementById('reviewEmptyCard').style.display='block';
    document.getElementById('reviewCounter').textContent='';
    document.querySelector('.main').style.display='none';
    return;
  }
  const total=_reviewBuildPool().length;
  const due=_reviewDueCount();
  document.getElementById('reviewCounter').textContent=
    due>0 ? `${total} tema(s) completados · 🕐 ${due} vencido(s) para repasar hoy`
          : `${total} tema(s) completados · nada vencido todavía, repasando al azar`;
  if(_reviewItem.mode==='py'){
    document.getElementById('reviewPyCard').style.display='block';
    document.getElementById('reviewPyName').textContent=EX[_reviewItem.idx].name;
    document.querySelector('.main').style.display='none';
    return;
  }
  _reviewSyncCodePanel(_reviewItem);
  const src=_reviewSrc(_reviewItem);
  _reviewCurrentSrc=src; // fijada aquí: _reviewCheckAnswer/_reviewShowSolution deben usar esta MISMA pregunta
  const badge={ao:'🧬 AO', math:'📐 Matemáticas', aoclassify:'🧭 AO · Clasificación', aocompare:'⚖️ AO · Comparación',
    racompare:'⚖️ RA · Comparación', ascompare:'⚖️ AS · Comparación',
    nscompare:'⚖️ NS · Comparación', rncompare:'⚖️ RN · Comparación', rfcompare:'⚖️ RF · Comparación',
    aolimits:'🚧 AO · Limitación', ralimits:'🚧 RA · Limitación', aslimits:'🚧 AS · Limitación',
    nslimits:'🚧 NS · Limitación', rnlimits:'🚧 RN · Limitación', rflimits:'🚧 RF · Limitación',
    ra:'🎲 RA', as:'🤖 AS', ns:'🧩 NS', rn:'🕸️ RN', rf:'🕹️ RF'}[_reviewItem.mode];
  document.getElementById('reviewSourceBadge').textContent=badge;
  const qText=src.question||src.problem;
  const qType=src.type||'mc';
  document.getElementById('reviewQuestionBody').innerHTML=qText.replace(/\n/g,'<br>');
  const optWrap=document.getElementById('reviewOptions');
  const numWrap=document.getElementById('reviewNumericWrap');
  if(qType==='mc'){
    numWrap.style.display='none';
    const res=_quizRenderAnswerArea('review', _reviewItem.mode, _reviewItem.idx, src);
    _reviewQuizShuffledCorrect=res.shuffled?res.shuffled.correct:null;
    _reviewQuizOrder=res.shuffled?res.shuffled.order:null;
  } else {
    optWrap.style.display='none';
    numWrap.style.display='flex';
    const inp=document.getElementById('reviewNumericInput');
    inp.value=''; inp.disabled=false;
    _reviewQuizShuffledCorrect=null;
    _reviewQuizOrder=null;
  }
  document.getElementById('reviewFeedback').style.display='none';
  document.getElementById('reviewSolutionBtn').style.display='none';
  const solBody=document.getElementById('reviewSolutionBody');
  solBody.style.display='none'; solBody.innerHTML='';
  document.getElementById('reviewNextBtn').style.display='none';
  document.getElementById('reviewQuizCard').style.display='block';
  _quizResetExtras('review');
  _mathRenderKatex();
}
/* Reintentar tras fallar: solo se bloquea la pregunta al ACERTAR (mismo
   cambio que en master-ao.js/master-ra.js/master-math.js) — un fallo deja
   el input/los botones habilitados para corregir un error o un typo e
   intentarlo de nuevo. */
function _reviewCheckAnswer(selectedIdx){
  if(_reviewAnswered || !_reviewItem) return;
  const src=_reviewCurrentSrc;
  const qType=src.type||'mc';
  let ok=false;
  if(qType==='mc'){
    ok = selectedIdx===_reviewQuizShuffledCorrect;
    document.querySelectorAll('#reviewOptions .math-option').forEach((btn,i)=>{
      btn.classList.remove('math-option-correct','math-option-wrong');
      if(ok){
        btn.disabled=true;
        if(i===_reviewQuizShuffledCorrect) btn.classList.add('math-option-correct');
      } else if(i===selectedIdx){
        btn.classList.add('math-option-wrong');
      }
    });
  } else {
    const inp=document.getElementById('reviewNumericInput');
    const val=parseFloat(inp.value.trim().replace(',','.'));
    const dec=src.decimals||0;
    const p=Math.pow(10,dec);
    ok = !isNaN(val) && Math.round(val*p)===Math.round(src.correct*p);
    inp.disabled=ok;
  }
  if(ok) _reviewAnswered=true;
  _recordAttempt(_reviewItem.mode, _reviewItem.idx, ok);
  const fb=document.getElementById('reviewFeedback');
  fb.style.display='block';
  fb.className='math-feedback '+(ok?'math-feedback-ok':'math-feedback-bad');
  // whyNot[i] explica esa opcion CONCRETA (indice ORIGINAL, sin barajar) --
  // mismo patron ya usado en master-ao.js/-ra.js/-as.js; aoclassify/math no
  // tienen whyNot, así que aquí simplemente da null y cae al texto generico.
  const whyNot = (!ok && qType==='mc' && src.whyNot && _reviewQuizOrder) ? src.whyNot[_reviewQuizOrder[selectedIdx]] : null;
  if(whyNot) _logErrorJournal(_reviewItem.mode, _reviewItem.idx, _reportTopicName(_reviewItem.mode, _reviewItem.idx), src.question, src.options[_reviewQuizOrder[selectedIdx]], src.options[src.correct], whyNot);
  fb.textContent = ok ? '✅ Correcto.' :
    (whyNot ? '❌ '+whyNot+' Puedes intentarlo de nuevo, o revisar la solución.'
            : '❌ Incorrecto — puedes intentarlo de nuevo, o revisar la solución.');
  document.getElementById('reviewSolutionBtn').style.display='inline-block';
  document.getElementById('reviewNextBtn').style.display='inline-block';
  if(ok) _quizRenderConfidencePrompt('review');
  if(qType==='mc' && _reviewQuizOrder){
    const otherOptionTexts=src.options.filter((_,i)=>i!==_reviewQuizOrder[selectedIdx]);
    _quizRenderReasonPrompt('review', otherOptionTexts);
  }
}
function _reviewShowSolution(){
  if(!_reviewItem) return;
  const src=_reviewCurrentSrc;
  const el=document.getElementById('reviewSolutionBody');
  el.innerHTML=src.solution.replace(/\n/g,'<br>')+_quizStepsHtml(src)+_quizWhyNotHtml(src, _reviewQuizOrder)+_quizStakesHtml(src);
  el.style.display='block';
  _mathRenderKatex();
}
function _reviewOpenPyChallenge(){
  if(!_reviewItem || _reviewItem.mode!=='py') return;
  const idx=_reviewItem.idx;
  exitReviewMode();
  toggleMasterMode();
  _masterGoTo(idx);
  // el Reto de ese tema se pide async (_masterFetchChallenge) — esperar a que
  // llegue antes de "abrirlo", igual que hace _masterCaptureAfterRun con las pistas.
  const tryOpen=()=>{
    if(_masterPos!==idx) return; // el alumno ya navegó a otro lado mientras esperaba
    if(_masterChallenge[idx]) masterNext();
    else setTimeout(tryOpen, 150);
  };
  setTimeout(tryOpen, 150);
}

