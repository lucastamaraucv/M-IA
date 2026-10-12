/* Motor de visualizacion conceptual para los 3 Modos Maestro (AO/RA/AS).
   Cada pregunta puede traer un campo `viz:{type,data}` (ver EX_AO/RA/AS) con
   datos YA verificados por ejecucion real de Python -- este archivo solo los
   dibuja, no inventa ningun numero. Los colores salen de variables CSS
   (--viz-accent/--viz-data1/2/3) definidas por curso en style.css, asi que
   la MISMA funcion de render sirve para AO, RA y AS sin parametro de color. */

function _vizFmtNum(v){
  if(typeof v!=='number' || !isFinite(v)) return String(v);
  if(Number.isInteger(v)) return String(v);
  const r=Math.round(v*100)/100;
  return String(r).replace('.',',');
}

function _vizBar(data){
  const vals=data.values||[];
  const labels=data.labels||[];
  if(!vals.length) return '';
  const max=Math.max(...vals.map(v=>Math.abs(v)), 1e-9);
  // Label y valor van en su propia linea (arriba), la barra ocupa el ancho
  // completo debajo -- evita que las etiquetas largas ("Favorable (casi
  // ordenada)") se corten o se monten sobre la barra, como pasaba con una
  // columna de etiqueta de ancho fijo.
  const rowH=46, padX=10, padY=12, chartW=420;
  const colorClasses=['viz-fill-1','viz-fill-3','viz-fill-2','viz-fill-accent'];
  const h=padY*2+vals.length*rowH;
  const w=padX*2+chartW;
  let rows='';
  vals.forEach((v,i)=>{
    const y=padY+i*rowH;
    const barW=Math.max(3, Math.abs(v)/max*chartW);
    const cls=colorClasses[i%colorClasses.length];
    const vt=_vizFmtNum(v)+(data.unit?(' '+data.unit):'');
    rows+=`<text x="${padX}" y="${(y+11).toFixed(1)}" class="viz-label">${esc(labels[i]||'')}</text>`+
      `<text x="${(padX+chartW).toFixed(1)}" y="${(y+11).toFixed(1)}" class="viz-value" text-anchor="end">${esc(vt)}</text>`+
      `<rect x="${padX}" y="${(y+18).toFixed(1)}" width="${barW.toFixed(1)}" height="16" rx="4" class="viz-bar-rect ${cls}"/>`;
  });
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">${rows}</svg>`;
}

function _vizCurve(data){
  const raw=data.points||[];
  if(!raw.length) return '';
  const pts=raw.map((p,i)=>Array.isArray(p)?p:[i,p]);
  const xs=pts.map(p=>p[0]), ys=pts.map(p=>p[1]);
  const xMin=Math.min(...xs), xMax=Math.max(...xs);
  const yMin=Math.min(...ys,0), yMax=Math.max(...ys);
  const w=440, h=160, padL=40, padB=26, padT=14, padR=14;
  const plotW=w-padL-padR, plotH=h-padT-padB;
  const sx=x=>padL+(xMax>xMin?(x-xMin)/(xMax-xMin):0.5)*plotW;
  const sy=y=>padT+plotH-(yMax>yMin?(y-yMin)/(yMax-yMin):0.5)*plotH;
  const path=pts.map((p,i)=>(i===0?'M':'L')+sx(p[0]).toFixed(1)+' '+sy(p[1]).toFixed(1)).join(' ');
  const dots=pts.map((p,i)=>{
    const isLast=i===pts.length-1;
    return `<circle cx="${sx(p[0]).toFixed(1)}" cy="${sy(p[1]).toFixed(1)}" r="${isLast?4.5:2.5}" class="${isLast?'viz-dot-final':'viz-dot'}"/>`;
  }).join('');
  const lastVal=`<text x="${(padL+plotW).toFixed(1)}" y="${(sy(ys[ys.length-1])-8).toFixed(1)}" class="viz-mark-value" text-anchor="end">${_vizFmtNum(ys[ys.length-1])}</text>`;
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">`+
    `<line x1="${padL}" y1="${padT+plotH}" x2="${padL+plotW}" y2="${padT+plotH}" class="viz-axis"/>`+
    `<line x1="${padL}" y1="${padT}" x2="${padL}" y2="${padT+plotH}" class="viz-axis"/>`+
    `<path d="${path}" class="viz-curve-path"/>${dots}${lastVal}`+
    `<text x="${padL}" y="${h-4}" class="viz-axis-label">${esc(data.xLabel||'')}</text>`+
    `<text x="4" y="${padT+8}" class="viz-axis-label">${esc(data.yLabel||'')}</text>`+
    `</svg>`;
}

