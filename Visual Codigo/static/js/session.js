/* ──────────── Sesión guiada de 60 minutos ────────────
   Implementa el §10 del plan de aprendizaje personal del usuario tal cual
   está escrito, con SU reparto exacto (no un Pomodoro genérico de 25/5):
   0-10' Recuperación, 10-25' Teoría, 25-45' Práctica, 45-52' Explicación,
   52-60' Reflexión. No reemplaza los paneles existentes (Modo Maestro AO/RA/
   AS, Repaso mezclado) — es una capa de RITMO por encima: guía la fase
   actual con un cronómetro y, para Teoría/Práctica/Explicación, un botón que
   abre el panel real correspondiente. El cronómetro (`_sessionActive`) es
   independiente de que el panel de la sesión esté visible (`_sessionOn`):
   una insignia flotante (#sessionFloatBadge) sigue mostrando la fase y el
   tiempo restante aunque el alumno esté dentro de Modo Maestro AO — así no
   se "pierde" el ritmo de la sesión al navegar a estudiar de verdad. */

const SESSION_PHASES=[
  {key:'recall',   name:'Recuperación', mins:10, icon:'🧠'},
  {key:'theory',   name:'Teoría',       mins:15, icon:'📖'},
  {key:'practice', name:'Práctica',     mins:20, icon:'✍️'},
  {key:'explain',  name:'Explicación',  mins:7,  icon:'🗣️'},
  {key:'reflect',  name:'Reflexión',    mins:8,  icon:'🪞'},
];
const SESSION_COURSE_NAME={ao:'🧬 AO', ra:'🎲 RA', as:'🤖 AS'};

let _sessionOn=false, _sessionActive=false, _sessionCourse=null, _sessionPhaseIdx=0,
  _sessionPhaseEndAt=0, _sessionTimerHandle=null, _sessionJustFinished=false;

function toggleSessionMode(){
  if(_sessionOn){ _sessionClosePanel(); return; }
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
  if(typeof _errorsOn!=='undefined' && _errorsOn) _errorsClose();
  if(typeof _marathonOn!=='undefined' && _marathonOn) _marathonClosePanel();
  _sessionOn=true;
  document.getElementById('sessionBar').style.display='flex';
  if(typeof autoLayout==='function') autoLayout();
  _sessionRender();
}
/* Cierra solo el PANEL (usada también desde toggleMasterAo/Ra/As y
   toggleReviewMode, para que no queden dos paneles superpuestos al navegar
   desde dentro de la sesión) — nunca detiene el cronómetro. */
function _sessionClosePanel(){
  _sessionOn=false;
  const bar=document.getElementById('sessionBar');
  if(bar) bar.style.display='none';
  if(typeof autoLayout==='function') autoLayout();
}

function _sessionStart(course){
  _sessionCourse=course;
  _sessionActive=true;
  _sessionJustFinished=false;
  _sessionStartPhase(0);
}
function _sessionStartPhase(idx){
  _sessionPhaseIdx=idx;
  _sessionPhaseEndAt=Date.now()+SESSION_PHASES[idx].mins*60000;
  if(_sessionTimerHandle) clearInterval(_sessionTimerHandle);
  _sessionTimerHandle=setInterval(_sessionTick, 1000);
  _sessionRender();
  _sessionRenderBadge();
}
function _sessionTick(){
  const remaining=_sessionPhaseEndAt-Date.now();
  if(remaining<=0){ _sessionAdvancePhase(); return; }
  _sessionRenderBadge();
  const t=document.getElementById('sessionTimerBig');
  if(t) t.textContent=_sessionFmt(remaining);
}
function _sessionAdvancePhase(){
  if(_sessionPhaseIdx>=SESSION_PHASES.length-1){ _sessionFinish(); return; }
  _sessionStartPhase(_sessionPhaseIdx+1);
}
function _sessionSkipPhase(){ _sessionAdvancePhase(); }
function _sessionFinish(){
  _sessionActive=false;
  _sessionJustFinished=true;
  if(_sessionTimerHandle){ clearInterval(_sessionTimerHandle); _sessionTimerHandle=null; }
  _sessionRenderBadge();
  _sessionRender();
}
function _sessionStop(){
  _sessionActive=false;
  _sessionJustFinished=false;
  _sessionCourse=null;
  _sessionPhaseIdx=0;
  if(_sessionTimerHandle){ clearInterval(_sessionTimerHandle); _sessionTimerHandle=null; }
  _sessionRenderBadge();
  _sessionRender();
}
function _sessionFmt(ms){
  const s=Math.max(0, Math.ceil(ms/1000));
  const m=Math.floor(s/60), r=s%60;
  return String(m).padStart(2,'0')+':'+String(r).padStart(2,'0');
}
function _sessionRenderBadge(){
  const b=document.getElementById('sessionFloatBadge');
  if(!b) return;
  if(!_sessionActive){ b.style.display='none'; return; }
  const phase=SESSION_PHASES[_sessionPhaseIdx];
  const remaining=_sessionPhaseEndAt-Date.now();
  b.style.display='block';
  b.textContent=phase.icon+' '+phase.name+' · '+_sessionFmt(remaining);
}
/* Abre el Modo Maestro real del curso elegido, y cierra el panel de la
   sesión (el cronómetro sigue vivo vía la insignia flotante). */
