/* ──────────── Cuaderno de errores personal ──────────────
   Implementa la sección 8 de tu plan de aprendizaje acelerado (test de
   estilos: Reflexivo+Teórico+Pragmático): cada fallo real en una pregunta
   mc con `whyNot` (AO/RA/AS/Repaso mezclado) se guarda solo, sin fricción
   (ver core.js, _logErrorJournal). Aquí, con calma, revisas cada entrada y
   escribes tu REGLA PERSONAL — el paso de reflexión activa que el registro
   automático no puede hacer por ti. Consulta /list_errors (SQLite real,
   ver error_journal_store.py) — mismo patrón que report.js. */
let _errorsOn=false, _errorsData=[], _errorsFilterMode='';

function toggleErrorJournal(){
  if(_errorsOn){ _errorsClose(); return; }
  if(typeof _masterOn!=='undefined' && _masterOn) exitMasterMode();
  if(typeof _aoOn!=='undefined' && _aoOn) exitMasterAo();
  if(typeof _mathOn!=='undefined' && _mathOn) exitMasterMath();
  if(typeof _raOn!=='undefined' && _raOn) exitMasterRa();
  if(typeof _asOn!=='undefined' && _asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn) exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn) exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn) exitMasterRf();
  if(typeof _reviewOn!=='undefined' && _reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _marathonOn!=='undefined' && _marathonOn) _marathonClosePanel();
  _errorsOn=true;
  document.getElementById('errorJournalBar').style.display='flex';
  const b=document.getElementById('bErrors');
  if(b){ b.textContent='📓 Cuaderno de errores (activo)'; b.classList.add('btn-looping'); }
  _errorsLoad();
  if(typeof autoLayout==='function') autoLayout();
}
function _errorsClose(){
  _errorsOn=false;
  document.getElementById('errorJournalBar').style.display='none';
  const b=document.getElementById('bErrors');
  if(b){ b.textContent='📓 Cuaderno de errores'; b.classList.remove('btn-looping'); }
  if(typeof autoLayout==='function') autoLayout();
}
function _errorsSetFilter(mode){
  _errorsFilterMode=mode;
  _errorsLoad();
}
const ERRORS_MODE_NAME={ao:'🧬 AO', ra:'🎲 RA', as:'🤖 AS', aoclassify:'🧭 AO·Clasif', aocompare:'⚖️ AO·Comp',
  racompare:'⚖️ RA·Comp', ascompare:'⚖️ AS·Comp',
  aolimits:'🚧 AO·Lim', ralimits:'🚧 RA·Lim', aslimits:'🚧 AS·Lim', math:'📐 Matemáticas',
  nslimits:'🚧 NS·Lim', rnlimits:'🚧 RN·Lim', rflimits:'🚧 RF·Lim',
  ns:'🧩 NS', rn:'🕸️ RN', rf:'🕹️ RF',
  nscompare:'⚖️ NS·Comp', rncompare:'⚖️ RN·Comp', rfcompare:'⚖️ RF·Comp'};
function _errorsLoad(){
  const body=document.getElementById('errorJournalBody');
  body.innerHTML='<p class="report-loading">⏳ Cargando tu cuaderno de errores desde la base de datos…</p>';
  const url = _errorsFilterMode ? ('/list_errors?mode='+encodeURIComponent(_errorsFilterMode)) : '/list_errors';
  fetch(url).then(r=>r.json()).then(rows=>{
    _errorsData=Array.isArray(rows)?rows:[];
    _errorsRender();
  }).catch(e=>{
    body.innerHTML='<p class="report-loading">❌ No se pudo cargar el cuaderno: '+e.message+'</p>';
  });
}
function _errorsRenderFilters(){
  const modes=[['','Todos'],['ao','🧬 AO'],['ra','🎲 RA'],['as','🤖 AS'],['ns','🧩 NS'],['rn','🕸️ RN'],['rf','🕹️ RF']];
  return '<div class="errors-filters">'+modes.map(([m,label])=>
    '<button class="master-btn errors-filter-btn'+(m===_errorsFilterMode?' errors-filter-active':'')+'" onclick="_errorsSetFilter(\''+m+'\')">'+label+'</button>'
  ).join('')+'</div>';
}
function _errorsRender(){
  const body=document.getElementById('errorJournalBody');
  let html=_errorsRenderFilters();
  if(!_errorsData.length){
    html+='<p class="report-loading">🎉 Todavía no hay errores registrados aquí — cuando falles una pregunta con explicación, aparecerá sola.</p>';
    body.innerHTML=html;
    return;
  }
  html+='<div class="errors-list">'+_errorsData.map(_errorsCard).join('')+'</div>';
  body.innerHTML=html;
}
/* Plantilla de "Cuaderno de errores" de tu plan (sección 8/27): PROBLEMA,
   MI RESPUESTA, CONCEPTO CORRECTO y CAUSA llegan ya redactados (whyNot);
   REGLA PERSONAL es el único campo que escribes tú, con calma, después. */
function _errorsCard(e){
  const modeLabel=ERRORS_MODE_NAME[e.mode]||e.mode;
  const date=(e.created_at||'').replace('T',' ').slice(0,16);
  const rule=e.personal_rule||'';
  return '<div class="errors-card" data-error-id="'+e.id+'">'+
    '<div class="errors-card-hdr"><span class="errors-card-mode">'+modeLabel+'</span>'+
    '<span class="errors-card-topic">'+esc(e.topic_name||'')+'</span>'+
    '<span class="errors-card-date">'+date+'</span></div>'+
    '<div class="errors-field"><b>PROBLEMA</b><div>'+e.question+'</div></div>'+
    '<div class="errors-field"><b>MI RESPUESTA</b><div class="errors-wrong">'+esc(e.chosen_text||'')+'</div></div>'+
    '<div class="errors-field"><b>CONCEPTO CORRECTO</b><div class="errors-correct">'+esc(e.correct_text||'')+'</div></div>'+
    '<div class="errors-field"><b>CAUSA</b><div>'+esc(e.why_wrong||'')+'</div></div>'+
    '<div class="errors-field errors-rule-field"><b>REGLA PERSONAL</b>'+
    '<textarea class="errors-rule-input" id="errorsRule'+e.id+'" placeholder="¿Qué debo recordar para no repetir este error?">'+esc(rule)+'</textarea>'+
    '<button class="master-btn" onclick="_errorsSaveRule('+e.id+')">💾 Guardar regla</button>'+
    '<span class="errors-rule-saved" id="errorsRuleSaved'+e.id+'" style="display:none">✓ Guardada</span>'+
    '</div></div>';
}
function _errorsSaveRule(id){
  const ta=document.getElementById('errorsRule'+id);
  if(!ta) return;
  const personal_rule=ta.value;
  fetch('/update_error_rule',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id, personal_rule})})
    .then(r=>r.json()).then(res=>{
      const saved=document.getElementById('errorsRuleSaved'+id);
      if(saved && res.ok){ saved.style.display='inline'; setTimeout(()=>{ saved.style.display='none'; }, 2000); }
    }).catch(()=>{});
}