function _vizMembership(data){
  const pts=data.points||[];
  if(!pts.length) return '';
  const xs=pts.map(p=>p[0]);
  const xMin=Math.min(...xs), xMax=Math.max(...xs);
  const w=440, h=160, padL=30, padB=26, padT=14, padR=14;
  const plotW=w-padL-padR, plotH=h-padT-padB;
  const sx=x=>padL+(xMax>xMin?(x-xMin)/(xMax-xMin):0.5)*plotW;
  const sy=y=>padT+plotH-Math.max(0,Math.min(1,y))*plotH;
  const path=pts.map((p,i)=>(i===0?'M':'L')+sx(p[0]).toFixed(1)+' '+sy(p[1]).toFixed(1)).join(' ');
  let mark='';
  if(data.markX!=null && data.markY!=null){
    const mx=sx(data.markX), my=sy(data.markY);
    mark=`<line x1="${mx.toFixed(1)}" y1="${(padT+plotH).toFixed(1)}" x2="${mx.toFixed(1)}" y2="${my.toFixed(1)}" class="viz-guide"/>`+
      `<line x1="${padL}" y1="${my.toFixed(1)}" x2="${mx.toFixed(1)}" y2="${my.toFixed(1)}" class="viz-guide"/>`+
      `<circle cx="${mx.toFixed(1)}" cy="${my.toFixed(1)}" r="4.5" class="viz-dot-final"/>`+
      `<text x="${mx.toFixed(1)}" y="${(padT+plotH+16).toFixed(1)}" class="viz-axis-label" text-anchor="middle">${_vizFmtNum(data.markX)}</text>`+
      `<text x="${(mx+7).toFixed(1)}" y="${(my-6).toFixed(1)}" class="viz-mark-value">${_vizFmtNum(data.markY)}</text>`;
  }
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">`+
    `<line x1="${padL}" y1="${padT}" x2="${padL}" y2="${padT+plotH}" class="viz-axis"/>`+
    `<line x1="${padL}" y1="${padT+plotH}" x2="${padL+plotW}" y2="${padT+plotH}" class="viz-axis"/>`+
    `<text x="2" y="${padT+8}" class="viz-axis-label">1</text>`+
    `<text x="2" y="${padT+plotH+4}" class="viz-axis-label">0</text>`+
    `<path d="${path}" class="viz-curve-path"/>${mark}`+
    `<text x="${padL}" y="${h-2}" class="viz-axis-label">${esc(data.xLabel||'')}</text>`+
    `</svg>`;
}

/* Trayectoria de busqueda sobre el paisaje de una funcion convexa
   centrada en el origen (f(x,y)=x^2+y^2, la que usan los temas de
   descenso del gradiente de este curso) -- los anillos son literalmente
   circulos de nivel de esa funcion, no decoracion: cualquier circulo
   centrado en el origen ES un contorno real de x^2+y^2=cte. */
function _vizContour(data){
  const pts=data.points||[];
  if(!pts.length) return '';
  const w=300, h=300, cx=150, cy=150, maxR=128;
  const maxAbs=Math.max(...pts.map(p=>Math.max(Math.abs(p[0]),Math.abs(p[1]))));
  const range=Math.max(2.5, maxAbs*1.15);
  const scale=maxR/range;
  const sx=x=>cx+x*scale, sy=y=>cy-y*scale;
  const rings=[0.25,0.5,0.75,1.0].map(f=>
    `<circle cx="${cx}" cy="${cy}" r="${(maxR*f).toFixed(1)}" class="viz-contour-ring"/>`).join('');
  const path=pts.map((p,i)=>(i===0?'M':'L')+sx(p[0]).toFixed(1)+' '+sy(p[1]).toFixed(1)).join(' ');
  const dots=pts.map((p,i)=>{
    const isFirst=i===0, isLast=i===pts.length-1;
    const cls=isFirst?'viz-dot':(isLast?'viz-dot-final':'viz-dot');
    return `<circle cx="${sx(p[0]).toFixed(1)}" cy="${sy(p[1]).toFixed(1)}" r="${isLast?5:3}" class="${cls}"/>`;
  }).join('');
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">`+
    `${rings}<circle cx="${cx}" cy="${cy}" r="3" class="viz-contour-min"/>`+
    `<path d="${path}" class="viz-curve-path"/>${dots}`+
    `</svg>`;
}

/* Frontera de decision: una cuadricula de fondo con la clase que el modelo
   predice en cada celda (entrenado y evaluado de verdad con sklearn, no
   aproximado a mano) + los puntos reales de entrenamiento encima,
   coloreados por su clase VERDADERA -- se ve de un vistazo donde el
   modelo acierta y donde la frontera deja puntos del lado equivocado. */