function _sessionOpenCourse(){
  _sessionClosePanel();
  const fn={ao:'toggleMasterAo', ra:'toggleMasterRa', as:'toggleMasterAs'}[_sessionCourse];
  if(fn && typeof window[fn]==='function') window[fn]();
}
function _sessionOpenReview(){
  _sessionClosePanel();
  if(typeof toggleReviewMode==='function') toggleReviewMode();
}
function _sessionSaveReflection(){
  const ta=document.getElementById('sessionReflectText');
  const savedMsg=document.getElementById('sessionReflectSaved');
  const text=(ta&&ta.value||'').trim();
  if(!text){ if(savedMsg){ savedMsg.style.display='inline'; savedMsg.textContent='Escribe algo antes de guardar.'; } return; }
  const topicName='Reflexión de sesión · '+SESSION_COURSE_NAME[_sessionCourse]+' · '+new Date().toLocaleDateString();
  fetch('/save_note',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({mode:'session', topic_idx:null, topic_name:topicName, text, feedback:null, kind:'reflection'})})
    .then(r=>r.json()).then(d=>{
      if(savedMsg){
        savedMsg.style.display='inline';
        savedMsg.textContent=(d && d.ok) ? '💾 Guardado' : '❌ No se pudo guardar';
        setTimeout(()=>{ if(savedMsg) savedMsg.style.display='none'; }, 2500);
      }
    }).catch(()=>{ if(savedMsg){ savedMsg.style.display='inline'; savedMsg.textContent='❌ No se pudo guardar'; } });
}

function _sessionPhaseContent(phase){
  if(phase.key==='recall'){
    return '<div class="session-phase-desc"><b>Sin mirar apuntes ni la app, respondé mentalmente (o en voz alta):</b>'+
      '<ul><li>¿Qué aprendí ayer?</li><li>¿Qué recuerdo de memoria, sin ayuda?</li>'+
      '<li>¿Qué errores cometí la última vez?</li></ul>'+
      'Recién después de intentar recordar de verdad, seguí a la fase de Teoría.</div>';
  }
  if(phase.key==='theory'){
    return '<div class="session-phase-desc">Estudiá SOLO un concepto concreto — no avances varios temas de una vez. '+
      'Cuando termines de leer, volvé acá o pasá directo a Práctica.</div>'+
      '<div class="session-course-buttons"><button class="master-btn" onclick="_sessionOpenCourse()">'+
      'Abrir Modo Maestro '+(SESSION_COURSE_NAME[_sessionCourse]||'')+'</button></div>';
  }
  if(phase.key==='practice'){
    return '<div class="session-phase-desc">Resolvé ejercicios SIN mirar la solución primero — intentalo, y solo si '+
      'te trabás, revisá la pista o la solución. El Repaso mezclado prioriza automáticamente lo que tenés vencido hoy.</div>'+
      '<div class="session-course-buttons"><button class="master-btn" onclick="_sessionOpenCourse()">'+
      'Seguir con Modo Maestro '+(SESSION_COURSE_NAME[_sessionCourse]||'')+'</button>'+
      '<button class="master-btn" onclick="_sessionOpenReview()">Abrir Repaso mezclado</button></div>';
  }
  if(phase.key==='explain'){
    return '<div class="session-phase-desc"><b>Método Feynman:</b> explicá el concepto de hoy con TUS propias '+
      'palabras, como si se lo enseñaras a alguien que no sabe nada del tema. En el tema donde estabas, usá el '+
      'bloque "🧠 Autoexplícate" para escribirlo.</div>'+
      '<div class="session-course-buttons"><button class="master-btn" onclick="_sessionOpenCourse()">'+
      'Volver a Modo Maestro '+(SESSION_COURSE_NAME[_sessionCourse]||'')+'</button></div>';
  }
  // reflect
  return '<div class="session-phase-desc">Cerrá la sesión respondiendo:'+
    '<ul><li>¿Qué entendí?</li><li>¿Qué no entendí?</li><li>¿Dónde me equivoqué?</li>'+
    '<li>¿Qué regla aprendí?</li><li>¿Qué debo practicar después?</li></ul></div>'+
    '<textarea id="sessionReflectText" placeholder="Escribe tu reflexión aquí..." style="width:100%;min-height:80px;'+
    'background:#1a1a24;border:1px solid #3d3d55;border-radius:4px;color:#e0e0e0;font-size:12px;padding:8px;font-family:inherit;resize:vertical;"></textarea>'+
    '<div style="margin-top:6px"><button class="self-explain-ai-btn" onclick="_sessionSaveReflection()">💾 Guardar reflexión</button>'+
    '<span class="self-explain-saved" id="sessionReflectSaved" style="display:none"></span></div>';
}

