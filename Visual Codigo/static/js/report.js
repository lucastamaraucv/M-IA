/* ──────────── Reporte visual de puntos fuertes/débiles ──────────────
   Consulta /stats_report (SQLite, ver stats_store.py) — NO localStorage:
   así el reporte refleja el historial real guardado en el servidor, no
   solo lo que hay en este navegador. Solo AO/RA/AS (mismo alcance que
   confianza/"No sé"/notas). Gráficos con CSS puro (conic-gradient para
   los donuts, barras segmentadas para el detalle), sin librería externa. */
let _reportOn=false, _reportData=null, _reportStreak=0, _reportTrend={ao:[],ra:[],as:[],ns:[],rn:[],rf:[]};

function toggleReport(){
  if(_reportOn){ _reportClose(); return; }
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
  if(typeof _marathonOn!=='undefined' && _marathonOn) _marathonClosePanel();
  _reportOn=true;
  document.getElementById('reportBar').style.display='flex';
  const b=document.getElementById('bReport');
  if(b){ b.textContent='📊 Reporte (activo)'; b.classList.add('btn-looping'); }
  _reportLoad();
  if(typeof autoLayout==='function') autoLayout();
}
function _reportClose(){
  _reportOn=false;
  document.getElementById('reportBar').style.display='none';
  const b=document.getElementById('bReport');
  if(b){ b.textContent='📊 Reporte'; b.classList.remove('btn-looping'); }
  if(typeof autoLayout==='function') autoLayout();
}
function _reportLoad(){
  const body=document.getElementById('reportBody');
  body.innerHTML='<p class="report-loading">⏳ Cargando tu historial real desde la base de datos…</p>';
  Promise.all([
    fetch('/stats_report').then(r=>r.json()),
    fetch('/stats_streak').then(r=>r.json()).catch(()=>({streak:0})),
    fetch('/stats_trend?mode=ao&days=14').then(r=>r.json()).catch(()=>[]),
    fetch('/stats_trend?mode=ra&days=14').then(r=>r.json()).catch(()=>[]),
    fetch('/stats_trend?mode=as&days=14').then(r=>r.json()).catch(()=>[]),
    fetch('/stats_trend?mode=ns&days=14').then(r=>r.json()).catch(()=>[]),
    fetch('/stats_trend?mode=rn&days=14').then(r=>r.json()).catch(()=>[]),
    fetch('/stats_trend?mode=rf&days=14').then(r=>r.json()).catch(()=>[]),
  ]).then(([report, streak, trendAo, trendRa, trendAs, trendNs, trendRn, trendRf])=>{
    _reportData=Array.isArray(report)?report:[];
    _reportStreak=(streak && streak.streak) || 0;
    _reportTrend={ao:Array.isArray(trendAo)?trendAo:[], ra:Array.isArray(trendRa)?trendRa:[], as:Array.isArray(trendAs)?trendAs:[],
      ns:Array.isArray(trendNs)?trendNs:[], rn:Array.isArray(trendRn)?trendRn:[], rf:Array.isArray(trendRf)?trendRf:[]};
    _reportRender();
  }).catch(e=>{
    body.innerHTML='<p class="report-loading">❌ No se pudo cargar el reporte: '+e.message+'</p>';
  });
}
const REPORT_MODE_NAME={ao:'🧬 Algoritmos de Optimización', ra:'🎲 Razonamiento Aproximado', as:'🤖 Aprendizaje Supervisado',
  ns:'🧩 No Supervisado', rn:'🕸️ Redes Neuronales', rf:'🕹️ Aprendizaje por Refuerzo'};
const REPORT_MODE_SHORT={ao:'AO', ra:'RA', as:'AS', ns:'NS', rn:'RN', rf:'RF'};
/* Total real de temas por curso (para poder mostrar tambien "sin intentar
   todavia", no solo lo que ya tiene intentos guardados) — se lee de los
   propios arrays EX_AO/EX_RA/EX_AS ya cargados, con fallback si por lo que
   sea todavia no existen. */