function _vizBoundary(data){
  const grid=data.grid; const points=data.points||[];
  if(!grid) return '';
  const w=320, h=240, pad=6;
  const plotW=w-2*pad, plotH=h-2*pad;
  const nx=grid.nx, ny=grid.ny, cells=grid.cells;
  const cellW=plotW/nx, cellH=plotH/ny;
  const classCls=['viz-class-0','viz-class-1','viz-class-2','viz-class-3'];
  let rects='';
  for(let r=0;r<ny;r++){
    for(let c=0;c<nx;c++){
      const cls=cells[r][c];
      const x=pad+c*cellW, y=pad+r*cellH;
      rects+=`<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${(cellW+0.6).toFixed(1)}" height="${(cellH+0.6).toFixed(1)}" class="viz-bg-cell ${classCls[cls%classCls.length]}"/>`;
    }
  }
  const sx=x=>pad+((x-grid.x0)/(grid.x1-grid.x0))*plotW;
  const sy=y=>pad+plotH-((y-grid.y0)/(grid.y1-grid.y0))*plotH;
  const dots=points.map(p=>{
    const [x,y,cls]=p;
    return `<circle cx="${sx(x).toFixed(1)}" cy="${sy(y).toFixed(1)}" r="4" class="viz-point ${classCls[cls%classCls.length]}"/>`;
  }).join('');
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">${rects}${dots}</svg>`;
}

function _vizRoute(data){
  const cities=data.cities||[];
  if(!cities.length) return '';
  const route=(data.route&&data.route.length)?data.route:cities.map((_,i)=>i);
  const xs=cities.map(c=>c[0]), ys=cities.map(c=>c[1]);
  const xMin=Math.min(...xs), xMax=Math.max(...xs), yMin=Math.min(...ys), yMax=Math.max(...ys);
  const w=320, h=200, pad=24;
  const sx=x=>pad+(xMax>xMin?(x-xMin)/(xMax-xMin):0.5)*(w-2*pad);
  const sy=y=>pad+(yMax>yMin?1-(y-yMin)/(yMax-yMin):0.5)*(h-2*pad);
  const closed=data.closed!==false;
  const pathD=route.map((ci,i)=>{
    const c=cities[ci]; return (i===0?'M':'L')+sx(c[0]).toFixed(1)+' '+sy(c[1]).toFixed(1);
  }).join(' ')+(closed?' Z':'');
  let dots='';
  cities.forEach((c,i)=>{
    const isStart=route[0]===i;
    dots+=`<circle cx="${sx(c[0]).toFixed(1)}" cy="${sy(c[1]).toFixed(1)}" r="${isStart?6:4.5}" class="${isStart?'viz-dot-final':'viz-dot'}"/>`+
      `<text x="${sx(c[0]).toFixed(1)}" y="${(sy(c[1])-8).toFixed(1)}" class="viz-axis-label" text-anchor="middle">${i}</text>`;
  });
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}"><path d="${pathD}" class="viz-route-path"/>${dots}</svg>`;
}

