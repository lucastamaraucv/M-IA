/* "Anatomía del código": ventana de explicabilidad visual estilo pizarra
   digital (pedida por el usuario) — código con resaltado de sintaxis real
   (tokenizado, no a mano) + anotaciones flotantes conectadas por
   CONECTORES EN CODO (ortogonales, no diagonales) a un token EXACTO, con
   animación de revelado (líneas de código entran primero, después cada
   anotación se dibuja) vía CSS -- ver [[project-code-anatomy-viz]] en
   memoria. Piloto de 5 temas + ronda de ~18 temas adicionales priorizando
   los de mayor abstracción, un tema por vez sigue siendo mano (contenido),
   pero el MOTOR (tokenizador, layout, animación) es genérico y sirve para
   cualquier código nuevo sin tocar este archivo.

   El coloreado de sintaxis SÍ es 100% automático (mecánico, no una
   decisión de contenido): _annotTokenizeLine reconoce keywords/strings/
   números/comentarios/identificadores con una única regex + heurística
   "¿el próximo caracter no-espacio es '('?" para distinguir identificador
   de llamada. Lo que se escribe a mano por tema son las ANOTACIONES (qué
   vale la pena señalar y cómo explicarlo).

   Animación: CSS puro (@keyframes en style.css, clases .ca-code-line/
   .ca-annot-box/.ca-connector/.ca-token-hl), no SMIL -- el SVG se inserta
   inline en el DOM real de la página (innerHTML), así que CSS es la
   opción correcta (SMIL es para SVGs standalone cargados como <img>, ver
   skill svg-animations). Cada `_xxRenderCodeAnatomy()` reemplaza el
   innerHTML entero con un SVG nuevo, así que las animaciones se disparan
   solas cada vez que el alumno entra a ese tema (son nodos DOM nuevos),
   sin lógica de JS adicional para "reiniciar" nada.

   REDISEÑO VISUAL (2026-09-01, pedido explícito del usuario tras el fix
   de superposición de conectores): esquinas de conector redondeadas
   (_annotRoundedD, técnica de "rounded orthogonal routing"), paleta de 6
   colores de acento cíclica por anotación -- el MISMO color se usa para
   el conector, su flecha, la franja superior de la caja Y el resaltado
   del fragmento de código exacto que señala, formando una cadena visual
   clara entre las 3-4 piezas de UNA sola anotación -- y sombra sutil en
   las cajas (feDropShadow) para que se lean como tarjetas con
   profundidad. El sistema de bandas/colisiones (_annotAssignBands,
   _annotConnectorPath) NO se tocó, ya estaba verificado con un detector
   geométrico (0 solapes/cruces en los 9 temas reales de AO+RA). */

const _ANNOT_KEYWORDS = new Set(['for','in','if','elif','else','def','return','import','from','as',
  'while','break','continue','pass','class','try','except','finally','with','lambda',
  'not','and','or','is','None','True','False','global','yield','raise','assert']);

const _ANNOT_TOKEN_RE = /#.*|'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|\d+\.\d+|\d+|[A-Za-z_]\w*|[+\-*/%=<>!&|^~]+|[(),:\[\]{}.]|\s+/g;