function _reportTotalTopics(mode){
  if(mode==='ao') return (typeof EX_AO!=='undefined') ? EX_AO.length : 41;
  if(mode==='ra') return (typeof EX_RA!=='undefined') ? EX_RA.length : 35;
  if(mode==='as') return (typeof EX_AS!=='undefined') ? EX_AS.length : 21;
  if(mode==='ns') return (typeof EX_NS!=='undefined') ? EX_NS.length : 0;
  if(mode==='rn') return (typeof EX_RN!=='undefined') ? EX_RN.length : 0;
  if(mode==='rf') return (typeof EX_RF!=='undefined') ? EX_RF.length : 0;
  return 0;
}
function _reportWeaknessBucket(r){
  if(r.weakness>=5) return 'weak';
  if(r.weakness>0) return 'mid';
  return 'ok';
}

/* Detecta bloques temáticos CONCENTRADOS de debilidad -- 2+ temas de la
   misma familia (convención "Familia · Tema", ya usada en los 3 cursos)
   con al menos 1 en weak/mid -- en vez de solo listar temas sueltos como
   ya hace _reportPriorityList. Evita falsos positivos: temas débiles
   repartidos en familias DISTINTAS no cuentan como cluster (ver umbral
   `topics.length<2` y `weakCount<1`). Alimenta el botón "Reforzar este
   bloque (guiado)" -> _focusStart() en core.js, que aplica el protocolo
   de aprendizaje del usuario (recordar->comprender->aplicar->explicar->
   reflexionar) sobre esos temas concretos, no solo redirige el quiz. */
function _reportWeaknessClusters(byMode){
  const clusters={};
  ['ao','ra','as','ns','rn','rf'].forEach(mode=>{
    const rows=byMode[mode]||[];
    const families={};
    rows.forEach(r=>{
      const familia=(r.name.split(' · ')[0]) || r.name;
      (families[familia]=families[familia]||[]).push(r);
    });
    let best=null;
    Object.keys(families).forEach(familia=>{
      const topics=families[familia];
      if(topics.length<2) return;
      const weakCount=topics.filter(r=>_reportWeaknessBucket(r)!=='ok').length;
      if(weakCount<1) return;
      const score=topics.reduce((s,r)=>s+r.weakness,0);
      if(!best || score>best.score) best={familia, topics, weakCount, score};
    });
    if(best) clusters[mode]=best;
  });
  return clusters;
}

/* Diagnóstico de IA sobre el patrón de razonamiento (reason_tag/opción
   dudada, ver core.js _quizRenderReasonPrompt) acumulado en un bloque
   débil -- se dispara solo (automático) cuando el propio Reporte ya
   detectó el cluster, no por cada pregunta. Cacheado por bloque para no
   repetir la llamada a Claude en cada re-render del Reporte. */
