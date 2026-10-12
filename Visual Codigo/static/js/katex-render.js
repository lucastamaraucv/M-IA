/* ──────────── Renderizado de fórmulas (KaTeX) en AO/RA/AS ────────────
   Modo Maestro Matemáticas ya usa KaTeX (ver _mathRenderKatex en
   master-math.js) — aquí se extiende lo mismo a los paneles de Teoría y
   Quiz de AO/RA/AS, que hasta ahora mostraban fórmulas como texto plano
   con símbolos Unicode (², ⁴, Σ...) en vez de tipografía matemática real.

   Truco de bajo riesgo: en vez de editar las funciones de render de cada
   modo (_aoRenderTheory, _raRenderTheory, _asRenderTheory — todas viven en
   archivos que otro proceso puede estar tocando a la vez), se ENVUELVEN
   por fuera: se guarda la función original y se reemplaza por una versión
   que llama a la original y LUEGO aplica KaTeX sobre el contenedor. Un
   `function nombre(){}` de nivel superior cuelga de `window` en el
   navegador, así que reasignar `window[nombre]` redirige también a quien
   la llame sin cualificar (`_aoRenderTheory()` dentro de `_aoGoTo()`
   sigue resolviendo al mismo `window._aoRenderTheory`).

   Las fórmulas deben escribirse entre `$...$` (inline) o `$$...$$` (en
   bloque) en el texto de `theory`/`question`/`solution` para que KaTeX las
   reconozca — el texto que no use esos delimitadores se muestra igual que
   antes, sin cambios. */
function _renderKatexIn(containerId){
  if(!window.renderMathInElement) return;
  const el=document.getElementById(containerId);
  if(!el) return;
  try{
    renderMathInElement(el, {
      delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
      throwOnError:false
    });
  }catch(e){}
}
function _wrapRenderWithKatex(fnName, containerId){
  const orig=window[fnName];
  if(typeof orig!=='function') return;
  window[fnName]=function(...args){
    const result=orig.apply(this, args);
    _renderKatexIn(containerId);
    return result;
  };
}
_wrapRenderWithKatex('_aoRenderTheory', 'aoTheoryBody');
_wrapRenderWithKatex('_aoShowQuizSolution', 'aoQuizSolutionBody');
_wrapRenderWithKatex('_raRenderTheory', 'raTheoryBody');
_wrapRenderWithKatex('_raShowQuizSolution', 'raQuizSolutionBody');
_wrapRenderWithKatex('_asRenderTheory', 'asTheoryBody');
_wrapRenderWithKatex('_asShowQuizSolution', 'asQuizSolutionBody');
_wrapRenderWithKatex('_nsRenderTheory', 'nsTheoryBody');
_wrapRenderWithKatex('_nsShowQuizSolution', 'nsQuizSolutionBody');
_wrapRenderWithKatex('_rnRenderTheory', 'rnTheoryBody');
_wrapRenderWithKatex('_rnShowQuizSolution', 'rnQuizSolutionBody');
_wrapRenderWithKatex('_rfRenderTheory', 'rfTheoryBody');
_wrapRenderWithKatex('_rfShowQuizSolution', 'rfQuizSolutionBody');