function _annotTokenizeLine(line){
  const tokens=[];
  let m;
  _ANNOT_TOKEN_RE.lastIndex=0;
  while((m=_ANNOT_TOKEN_RE.exec(line))){
    const t=m[0];
    const col=m.index;
    if(/^\s+$/.test(t)) continue; // los espacios no generan span (la columna ya los deja en su lugar)
    let type='punct';
    if(t.startsWith('#')) type='comment';
    else if(/^['"]/.test(t)) type='string';
    else if(/^\d/.test(t)) type='number';
    else if(/^[A-Za-z_]/.test(t)){
      if(_ANNOT_KEYWORDS.has(t)) type='keyword';
      else{
        let j=col+t.length;
        while(j<line.length && line[j]===' ') j++;
        type=(line[j]==='(')?'call':'ident';
      }
    }
    tokens.push({text:t, col, type});
  }
  return tokens;
}

const _ANNOT_COLORS={keyword:'#ff2fa0', ident:'#62e0ff', call:'#ffd23f', number:'#7dff8a',
  string:'#ffb86c', comment:'#6b8f6a', punct:'#e4e4ee'};

// Paleta de acento por ANOTACIÓN (no por tipo de token) -- distinta a
// propósito de _ANNOT_COLORS, para que la capa "meta" (anotaciones) nunca
// compita visualmente con la capa "código" (sintaxis). Se cicla por orden
// de aparición en el recorrido de revelado; ningún tema actual pasa de 8
// anotaciones, así que 6 colores repitiéndose sigue siendo legible sin
// volverse un arcoíris.
const _ANNOT_ACCENTS=['#5ec8e0','#b98aef','#f0a868','#6fd9a8','#ef8fae','#d9d16a'];

const _ANNOT_CHAR_W=8.1, _ANNOT_LINE_H=24, _ANNOT_PAD_L=48, _ANNOT_BAND_GAP=14, _ANNOT_STUB=11, _ANNOT_CORNER_R=6;

function _annotEsc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* Busca `text` dentro de line[fromIdx en más], devuelve columna o -1. La
   anotación puede pedir occurrence>0 si el mismo texto aparece más de una
   vez en la línea (ej. dos 'w' distintas). */
function _annotFindCol(line, text, occurrence){
  let idx=-1, from=0;
  for(let k=0;k<=(occurrence||0);k++){
    idx=line.indexOf(text, from);
    if(idx===-1) return -1;
    from=idx+1;
  }
  return idx;
}

function _annotBoxLines(a){
  const l=[a.label]; if(a.desc) l.push(a.desc); if(a.detail) l.push(a.detail);
  return l;
}
function _annotBoxSize(a){
  const l=_annotBoxLines(a);
  const w=Math.max(70, Math.max(...l.map(t=>t.length))*6.6+22);
  const h=l.length*15+14;
  return {w,h};
}

/* Convierte una lista de puntos [x,y] de una ruta estrictamente ortogonal
   (todos los tramos horizontales o verticales, como las que arman
   _annotElbowPath/_annotConnectorPath) en un `d` de SVG con las esquinas
   INTERIORES redondeadas: en cada vértice se recortan `radius` px de cada
   tramo adyacente (acotado a la mitad del tramo más corto -- cubre tramos
   chicos o de largo 0, que ya ocurren hoy cuando bx===tx) y se unen con
   una curva Q usando el vértice original como punto de control -- la
   técnica estándar de "rounded orthogonal routing" (draw.io/AWS). Los
   puntos duplicados consecutivos se descartan primero para no generar
   tramos degenerados. */
function _annotRoundedD(points, radius){
  const pts=points.filter((p,i)=> i===0 || p[0]!==points[i-1][0] || p[1]!==points[i-1][1]);
  if(pts.length<2) return '';
  if(pts.length===2) return `M${pts[0][0]},${pts[0][1]} L${pts[1][0]},${pts[1][1]}`;
  let d=`M${pts[0][0]},${pts[0][1]}`;
  for(let i=1;i<pts.length-1;i++){
    const [x0,y0]=pts[i-1], [x,y]=pts[i], [x2,y2]=pts[i+1];
    const segIn=Math.abs(x-x0)+Math.abs(y-y0), segOut=Math.abs(x2-x)+Math.abs(y2-y);
    const r=Math.max(0, Math.min(radius, segIn/2, segOut/2));
    const inX=x-Math.sign(x-x0)*r, inY=y-Math.sign(y-y0)*r;
    const outX=x+Math.sign(x2-x)*r, outY=y+Math.sign(y2-y)*r;
    d+=` L${inX},${inY} Q${x},${y} ${outX},${outY}`;
  }
  const last=pts[pts.length-1];
  d+=` L${last[0]},${last[1]}`;
  return d;
}

/* Conector en codo (ortogonal): de la caja sale un tramo corto PERPENDICULAR
   al borde del código, después un tramo horizontal hasta alinearse con el
   token, y un último tramo vertical hasta el token -- en vez de una línea
   diagonal directa. Reduce mucho el cruce visual sobre código no
   relacionado en fragmentos de varias líneas. Devuelve los PUNTOS de la
   ruta (no un `d` armado) + el largo Manhattan exacto, para que el
   llamador decida cómo dibujarla (ver _annotRoundedD) y cuánto reservar
   para la animación de dibujado. */
function _annotElbowPath(bx, byEdge, tx, ty, side){
  const shelfY = side==='top' ? byEdge+_ANNOT_STUB : byEdge-_ANNOT_STUB;
  const points=[[bx,byEdge],[bx,shelfY],[tx,shelfY],[tx,ty]];
  const len=Math.abs(shelfY-byEdge) + Math.abs(tx-bx) + Math.abs(ty-shelfY);
  return {points, len};
}

/* Cuando una anotación vive en una banda EXTERIOR (lejos del código), su
   conector tiene que atravesar el espacio de las bandas MÁS CERCANAS al
   código antes de llegar a él -- con el elbow simple de arriba, ese tramo
   vertical va exactamente por bx (el centro de la propia caja), y si una
   caja de una banda interior ocupa esa misma columna x, el conector la
   atraviesa de lleno. Esta versión primero revisa si bx/tx caen libres de
   TODAS las bandas interiores (`blockingSegs`, la unión de sus segmentos
   ocupados); si no, busca el canal x libre más cercano y rodea por ahí con
   un tramo extra, en vez de cruzar en línea recta. Con blockingSegs vacío
   (banda 0, nada por delante) se comporta exactamente igual que
   _annotElbowPath. */
function _annotConnectorPath(bx, byEdge, tx, ty, side, blockingSegs, codeEdgeY){
  const fits = x => !blockingSegs.some(seg => x>seg.left-6 && x<seg.right+6);
  if(!blockingSegs.length || fits(bx)){
    return _annotElbowPath(bx, byEdge, tx, ty, side);
  }
  let channelX=bx, found=fits(tx);
  if(found) channelX=tx;
  for(let d0=4; d0<=400 && !found; d0+=4){
    const preferRight = tx>=bx;
    const cand1=bx+(preferRight?d0:-d0), cand2=bx+(preferRight?-d0:d0);
    if(fits(cand1)){ channelX=cand1; found=true; }
    else if(fits(cand2)){ channelX=cand2; found=true; }
  }
  // el hueco real entre la banda 0 (la más cercana) y el borde del código es
  // SIEMPRE de 6px exactos (la constante "+6" de boxCenterFromCode en
  // renderCodeAnatomy se cancela con la mitad de su propia altura de banda,
  // asi que el borde de la banda 0 queda fijo en codeEdgeY∓6 sin importar
  // el alto de esa banda) -- usar _ANNOT_STUB (11) ahí se metería DENTRO de
  // la banda 0; 3 deja margen de sobra a cada lado de ese hueco de 6px.
  const nearCodeY = side==='top' ? codeEdgeY-3 : codeEdgeY+3;
  const points=[[bx,byEdge],[channelX,byEdge],[channelX,nearCodeY],[tx,nearCodeY],[tx,ty]];
  const len=Math.abs(channelX-bx) + Math.abs(nearCodeY-byEdge) + Math.abs(tx-channelX) + Math.abs(ty-nearCodeY);
  return {points, len};
}

/* Asigna cada anotación a la banda (fila) MÁS CERCANA al código donde su
   caja (ancho real estimado) no choca con ninguna otra ya puesta en esa
   banda -- colisión real por segmentos horizontales, no una heurística de
   paridad par/impar. Prioriza banda cercana según `_edgeDist` (qué tan
   cerca está la línea objetivo del borde del bloque hacia ese lado) para
   que las líneas conectoras no tengan que viajar tan lejos. Devuelve
   además la altura de cada banda (el máximo alto de caja que contiene). */
function _annotAssignBands(list){
  const sorted=list.slice().sort((a,b)=> (a._edgeDist-b._edgeDist) || (a._x-b._x));
  const bandSegs=[]; // bandSegs[i] = [{left,right}, ...]
  const bandH=[];
  sorted.forEach(a=>{
    const sz=_annotBoxSize(a);
    a._boxW=sz.w; a._boxH=sz.h;
    const left=a._x-sz.w/2, right=a._x+sz.w/2;
    let bi=0;
    for(;;bi++){
      if(!bandSegs[bi]) bandSegs[bi]=[];
      const collide=bandSegs[bi].some(seg=>!(right<seg.left-8 || left>seg.right+8));
      if(!collide){ bandSegs[bi].push({left,right}); break; }
    }
    a._band=bi;
    bandH[bi]=Math.max(bandH[bi]||0, sz.h);
  });
  return {items:sorted, bandH, nBands:bandH.length, bandSegs};
}

/* spec = {title, caption, lines:[str...], annotations:[{line,text,occurrence?,label,desc?,detail?,side:'top'|'bottom'}...], blockBracket:{from,to,label}?} */
function renderCodeAnatomy(spec){
  if(!spec || !Array.isArray(spec.lines) || !spec.lines.length) return '';
  const lines=spec.lines;
  const maxLineLen=Math.max(...lines.map(l=>l.length));
  const codeW=_ANNOT_PAD_L + maxLineLen*_ANNOT_CHAR_W + 40;

  const rawTop=(spec.annotations||[]).filter(a=>a.side!=='bottom');
  const rawBottom=(spec.annotations||[]).filter(a=>a.side==='bottom');

  function locate(a){
    const line=lines[a.line]||'';
    const col=_annotFindCol(line, a.text, a.occurrence||0);
    a._col=col;
    a._x=_ANNOT_PAD_L + Math.max(0,col)*_ANNOT_CHAR_W + (a.text.length*_ANNOT_CHAR_W)/2;
    a._edgeDist = a.side==='bottom' ? (lines.length-1-a.line) : a.line;
    a._found=col>=0;
    return a;
  }
  rawTop.forEach(locate); rawBottom.forEach(locate);
  const top=_annotAssignBands(rawTop.filter(a=>a._found));
  const bottom=_annotAssignBands(rawBottom.filter(a=>a._found));

  // offset acumulado (desde el código hacia afuera) de cada banda, sumando
  // la altura real de las bandas más internas + separación
  function bandOffsets(bandH){
    const off=[]; let acc=0;
    for(let i=0;i<bandH.length;i++){ off[i]=acc; acc+=bandH[i]+_ANNOT_BAND_GAP; }
    return {off, total: bandH.length? acc : 0};
  }
  const topLayout=bandOffsets(top.bandH);
  const bottomLayout=bandOffsets(bottom.bandH);
  top.off=topLayout.off; bottom.off=bottomLayout.off;

  const bracket=spec.blockBracket;
  const bracketLabelW=bracket ? (String(bracket.label||'Block of code').length*6.2+40) : 0;

  const titleH=spec.title? 46 : 14;
  const codeTop=titleH+topLayout.total+(top.items.length?10:0);
  const codeH=lines.length*_ANNOT_LINE_H;
  const bottomH=bottomLayout.total+(bottom.items.length?10:0);
  const captionH=spec.caption?32:6;

  const svgW=Math.round(Math.max(codeW+bracketLabelW+24, 360));
  const svgH=Math.round(codeTop+codeH+bottomH+captionH+18);

  // orden de revelado: primero las líneas de código, luego las anotaciones
  // de banda más cercana a más lejana (top y bottom intercaladas por
  // cercanía) -- así el ojo sigue un recorrido lógico, no aleatorio. De
  // paso, ese mismo índice de recorrido asigna el color de acento cíclico
  // (_colorIdx) -- dos anotaciones consecutivas casi nunca comparten color.
  const codeRevealEnd = (lines.length-1)*0.045 + 0.32;
  const allAnnots=top.items.concat(bottom.items).sort((a,b)=>a._band-b._band || a._x-b._x);
  allAnnots.forEach((a,i)=>{ a._delay=(codeRevealEnd + i*0.085).toFixed(3); a._colorIdx=i%_ANNOT_ACCENTS.length; });

  // agrupa anotaciones por línea de código, para resaltar el fragmento
  // exacto detrás del texto de esa línea (ver más abajo)
  const annotsByLine={};
  allAnnots.forEach(a=>{ (annotsByLine[a.line]=annotsByLine[a.line]||[]).push(a); });

  let s='';
  s+=`<svg class="code-anatomy-svg" viewBox="0 0 ${svgW} ${svgH}" xmlns="http://www.w3.org/2000/svg" font-family="Menlo, 'Fira Code', Consolas, monospace">`;
  s+=`<defs>`;
  s+=`<filter id="caBoxShadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="2.5" stdDeviation="2.4" flood-color="#000" flood-opacity="0.45"/></filter>`;
  _ANNOT_ACCENTS.forEach((c,i)=>{
    s+=`<marker id="annotArrow${i}" markerWidth="9" markerHeight="9" refX="4.6" refY="4.5" orient="auto"><path d="M0,0.6 L9,4.5 L0,8.4 L2.4,4.5 Z" fill="${c}"/></marker>`;
  });
  s+=`</defs>`;
  s+=`<rect x="0" y="0" width="${svgW}" height="${svgH}" rx="10" fill="#12121a" stroke="#2c2c3c"/>`;

  if(spec.title) s+=`<text x="${svgW/2}" y="26" text-anchor="middle" font-size="16" font-weight="700" fill="#ff6b5b">${_annotEsc(spec.title)}</text>`;

  // corchete de bloque (opcional), a la derecha del código
  if(bracket){
    const y1=codeTop + bracket.from*_ANNOT_LINE_H - 15;
    const y2=codeTop + bracket.to*_ANNOT_LINE_H + 7;
    const bx=codeW+8;
    s+=`<path class="ca-code-line" style="animation-delay:${codeRevealEnd.toFixed(3)}s" d="M${bx},${y1} h8 v${y2-y1} h-8" fill="none" stroke="#a888e0" stroke-width="2"/>`;
    s+=`<text class="ca-code-line" style="animation-delay:${codeRevealEnd.toFixed(3)}s" x="${bx+14}" y="${(y1+y2)/2+4}" font-size="11" fill="#a888e0" font-family="sans-serif">${_annotEsc(bracket.label||'Block of code')}</text>`;
  }

  // numeros de linea + resaltados de fragmento + tokens coloreados -- cada
  // línea es un <g> propio para poder animarla como unidad (fade + slide
  // sutil hacia abajo). Los resaltados van ANTES que los tokens (quedan
  // detrás del texto) y usan el delay/color de SU anotación, no el de la
  // línea -- aparecen en sincronía con su caja+conector, reforzando la
  // cadena visual "caja color X -> conector color X -> fragmento color X".
  lines.forEach((line,i)=>{
    const y=codeTop + i*_ANNOT_LINE_H + 15;
    const delay=(i*0.045).toFixed(3);
    s+=`<g class="ca-code-line" style="animation-delay:${delay}s">`;
    (annotsByLine[i]||[]).forEach(a=>{
      const hlX=_ANNOT_PAD_L + a._col*_ANNOT_CHAR_W - 3;
      const hlW=a.text.length*_ANNOT_CHAR_W + 6;
      s+=`<rect class="ca-token-hl" style="animation-delay:${a._delay}s" x="${hlX}" y="${y-14}" width="${hlW}" height="18" rx="3" fill="${_ANNOT_ACCENTS[a._colorIdx]}"/>`;
    });
    s+=`<text x="20" y="${y}" font-size="13" fill="#5a5a70" text-anchor="end">${i+1}</text>`;
    const toks=_annotTokenizeLine(line);
    toks.forEach(t=>{
      const x=_ANNOT_PAD_L + t.col*_ANNOT_CHAR_W;
      s+=`<text x="${x}" y="${y}" font-size="13.5" fill="${_ANNOT_COLORS[t.type]}" xml:space="preserve">${_annotEsc(t.text)}</text>`;
    });
    s+=`</g>`;
  });

  function renderSide(layout, side){
    // `layout.bandSegs` (de _annotAssignBands) guarda la posición NATURAL de
    // cada caja, antes del "clamp" que la empuja hacia adentro si se saldría
    // del lienzo -- pero la caja se DIBUJA en la posición ya recortada. Si el
    // clamp movió alguna, esos segmentos quedan desactualizados y un
    // conector puede terminar "esquivando" un hueco que en realidad ya no
    // existe. Por eso primero se recorta la posición real de CADA caja, y
    // recién con esas posiciones finales se arma bandSegsFinal para el
    // chequeo de colisión de los conectores.
    const bandSegsFinal=[];
    layout.items.forEach(a=>{
      let boxX=Math.min(Math.max(a._x-a._boxW/2, _ANNOT_PAD_L-6), svgW-a._boxW-4);
      // El clamp de arriba solo mira los bordes del lienzo, no las cajas
      // YA colocadas en esta misma banda -- dos cajas angostas cerca del
      // borde izquierdo pueden clampear al mismo punto y quedar
      // solapadas (visto en VC3 · Programación lineal: dos arrays que
      // arrancan en columna 0). Si tras el clamp sigue chocando con una
      // caja anterior de la banda, se empuja a la derecha del hueco libre
      // más cercano, y recién ahí se re-clampea al lienzo.
      const bandSegs=bandSegsFinal[a._band]||[];
      let moved=true;
      while(moved){
        moved=false;
        for(const seg of bandSegs){
          if(!(boxX+a._boxW < seg.left-8 || boxX > seg.right+8)){
            boxX=seg.right+8.5;
            moved=true;
          }
        }
      }
      boxX=Math.min(boxX, svgW-a._boxW-4);
      a._finalLeft=boxX; a._finalRight=boxX+a._boxW;
      (bandSegsFinal[a._band]=bandSegsFinal[a._band]||[]).push({left:a._finalLeft, right:a._finalRight});
    });
    layout.items.forEach(a=>{
      const off=layout.off[a._band];
      const tokenY=codeTop + a.line*_ANNOT_LINE_H + (side==='top'? 3 : 20);
      // centro vertical de la caja, medido desde el borde del código hacia afuera
      const boxCenterFromCode=off + layout.bandH[a._band]/2 + 6;
      const boxCY = side==='top' ? (codeTop-boxCenterFromCode) : (codeTop+codeH+boxCenterFromCode);
      const boxX=a._finalLeft;
      const boxY=boxCY-a._boxH/2;
      const edgeY = side==='top' ? boxY+a._boxH : boxY;
      // segmentos ocupados por bandas MÁS CERCANAS al código que la de esta
      // anotación -- el conector tiene que esquivarlos, no atravesarlos
      const blockingSegs=[];
      for(let bi=0; bi<a._band; bi++) (bandSegsFinal[bi]||[]).forEach(seg=>blockingSegs.push(seg));
      const codeEdgeY = side==='top' ? codeTop : codeTop+codeH;
      const conn=_annotConnectorPath(boxX+a._boxW/2, edgeY, a._x, tokenY, side, blockingSegs, codeEdgeY);
      const accent=_ANNOT_ACCENTS[a._colorIdx];
      const pathD=_annotRoundedD(conn.points, _ANNOT_CORNER_R);
      const dashLen=Math.ceil(conn.len)+8;
      s+=`<path class="ca-connector" style="animation-delay:${a._delay}s;stroke-dasharray:${dashLen};stroke-dashoffset:${dashLen}" d="${pathD}" stroke="${accent}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none" marker-end="url(#annotArrow${a._colorIdx})"/>`;
      s+=`<g class="ca-annot-box" style="animation-delay:${a._delay}s">`;
      s+=`<rect x="${boxX}" y="${boxY}" width="${a._boxW}" height="${a._boxH}" rx="7" fill="#1c1c28" stroke="#3a3a52" filter="url(#caBoxShadow)"/>`;
      s+=`<rect x="${boxX+7}" y="${boxY+3}" width="${Math.max(4,a._boxW-14)}" height="3.5" rx="1.75" fill="${accent}"/>`;
      _annotBoxLines(a).forEach((t,li)=>{
        const cls=li===0?'font-size="11" font-weight="700" fill="#e8c8a8"':'font-size="10" fill="#9aa8bb"';
        s+=`<text x="${boxX+a._boxW/2}" y="${boxY+18+li*13}" text-anchor="middle" font-family="sans-serif" ${cls}>${_annotEsc(t)}</text>`;
      });
      s+=`</g>`;
    });
  }
  renderSide(top,'top');
  renderSide(bottom,'bottom');

  if(spec.caption) s+=`<text class="ca-code-line" style="animation-delay:${codeRevealEnd.toFixed(3)}s" x="${svgW/2}" y="${svgH-10}" text-anchor="middle" font-size="11" fill="#8899aa" font-family="sans-serif">${_annotEsc(spec.caption)}</text>`;

  s+='</svg>';
  return s;
}