const _clusterDiagCache=new Map();
function _reportFetchDiagnosis(mode, familia, idxs){
  const key=mode+'|'+familia+'|'+idxs.join(',');
  const elId='clusterDiag_'+mode;
  const apply=diag=>{
    const el=document.getElementById(elId);
    if(!el) return;
    if(diag){ el.style.display='block'; el.innerHTML='🔎 <b>Claude detectó:</b> '+esc(diag); }
    else el.style.display='none';
  };
  if(_clusterDiagCache.has(key)){ apply(_clusterDiagCache.get(key)); return; }
  fetch('/analyze_patterns',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({mode, topic_idxs:idxs, familia})})
    .then(r=>r.json()).then(d=>{
      const diag=(d && d.ok && d.diagnosis) ? d.diagnosis : null;
      _clusterDiagCache.set(key, diag);
      apply(diag);
    }).catch(()=>{ apply(null); });
}
function _reportClusterCards(byMode){
  const clusters=_reportWeaknessClusters(byMode);
  const modes=Object.keys(clusters);
  if(!modes.length) return '';
  let html='<div class="cluster-wrap"><div class="cluster-hdr">🎯 Refuerza tus puntos débiles (guiado)</div>';
  modes.forEach(mode=>{
    const c=clusters[mode];
    const idxs=c.topics.map(r=>r.topic_idx).sort((a,b)=>a-b);
    html+='<div class="cluster-card">'+
      '<div class="cluster-card-title">🔴 '+esc(c.familia)+' en '+REPORT_MODE_NAME[mode]+'</div>'+
      '<div class="cluster-card-sub">'+c.weakCount+' de '+c.topics.length+' temas de este bloque están flojos</div>'+
      '<div class="cluster-diagnosis" id="clusterDiag_'+mode+'">🔎 Analizando patrón…</div>'+
      '<button class="master-btn cluster-card-btn" onclick="_focusStart(\''+mode+'\', ['+idxs.join(',')+'], \''+c.familia.replace(/'/g,"\\'")+'\')">Reforzar este bloque (guiado) →</button>'+
      '</div>';
    _reportFetchDiagnosis(mode, c.familia, idxs);
  });
  html+='</div>';
  return html;
}

function _reportRender(){
  const body=document.getElementById('reportBody');
  if(!_reportData || !_reportData.length){
    body.innerHTML='<p class="report-loading">Todavía no hay intentos guardados — responde algunas preguntas en AO, RA o AS y vuelve aquí.</p>';
    return;
  }
  const byMode={ao:[], ra:[], as:[], ns:[], rn:[], rf:[]};
  _reportData.forEach(row=>{ if(byMode[row.mode]) byMode[row.mode].push(row); });

  let html = _reportStreakBadge() + _reportCompareBars(byMode) + _reportPriorityList(_reportData) + _reportClusterCards(byMode);

  ['ao','ra','as','ns','rn','rf'].forEach(mode=>{
    const rows=byMode[mode];
    if(!rows.length) return;
    rows.sort((a,b)=> b.weakness - a.weakness);
    html += _reportCourseCard(mode, rows);
  });
  body.innerHTML = html || '<p class="report-loading">Todavía no hay intentos guardados en AO, RA o AS.</p>';
}

/* Comparativa entre cursos: barras horizontales agrupadas (reemplaza al
   radar de 3 ejes anterior -- con exactamente 3 categorías, un radar SIEMPRE
   dibuja un triángulo sea cual sea el dato, así que la forma no comunica
   nada; una barra sí deja leer el número exacto de un vistazo). Dos barras
   por curso: "% dominado" (conocimiento real, sólida) y "% intentado"
   (cobertura, más clara) -- mismo par de métricas que antes, para seguir
   distinguiendo "débil porque casi no lo intenté" de "débil aunque ya lo
   intenté mucho". Reutiliza el acento de color ya asignado a cada curso. */
function _reportCompareBars(byMode){
  const modes=['ao','ra','as','ns','rn','rf'];
  const stats=modes.map(mode=>{
    const rows=byMode[mode]||[];
    const total=_reportTotalTopics(mode);
    const dominado=rows.filter(r=>_reportWeaknessBucket(r)==='ok').length;
    const attempted=rows.length;
    return {
      mode,
      dominadoPct: total>0 ? dominado/total*100 : 0,
      attemptedPct: total>0 ? attempted/total*100 : 0,
    };
  });
  if(stats.every(s=>s.attemptedPct===0)) return '';

  const rowsHtml=stats.map(s=>{
    const dom=Math.round(s.dominadoPct), att=Math.round(s.attemptedPct);
    return '<div class="report-compare-row">'+
      '<div class="report-compare-name">'+REPORT_MODE_NAME[s.mode]+'</div>'+
      '<div class="report-compare-track">'+
        '<div class="report-compare-fill report-compare-fill-dominado report-compare-fill-'+s.mode+'" style="width:'+dom+'%"></div>'+
        '<span class="report-compare-val">'+dom+'% dominado</span>'+
      '</div>'+
      '<div class="report-compare-track">'+
        '<div class="report-compare-fill report-compare-fill-attempted report-compare-fill-'+s.mode+'" style="width:'+att+'%"></div>'+
        '<span class="report-compare-val">'+att+'% intentado</span>'+
      '</div>'+
    '</div>';
  }).join('');

  return '<div class="report-compare-wrap">'+
    '<div class="report-compare-hdr">📊 Comparativa entre cursos</div>'+
    '<div class="report-compare-rows">'+rowsHtml+'</div>'+
    '<div class="report-radar-legend">'+
      '<span class="report-radar-legend-item"><span class="report-radar-swatch report-radar-swatch-dominado"></span>% dominado (lo que de verdad sabes)</span>'+
      '<span class="report-radar-legend-item"><span class="report-radar-swatch report-radar-swatch-attempted"></span>% intentado (cuánto del curso ya probaste)</span>'+
    '</div></div>';
}

/* Los 8 temas MÁS débiles de los 3 cursos juntos, arriba de todo — para
   responder directo "¿qué reviso hoy?" sin tener que bajar curso por
   curso comparando barras a ojo. */
function _reportPriorityList(allRows){
  const prioritarios=allRows.filter(r=>r.weakness>0).slice().sort((a,b)=>b.weakness-a.weakness).slice(0,8);
  if(!prioritarios.length){
    return '<div class="report-priority report-priority-empty">🎉 Ningún tema con fallos ni "No sé" pendiente ahora mismo — lo que respondiste, lo respondiste bien.</div>';
  }
  const items=prioritarios.map(r=>{
    const bucket=_reportWeaknessBucket(r);
    const motivo=[];
    if(r.incorrect>0) motivo.push(r.incorrect+' fallo'+(r.incorrect===1?'':'s'));
    if(r.dont_know>0) motivo.push(r.dont_know+' "no sé"');
    if(r.guess>0) motivo.push(r.guess+' adivinado'+(r.guess===1?'':'s'));
    return '<div class="report-priority-item report-priority-'+bucket+'" onclick="_reportGoToTopic(\''+r.mode+'\','+r.topic_idx+')">'+
      '<span class="report-priority-course">'+REPORT_MODE_SHORT[r.mode]+'</span>'+
      '<span class="report-priority-name">'+esc(r.name)+'</span>'+
      '<span class="report-priority-why">'+motivo.join(' · ')+'</span>'+
      '</div>';
  }).join('');
  return '<div class="report-priority"><div class="report-priority-hdr">🎯 Prioridad de repaso (los más débiles de los 3 cursos)</div>'+items+'</div>';
}
/* Racha de días consecutivos estudiando (cualquier curso) — deriva de
   fechas distintas en `attempts` (ver get_streak() en stats_store.py), no
   es un contador aparte. Ligada al mismo riesgo que la deuda de repaso del
   calendario: con un plazo ajustado, la constancia importa más que la
   técnica. */
function _reportStreakBadge(){
  if(_reportStreak<=0) return '<div class="report-streak report-streak-zero">📅 Sin racha activa — respondiendo algo hoy la empiezas.</div>';
  return '<div class="report-streak">🔥 <b>'+_reportStreak+'</b> día'+(_reportStreak===1?'':'s')+' seguido'+(_reportStreak===1?'':'s')+' estudiando</div>';
}
/* Mini-gráfico de tendencia (barras CSS, sin librería) — % de acierto por
   día de los últimos 14 días CON datos (get_trend() en stats_store.py).
   Compara la primera mitad del rango contra la segunda para dar una
   flecha de dirección: no basta con ver el nivel actual, importa si vas
   mejorando o empeorando. */
function _reportSparkline(mode){
  const trend=_reportTrend[mode]||[];
  if(!trend.length) return '<div class="report-spark-empty">Sin historial reciente para graficar tendencia.</div>';
  const bars=trend.map(d=>{
    const h=Math.max(6, d.pct);
    const cls = d.pct>=70?'report-spark-good':d.pct>=40?'report-spark-mid':'report-spark-bad';
    return '<span class="report-spark-bar '+cls+'" style="height:'+h+'%" title="'+d.day+': '+d.pct+'% ('+d.correct+'/'+d.total+')"></span>';
  }).join('');
  return '<div class="report-spark-wrap"><div class="report-spark-label">Tendencia (últimos '+trend.length+' días con actividad) '+_reportTrendDirection(trend)+'</div>'+
    '<div class="report-spark">'+bars+'</div></div>';
}
function _reportTrendDirection(trend){
  if(trend.length<2) return '';
  const mid=Math.floor(trend.length/2);
  const firstHalf=trend.slice(0,mid), secondHalf=trend.slice(mid);
  const avg=arr=>arr.reduce((a,d)=>a+d.pct,0)/arr.length;
  const diff=avg(secondHalf)-avg(firstHalf);
  if(diff>=8) return '<span class="report-trend-up">↑ mejorando</span>';
  if(diff<=-8) return '<span class="report-trend-down">↓ bajando</span>';
  return '<span class="report-trend-flat">→ estable</span>';
}
/* Clic en un item de prioridad: te lleva directo a ese tema en su Modo
   Maestro, igual que hace el calendario con "Ir a estos temas". */
function _reportGoToTopic(mode, idx){
  _reportClose();
  const fn={ao:'toggleMasterAo', ra:'toggleMasterRa', as:'toggleMasterAs',
    ns:'toggleMasterNs', rn:'toggleMasterRn', rf:'toggleMasterRf'}[mode];
  if(fn && typeof window[fn]==='function'){
    window[fn]();
    const goFn={ao:'_aoGoTo', ra:'_raGoTo', as:'_asGoTo', ns:'_nsGoTo', rn:'_rnGoTo', rf:'_rfGoTo'}[mode];
    if(goFn && typeof window[goFn]==='function') window[goFn](idx);
  }
}

function _reportCourseCard(mode, rows){
  const total=_reportTotalTopics(mode);
  const attempted=rows.length;
  const dominado=rows.filter(r=>_reportWeaknessBucket(r)==='ok').length;
  const enProgreso=rows.filter(r=>_reportWeaknessBucket(r)==='mid').length;
  const debil=rows.filter(r=>_reportWeaknessBucket(r)==='weak').length;
  const sinIntentar=Math.max(0, total-attempted);

  const pctOf=n=> total>0 ? (n/total*100) : 0;
  const p1=pctOf(dominado), p2=p1+pctOf(enProgreso), p3=p2+pctOf(debil); // acumulado, resto = sin intentar
  const donutStyle='background:conic-gradient(#2f9e5c 0% '+p1.toFixed(2)+'%, #c9a13a '+p1.toFixed(2)+'% '+p2.toFixed(2)+'%, '+
    '#b3492b '+p2.toFixed(2)+'% '+p3.toFixed(2)+'%, #3a3a3a '+p3.toFixed(2)+'% 100%)';
  const pctDominado=total>0 ? Math.round(dominado/total*100) : 0;

  let html='<div class="report-course">';
  html+='<div class="report-course-hdr">'+REPORT_MODE_NAME[mode]+'</div>';
  html+='<div class="report-course-summary">';
  html+='<div class="report-donut" style="'+donutStyle+'"><div class="report-donut-hole"><span>'+pctDominado+'%</span><small>dominado</small></div></div>';
  html+='<div class="report-legend">'+
    '<div class="report-legend-item"><span class="report-dot" style="background:#2f9e5c"></span>Dominado <b>'+dominado+'</b></div>'+
    '<div class="report-legend-item"><span class="report-dot" style="background:#c9a13a"></span>En progreso <b>'+enProgreso+'</b></div>'+
    '<div class="report-legend-item"><span class="report-dot" style="background:#b3492b"></span>Débil <b>'+debil+'</b></div>'+
    '<div class="report-legend-item"><span class="report-dot" style="background:#3a3a3a"></span>Sin intentar <b>'+sinIntentar+'</b></div>'+
    '<div class="report-legend-total">'+total+' temas en total</div>'+
    '</div></div>';
  html+=_reportTopicRadar(mode, rows);
  html+=_reportSparkline(mode);
  html+='<div class="report-rows">';
  rows.forEach(r=>{ html+=_reportRow(r); });
  html+='</div></div>';
  return html;
}

/* Radar por curso, un eje por TEMA (no por curso) -- aquí sí tiene sentido
   la forma de radar, porque con 20-40+ ejes la silueta irregular SÍ
   comunica algo real ("estos temas seguidos están flojos") que con 3 ejes
   (ver _reportCompareBars) no se podía ver. El radio de cada eje es el %
   de acierto real de ESE tema (r.correct/r.total), no un bucket — el color
   del punto sigue las mismas 4 categorías que ya usa el donut. Cada eje
   sin datos (tema nunca intentado) queda en el centro, en gris. Los temas
   no traen nombre corto, así que las etiquetas de texto se omiten (habría
   40 textos superpuestos) y en su lugar cada punto es clicable + trae un
   <title> nativo del navegador con el nombre completo al pasar el mouse. */
function _reportTopicRadar(mode, rows){
  const total=_reportTotalTopics(mode);
  if(total<2) return '';
  const byIdx={};
  rows.forEach(r=>{ byIdx[r.topic_idx]=r; });

  const cx=100, cy=100, R=82;
  const angleFor=i=> (Math.PI*2*i/total) - Math.PI/2;
  const pointFor=(pct,i)=>{
    const ang=angleFor(i);
    const r=R*(Math.max(0,Math.min(100,pct))/100);
    return {x: cx+r*Math.cos(ang), y: cy+r*Math.sin(ang)};
  };

  let gridSvg='';
  [25,50,75,100].forEach(ringPct=>{
    const pts=[];
    for(let i=0;i<total;i++){ const p=pointFor(ringPct,i); pts.push(p.x.toFixed(1)+','+p.y.toFixed(1)); }
    gridSvg+='<polygon points="'+pts.join(' ')+'" class="report-radar-grid" />';
  });

  let axesSvg='', dotsSvg='';
  const polyPts=[];
  for(let i=0;i<total;i++){
    const edge=pointFor(100,i);
    axesSvg+='<line x1="'+cx+'" y1="'+cy+'" x2="'+edge.x.toFixed(1)+'" y2="'+edge.y.toFixed(1)+'" class="report-radar-axis" />';
    const r=byIdx[i];
    const pct = r ? Math.round((r.correct/(r.total||1))*100) : 0;
    const p=pointFor(pct,i);
    polyPts.push(p.x.toFixed(1)+','+p.y.toFixed(1));
    const bucket = r ? _reportWeaknessBucket(r) : 'none';
    const name = (typeof _reportTopicName==='function' && _reportTopicName(mode,i)) || ('Tema '+(i+1));
    dotsSvg+='<circle cx="'+p.x.toFixed(1)+'" cy="'+p.y.toFixed(1)+'" r="2.6" '+
      'class="report-topic-dot report-topic-dot-'+bucket+'" '+
      'onclick="_reportGoToTopic(\''+mode+'\','+i+')">'+
      '<title>'+esc(name)+(r?' — '+pct+'% acierto':' — sin intentar')+'</title></circle>';
  }
  const polyClosed=polyPts.join(' ');

  return '<div class="report-topic-radar-wrap">'+
    '<div class="report-topic-radar-hdr">🕸️ Detalle por tema ('+total+' temas — pasa el cursor o toca un punto)</div>'+
    '<svg viewBox="0 0 200 200" class="report-radar-svg report-topic-radar-svg">'+
      gridSvg+axesSvg+
      '<polygon points="'+polyClosed+'" class="report-topic-radar-poly report-topic-radar-poly-'+mode+'" />'+
      dotsSvg+
    '</svg></div>';
}

function _reportRow(r){
  const total=r.total || 1;
  const seg=(n, cls)=> n>0 ? `<span class="report-seg ${cls}" style="width:${(n/total*100).toFixed(1)}%" title="${n}"></span>` : '';
  // Los aciertos se reparten segun confianza (sure/unsure/guess); lo que
  // acertaste sin haber elegido confianza todavia (o antes de este cambio)
  // se pinta como "correct-plain".
  const correctoConNivel=r.sure + r.unsure + r.guess;
  const correctoSinNivel=Math.max(0, r.correct - correctoConNivel);
  const bar=
    seg(r.sure,'report-seg-sure') + seg(r.unsure,'report-seg-unsure') + seg(r.guess,'report-seg-guess') +
    seg(correctoSinNivel,'report-seg-plain') + seg(r.incorrect,'report-seg-fail') + seg(r.dont_know,'report-seg-dontknow');
  const bucket=_reportWeaknessBucket(r);
  const weaknessTag = bucket==='weak' ? '<span class="report-tag report-tag-weak">🔴 reforzar</span>'
    : bucket==='mid' ? '<span class="report-tag report-tag-mid">🟡 casi</span>'
    : '<span class="report-tag report-tag-ok">🟢 dominado</span>';
  const pctAcierto=total>0 ? Math.round(r.correct/total*100) : 0;
  return '<div class="report-row" onclick="_reportGoToTopic(\''+r.mode+'\','+r.topic_idx+')">'+
    '<div class="report-row-name">'+esc(r.name)+' '+weaknessTag+'</div>'+
    '<div class="report-bar">'+bar+'</div>'+
    '<div class="report-row-meta">'+pctAcierto+'% acierto · ✅'+r.correct+' ❌'+r.incorrect+' 🤷'+r.dont_know+
    (r.due_at ? ' · caja '+(r.box||1) : '')+'</div>'+
    '</div>';
}
