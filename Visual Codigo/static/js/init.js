/* ──────────── Init ──────────── */
_migrateAoOrder(); // ver core.js: reordeno EX_AO 2026-08-09, esto remapea progreso viejo una sola vez
_migrateAoBatch345Order(); // ver core.js: inserté los batches 3-5 de AO EN MEDIO, remapea el progreso de Algoritmos Genéticos (+23)
document.getElementById('codeInput').value=EX[0].code;
renderLineNums();
renderExec(-1,-1);
updBtns();
autoLayout();
// Auto-run first example on page load
setTimeout(runCode, 400);

// _reviewDueCount() (deuda de repaso, ver calendar.js) lee los Sets
// _masterDone/_aoDone/_mathDone/_raDone/_asDone en memoria, no localStorage
// directo — sin este precargado, el banner marcaría "0 vencidos" en cada
// carga de página hasta que el usuario abriera algún Modo Maestro por su
// cuenta, justo lo que se quiere evitar.
_loadMasterProgress(); _loadAoProgress(); _loadMathProgress(); _loadRaProgress(); _loadAsProgress();

// Banner "hoy toca" (ver calendar.js): se recalcula al cargar, al volver a
// la pestaña y cada tanto mientras la pestaña sigue abierta, porque el
// progreso real de AO/RA/AS puede cambiar sin recargar la página.
_calRenderBanner();
window.addEventListener('focus', _calRenderBanner);
setInterval(_calRenderBanner, 10000);