function _vizTree(data){
  const nodes=data.nodes||[];
  if(!nodes.length) return '';
  const levels={};
  nodes.forEach(n=>{ (levels[n.level]=levels[n.level]||[]).push(n); });
  const maxLevel=Math.max(...nodes.map(n=>n.level));
  const w=440, levelH=48, padT=20;
  const h=padT*2+maxLevel*levelH;
  const byId={}; nodes.forEach(n=>{ byId[n.id]=n; });
  function xOf(n){
    const arr=levels[n.level];
    const slot=n.pos!=null?n.pos:arr.indexOf(n);
    return (w/(arr.length+1))*(slot+1);
  }
  function yOf(n){ return padT+n.level*levelH; }
  let edges='', circles='';
  nodes.forEach(n=>{
    const x=xOf(n), y=yOf(n);
    if(n.parent!=null && byId[n.parent]){
      const p=byId[n.parent];
      edges+=`<line x1="${xOf(p).toFixed(1)}" y1="${yOf(p).toFixed(1)}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" class="${n.pruned?'viz-edge-pruned':'viz-edge'}"/>`;
    }
    const nodeCls=n.pruned?'viz-node-pruned':(n.final?'viz-node-final':'viz-node');
    circles+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="13" class="${nodeCls}"/>`+
      `<text x="${x.toFixed(1)}" y="${(y+4).toFixed(1)}" class="viz-node-label" text-anchor="middle">${esc(n.label!=null?String(n.label):'')}</text>`;
  });
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">${edges}${circles}</svg>`;
}

function _vizGrid(data){
  const rows=data.rows, cols=data.cols;
  const values=data.values||[];
  if(!rows || !cols) return '';
  const flat=values.flat();
  const min=(data.min!=null)?data.min:Math.min(...flat);
  const max=(data.max!=null)?data.max:Math.max(...flat);
  const rowLabels=data.rowLabels||null;
  const labelW=rowLabels?64:0;
  const padX=8, padY=8;

  // barMode: cada fila se dibuja como barras (altura = valor), no como
  // celdas planas de color -- para arrays comparables (p.ej. "antes/despues"
  // de ordenar) esto se lee de un vistazo, mientras que un mapa de calor de
  // numeros no dice nada sin leer celda por celda.
  if(data.barMode){
    const cell=28, gap=4, barAreaH=50, rowBandH=barAreaH+34;
    const w=padX*2+labelW+cols*(cell+gap)-gap;
    const h=padY*2+rows*rowBandH;
    let out='';
    for(let r=0;r<rows;r++){
      const bandTop=padY+r*rowBandH;
      const baseline=bandTop+barAreaH+16;
      if(rowLabels && rowLabels[r]!=null)
        out+=`<text x="${padX}" y="${(baseline+4).toFixed(1)}" class="viz-label">${esc(rowLabels[r])}</text>`;
      for(let c=0;c<cols;c++){
        const v=values[r][c];
        const t=max>min?(v-min)/(max-min):0.5;
        const barH=Math.max(2, t*barAreaH);
        const x=padX+labelW+c*(cell+gap);
        const barY=baseline-barH;
        const label=(data.cellText && data.cellText[r])?data.cellText[r][c]:(typeof v==='number'?_vizFmtNum(v):'');
        out+=`<rect x="${x.toFixed(1)}" y="${barY.toFixed(1)}" width="${cell}" height="${barH.toFixed(1)}" rx="3" class="viz-grid-cell"/>`+
          (label!==''?`<text x="${(x+cell/2).toFixed(1)}" y="${(barY-4).toFixed(1)}" class="viz-grid-text" text-anchor="middle">${esc(String(label))}</text>`:'');
      }
      out+=`<line x1="${padX+labelW}" y1="${baseline.toFixed(1)}" x2="${(padX+labelW+cols*(cell+gap)-gap).toFixed(1)}" y2="${baseline.toFixed(1)}" class="viz-axis"/>`;
    }
    return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">${out}</svg>`;
  }

  const cell=36, gap=3;
  const w=padX*2+labelW+cols*(cell+gap)-gap, h=padY*2+rows*(cell+gap)-gap;
  let rects='';
  for(let r=0;r<rows;r++){
    if(rowLabels && rowLabels[r]!=null){
      const ly=padY+r*(cell+gap)+cell/2+4;
      rects+=`<text x="${padX}" y="${ly.toFixed(1)}" class="viz-label">${esc(rowLabels[r])}</text>`;
    }
    for(let c=0;c<cols;c++){
      const v=values[r][c];
      const t=max>min?(v-min)/(max-min):0.5;
      const x=padX+labelW+c*(cell+gap), y=padY+r*(cell+gap);
      const label=(data.cellText && data.cellText[r])?data.cellText[r][c]:(typeof v==='number'?_vizFmtNum(v):'');
      rects+=`<rect x="${x}" y="${y}" width="${cell}" height="${cell}" rx="4" class="viz-grid-cell" style="fill-opacity:${(0.15+t*0.85).toFixed(2)}"/>`+
        (label!==''?`<text x="${x+cell/2}" y="${y+cell/2+4}" class="viz-grid-text" text-anchor="middle">${esc(String(label))}</text>`:'');
    }
  }
  return `<svg viewBox="0 0 ${w} ${h}" class="viz-svg" role="img" aria-label="${esc(data.aria||'')}">${rects}</svg>`;
}

function renderConceptViz(viz){
  if(!viz || !viz.type) return '';
  try{
    switch(viz.type){
      case 'bar': return _vizBar(viz.data||{});
      case 'curve': return _vizCurve(viz.data||{});
      case 'membership': return _vizMembership(viz.data||{});
      case 'route': return _vizRoute(viz.data||{});
      case 'tree': return _vizTree(viz.data||{});
      case 'grid': return _vizGrid(viz.data||{});
      case 'contour': return _vizContour(viz.data||{});
      case 'boundary': return _vizBoundary(viz.data||{});
      default: return '';
    }
  }catch(e){ console.error('renderConceptViz', e); return ''; }
}