function _sessionRender(){
  const body=document.getElementById('sessionBody');
  if(!body) return;
  if(_sessionJustFinished){
    body.innerHTML='<div class="session-phase-desc">🎉 <b>¡Sesión completa!</b> Recuperación → Teoría → Práctica → '+
      'Explicación → Reflexión — los 60 minutos completos de '+(SESSION_COURSE_NAME[_sessionCourse]||'')+'. '+
      'Repetilo mañana con recuperación espaciada (Repaso mezclado ya prioriza lo vencido).</div>'+
      '<div class="session-select-buttons">'+
      '<button class="master-btn session-select-btn" onclick="_sessionStart(\'ao\')">🧬 AO</button>'+
      '<button class="master-btn session-select-btn" onclick="_sessionStart(\'ra\')">🎲 RA</button>'+
      '<button class="master-btn session-select-btn" onclick="_sessionStart(\'as\')">🤖 AS</button>'+
      '</div>';
    return;
  }
  if(!_sessionActive){
    body.innerHTML='<div class="session-phase-desc">Elegí el curso de hoy — la sesión sigue tu reparto exacto: '+
      '10\' Recuperación → 15\' Teoría → 20\' Práctica → 7\' Explicación → 8\' Reflexión (60\' en total).</div>'+
      '<div class="session-select-buttons">'+
      '<button class="master-btn session-select-btn" onclick="_sessionStart(\'ao\')">🧬 AO</button>'+
      '<button class="master-btn session-select-btn" onclick="_sessionStart(\'ra\')">🎲 RA</button>'+
      '<button class="master-btn session-select-btn" onclick="_sessionStart(\'as\')">🤖 AS</button>'+
      '</div>';
    return;
  }
  const phase=SESSION_PHASES[_sessionPhaseIdx];
  const isLast=_sessionPhaseIdx>=SESSION_PHASES.length-1;
  const chips=SESSION_PHASES.map((p,i)=>{
    const cls=i<_sessionPhaseIdx?'session-phase-chip session-phase-chip-done':
      (i===_sessionPhaseIdx?'session-phase-chip session-phase-chip-current':'session-phase-chip');
    return `<span class="${cls}">${p.icon} ${p.name} (${p.mins}')</span>`;
  }).join('');
  body.innerHTML=
    '<div class="session-phases">'+chips+'</div>'+
    '<div class="session-timer-big" id="sessionTimerBig">'+_sessionFmt(_sessionPhaseEndAt-Date.now())+'</div>'+
    _sessionPhaseContent(phase)+
    '<div class="session-course-buttons" style="margin-top:14px">'+
      (isLast?'':'<button class="master-btn" onclick="_sessionSkipPhase()">⏭️ Saltar a la siguiente fase</button>')+
      '<button class="master-btn master-btn-exit" onclick="_sessionStop()">⏹️ Terminar sesión</button>'+
    '</div>';
}
