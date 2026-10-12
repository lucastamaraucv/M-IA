/* ──────────── Test E2E en navegador real (Playwright + Chromium headless) ────────────
   A diferencia de los demás verify/*_test.js (que simulan el DOM con un vm de Node,
   sin navegador real), este abre la app de verdad en Chromium headless y escucha:
     - console.error / console.warn del navegador (errores de JS reales, no simulados)
     - 'pageerror' (excepciones no capturadas)
     - respuestas HTTP >= 400 de cualquier request (exactamente el tipo de fallo que
       causó el "Unexpected token '<'" del Cuaderno de errores: un endpoint que
       devuelve HTML de error 404 en vez de JSON, porque el servidor no se había
       reiniciado con el código nuevo)
   Pensado para correr DESPUÉS de cada mejora, contra el servidor real ya arrancado.
   Uso: BASE_URL=http://127.0.0.1:5000 node verify/e2e_browser_test.js */
const { chromium } = require('playwright');

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5000';
const consoleErrors = [];
const pageErrors = [];
const badResponses = [];
let checks = 0, fails = 0;

function record(label, ok, detail) {
  checks++;
  console.log((ok ? 'OK   ' : 'FAIL ') + '— ' + label);
  if (!ok) { fails++; if (detail) console.log('     ' + detail); }
}

async function openPanel(page, btnSelector, panelSelector) {
  // Los botones de Modo Maestro ahora viven detrás del desplegable "🎓
  // Cursos" (barra de estudio) y arrancan con display:none -- si el botón
  // pedido no está visible todavía, se abre el desplegable primero. Los
  // botones de herramientas (Reporte, Errores, etc.) siguen visibles
  // directamente, así que para esos este paso es un no-op.
  if (!(await page.locator(btnSelector).isVisible().catch(() => false))) {
    await page.click('#bCursosToggle');
    await page.waitForTimeout(150);
  }
  await page.click(btnSelector);
  await page.waitForSelector(panelSelector, { state: 'visible', timeout: 15000 });
}

/* Recorre un Modo Maestro (AO/RA/AS): abre el panel, responde la pregunta rápida
   (mc: hace clic en la primera opción -- si es incorrecta, ejercita el camino de
   whyNot/Cuaderno de errores; numeric: escribe un valor cualquiera), pide la
   solución, y avanza de tema unas pocas veces -- no las 41/35/21 completas, es un
   smoke pass tras cada mejora, no un recorrido exhaustivo (para eso están los
   *_smoke_test.js existentes). */
async function walkMaster(page, prefix, toggleBtn, panelSel, topics, expectApplication) {
  await openPanel(page, toggleBtn, panelSel);
  for (let t = 0; t < topics; t++) {
    if (expectApplication) {
      const appVisible = await page.locator('#' + prefix + 'ApplicationBlock').isVisible();
      const appText = await page.locator('#' + prefix + 'ApplicationBody').textContent().catch(() => '');
      record(prefix + ' tema ' + t + ': panel "Aplicación real" visible con contenido', appVisible && appText.length > 20, 'visible=' + appVisible + ' len=' + appText.length);
    }
    const optWrap = page.locator('#' + prefix + 'QuizOptions');
    const numWrap = page.locator('#' + prefix + 'QuizNumericWrap');
    await page.waitForTimeout(300); // deja que _xxRenderQuiz termine de pintar
    if (t === 0) {
      const copyBtn = page.locator('#' + prefix + 'QuizCopyBtn');
      await copyBtn.click();
      await page.waitForTimeout(200);
      const copyBtnText = await copyBtn.textContent();
      record(prefix + ': "Copiar pregunta y código" confirma con el flash "✅ Copiado"', /Copiado/.test(copyBtnText), copyBtnText);
    }
    if (await optWrap.isVisible()) {
      const firstOption = optWrap.locator('button.math-option').first();
      await firstOption.click();
      await page.waitForTimeout(150);
      const fbText = await page.locator('#' + prefix + 'QuizFeedback').textContent();
      record(prefix + ' tema ' + t + ': respondió pregunta mc', !!fbText && fbText.length > 3, fbText);
      const solBtn = page.locator('#' + prefix + 'QuizSolutionBtn');
      if (await solBtn.isVisible()) await solBtn.click();
    } else if (await numWrap.isVisible()) {
      await page.fill('#' + prefix + 'QuizNumericInput', '1');
      await page.click('#' + prefix + 'QuizNumericWrap button');
      await page.waitForTimeout(150);
      record(prefix + ' tema ' + t + ': respondió pregunta numeric', true);
    } else {
      record(prefix + ' tema ' + t + ': ni mc ni numeric visible', false, 'ningún wrap de pregunta visible');
    }
    const nextBtn = page.locator('#mNext' + prefix[0].toUpperCase() + prefix.slice(1));
    if (await nextBtn.isVisible()) await nextBtn.click();
    await page.waitForTimeout(200);
  }
}

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => pageErrors.push(err.message));
  page.on('response', res => {
    if (res.status() >= 400) badResponses.push(res.status() + ' ' + res.url());
  });

  await page.goto(BASE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  record('Página principal carga', true);

  // Barra de estudio reorganizada: los 5 botones de Modo Maestro empiezan
  // ocultos dentro del desplegable "🎓 Cursos" (no listados sueltos en la
  // barra), se ven al abrirlo, y un clic fuera lo cierra sin navegar a
  // ningún curso.
  record('Cursos: el menú arranca cerrado', !(await page.locator('#cursosMenu').isVisible()));
  await page.click('#bCursosToggle');
  await page.waitForTimeout(150);
  record('Cursos: el menú se abre y muestra los 5 cursos', await page.locator('#cursosMenu').isVisible() && await page.locator('#bMasterAo').isVisible() && await page.locator('#bMasterAs').isVisible());
  await page.click('.hbrand'); // clic fuera del menú, en un elemento neutral del header
  await page.waitForTimeout(150);
  record('Cursos: un clic fuera cierra el menú sin abrir ningún curso', !(await page.locator('#cursosMenu').isVisible()) && !(await page.locator('#masterAoBar').isVisible()));

  await walkMaster(page, 'ao', '#bMasterAo', '#masterAoBar', 3, true);
  await walkMaster(page, 'ra', '#bMasterRa', '#masterRaBar', 3, true);
  await walkMaster(page, 'as', '#bMasterAs', '#masterAsBar', 3, true);

  // Repaso mezclado: mezcla lo ya completado (los temas recorridos arriba)
  await openPanel(page, '#bReview', '#reviewBar');
  await page.waitForTimeout(400);
  // Solo se completaron temas ao/ra/as arriba, así que el sorteo debe caer
  // en uno de esos -- confirma que el código real queda visible junto a la
  // pregunta (la mejora pedida: "no puedo entrar en contexto si no está
  // ahí mismo el código Python y su emulación").
  const mainVisibleInReview = await page.locator('.main').isVisible();
  const codeInputLen = await page.locator('#codeInput').inputValue().then(v => v.length).catch(() => 0);
  record('Repaso mezclado: muestra el código real (.main visible + codeInput con contenido)',
    mainVisibleInReview && codeInputLen > 0, 'mainVisible=' + mainVisibleInReview + ' codeInputLen=' + codeInputLen);
  const reviewCopyBtn = page.locator('#reviewCopyBtn');
  await reviewCopyBtn.click();
  await page.waitForTimeout(200);
  const reviewCopyBtnText = await reviewCopyBtn.textContent();
  record('Repaso mezclado: "Copiar pregunta y código" confirma con el flash "✅ Copiado"', /Copiado/.test(reviewCopyBtnText), reviewCopyBtnText);
  const reviewOpt = page.locator('#reviewOptions button.math-option').first();
  if (await reviewOpt.isVisible().catch(() => false)) {
    await reviewOpt.click();
    await page.waitForTimeout(150);
    record('Repaso mezclado: respondió una pregunta', true);
  } else {
    record('Repaso mezclado: panel abierto (sin pregunta mc disponible aún, puede ser numeric/py)', true);
  }

  // Cuaderno de errores: la mejora que se pidió verificar explícitamente --
  // si el servidor no se reinició, esto es justo donde aparecería el
  // "Unexpected token '<'" reportado antes.
  await openPanel(page, '#bErrors', '#errorJournalBar');
  await page.waitForTimeout(600);
  const errorsBody = await page.locator('#errorJournalBody').textContent();
  const loadFailed = errorsBody.includes('No se pudo cargar');
  record('Cuaderno de errores: carga sin el error "No se pudo cargar"', !loadFailed, errorsBody.slice(0, 200));
  const hasCards = await page.locator('.errors-card').count();
  record('Cuaderno de errores: tiene al menos 1 tarjeta (se generó whyNot arriba)', hasCards > 0, 'tarjetas encontradas: ' + hasCards);
  if (hasCards > 0) {
    const firstCard = page.locator('.errors-card').first();
    const ruleBox = firstCard.locator('.errors-rule-input');
    await ruleBox.fill('Regla de prueba del test E2E — verificar que el guardado funciona.');
    await firstCard.locator('button:has-text("Guardar regla")').click();
    await page.waitForTimeout(600);
    const savedVisible = await firstCard.locator('.errors-rule-saved').isVisible();
    record('Cuaderno de errores: guardar "regla personal" funciona', savedVisible);
  }

  // Reporte: confirma las 2 gráficas nuevas (barras de comparación entre
  // cursos + radar por tema dentro de cada curso, reemplazan al radar de
  // 3 ejes que "no decía mucho").
  await openPanel(page, '#bReport', '#reportBar');
  await page.waitForTimeout(500);
  record('Reporte: panel abre sin errores', true);
  const compareBars = await page.locator('.report-compare-wrap').count();
  record('Reporte: barras de comparación entre cursos presentes', compareBars > 0, 'encontradas: ' + compareBars);
  const topicRadars = await page.locator('.report-topic-radar-wrap').count();
  record('Reporte: radar por tema presente (al menos 1 curso con datos)', topicRadars > 0, 'encontrados: ' + topicRadars);
  const oldRadarGone = await page.locator('.report-radar-wrap').count();
  record('Reporte: el radar viejo de 3 ejes ya no existe', oldRadarGone === 0, 'restantes: ' + oldRadarGone);

  // Refuerzo guiado (modo enfocado): llama _focusStart directamente en vez
  // de depender de que el sorteo aleatorio de arriba haya producido un
  // cluster real (no siempre lo hace) -- prueba determinista del mecanismo
  // en sí: navega solo los temas del "bloque", con banner + prompt de
  // recuerdo, y "Entendido, siguiente" avanza DENTRO del bloque, no al
  // temario completo.
  await page.evaluate(() => { _focusStart('ao', [8, 16], 'Prueba E2E'); });
  await page.waitForTimeout(400);
  const focusBannerVisible = await page.locator('#aoFocusBanner').isVisible();
  const focusBannerText = await page.locator('#aoFocusBanner').textContent();
  record('Refuerzo guiado: banner de modo enfocado visible con progreso', focusBannerVisible && /1\/2/.test(focusBannerText), focusBannerText);
  const recallVisible = await page.locator('#aoFocusRecallBlock').isVisible();
  record('Refuerzo guiado: prompt de recuperación activa visible antes de la teoría', recallVisible);
  let aoPosAfterStart = await page.evaluate(() => _aoPos);
  record('Refuerzo guiado: navegó al primer tema del bloque (idx 8)', aoPosAfterStart === 8, 'aoPos=' + aoPosAfterStart);

  await page.click('#mNextAo');
  await page.waitForTimeout(300);
  let aoPosAfterNext = await page.evaluate(() => _aoPos);
  record('Refuerzo guiado: "siguiente" avanzó al 2º tema del BLOQUE (idx 16), no al temario completo', aoPosAfterNext === 16, 'aoPos=' + aoPosAfterNext);

  await page.click('#mNextAo');
  await page.waitForTimeout(300);
  const focusModeAfterFinish = await page.evaluate(() => _focusMode);
  const bannerAfterFinish = await page.locator('#aoFocusBanner').textContent();
  record('Refuerzo guiado: terminó el bloque y limpió el modo enfocado', focusModeAfterFinish === null, 'bannerAfterFinish=' + bannerAfterFinish.slice(0, 80));
  await page.click('#aoFocusBanner button');
  await page.waitForTimeout(200);

  // Simulacro de examen: abrir, empezar el de AO, responder 2 preguntas SIN
  // que aparezca feedback inmediato ni opción de reintento (a diferencia de
  // todo lo demás en la app), forzar el fin (como timeout, sin esperar 60
  // min reales) y confirmar que los resultados se ven coherentes.
  await openPanel(page, '#bExam', '#examBar');
  await page.waitForTimeout(300);
  const examCounts = await page.locator('#examCountAo').textContent();
  record('Simulacro: selector muestra el conteo de preguntas de AO', /\d+ preguntas/.test(examCounts), examCounts);
  await page.click('button[onclick="_examStart(\'ao\')"]');
  await page.waitForTimeout(300);
  record('Simulacro: cronómetro visible al empezar', await page.locator('#examTimer').isVisible());

  for (let i = 0; i < 2; i++) {
    const optWrap = page.locator('#examOptions');
    const numWrap = page.locator('#examNumericWrap');
    await page.waitForTimeout(150);
    if (await optWrap.isVisible()) {
      await optWrap.locator('button.math-option').first().click();
      const hasCorrectClass = await optWrap.locator('.math-option-correct, .math-option-wrong').count();
      record('Simulacro pregunta ' + i + ': NO revela correcto/incorrecto al elegir (examen real)', hasCorrectClass === 0, 'clases correct/wrong encontradas: ' + hasCorrectClass);
      const retryVisible = await page.locator('#examSolutionBtn').count();
      record('Simulacro pregunta ' + i + ': sin botón de "ver solución" (no existe en examen)', retryVisible === 0);
    } else if (await numWrap.isVisible()) {
      await page.fill('#examNumericInput', '1');
    }
    await page.click('#examNextBtn');
  }

  // Forzar el fin como si se hubiera agotado el tiempo (sin esperar 1h real)
  await page.evaluate(() => _examFinish(true));
  await page.waitForTimeout(300);
  const resultsVisible = await page.locator('#examResultsView').isVisible();
  const resultsText = await page.locator('#examResultsBody').textContent();
  record('Simulacro: pantalla de resultados aparece con nota', resultsVisible && /\d+\/\d+/.test(resultsText), resultsText.slice(0, 150));

  // Captura de razonamiento por botones (¿qué otra opción dudaste? + ¿por
  // qué elegiste la tuya?): contra el servidor real -- /record_reasoning
  // solo persiste, no llama a Claude, así que no hace falta mockear nada.
  // toggleMasterAo() es un TOGGLE de verdad (si _aoOn ya es true, CIERRA el
  // panel en vez de abrirlo) -- exitMasterAo() primero es idempotente
  // (seguro llamarlo aunque ya esté cerrado) y garantiza que el toggle que
  // sigue realmente abra el panel, sin depender de en qué estado haya
  // quedado el flujo de arriba (Refuerzo guiado ya lo dejó abierto).
  await page.evaluate(() => { exitMasterAo(); toggleMasterAo(); _aoGoTo(3); });
  await page.waitForTimeout(300);
  const mcOptSel = '#aoQuizOptions .math-option';
  if (await page.locator(mcOptSel).count() > 0) {
    await page.locator(mcOptSel).first().click();
    await page.waitForTimeout(300);
    const reasonVisible = await page.locator('#aoQuizReason').isVisible();
    record('Razonamiento: el prompt "¿qué otra opción dudaste?" aparece tras responder', reasonVisible);
    const reasonText = await page.locator('#aoQuizReason').textContent();
    record('Razonamiento: ofrece "Ninguna, estaba seguro" como opción', /Ninguna, estaba seguro/.test(reasonText));
    await page.locator('#aoQuizReason button:has-text("Ninguna, estaba seguro")').click();
    await page.waitForTimeout(200);
    const tagsText = await page.locator('#aoQuizReason').textContent();
    record('Razonamiento: tras "ninguna" aparecen los 5 motivos', /Lo sabía por la teoría/.test(tagsText) && /Adiviné/.test(tagsText));
    await page.locator('#aoQuizReason button:has-text("Adiviné")').click();
    await page.waitForTimeout(300);
    const doneText = await page.locator('#aoQuizReason').textContent();
    record('Razonamiento: confirma "✓ Registrado" tras elegir el motivo (persistido de verdad)', /Registrado/.test(doneText));
  } else {
    record('Razonamiento: AO tema 3 tenía una pregunta numérica en este banco, se omite (no aplica)', true);
  }

  // Diagnóstico automático de IA en clusters débiles (_reportClusterCards →
  // /analyze_patterns): esa ruta SÍ invoca al CLI real de Claude, lento y
  // con coste -- se intercepta con page.route para devolver una respuesta
  // simulada y solo confirmar que el frontend la pinta, sin gastar una
  // llamada real en cada corrida del E2E. Se usa una familia/idxs que no
  // puede coincidir con ningún cluster real detectado arriba (evita un
  // cache-hit con un resultado real ya guardado bajo la misma clave).
  await page.route('**/analyze_patterns', route => route.fulfill({
    status: 200, contentType: 'application/json',
    body: JSON.stringify({ ok: true, diagnosis: 'Diagnóstico simulado E2E: confusión de prueba entre dos conceptos.' }),
  }));
  // Usamos un mode falso ('zzztest') para el id del div, no 'ao' -- el
  // recorrido de arriba pudo haber generado de verdad un cluster real de AO
  // (contestamos varias preguntas mal a propósito), y ese cluster real ya
  // pinta su propio elemento con id="clusterDiag_ao" dentro de #reportBody.
  // Reusar ese mismo id aquí crearía un id duplicado en el DOM (inválido) y
  // el locator de Playwright fallaría por ambigüedad -- con un mode inventado
  // el id nuevo no puede chocar con ningún id que la app real genere.
  await page.evaluate(() => {
    const d = document.createElement('div');
    d.id = 'clusterDiag_zzztest';
    document.body.appendChild(d);
  });
  await page.evaluate(() => { _reportFetchDiagnosis('zzztest', 'ZZZ_TEST_ONLY_E2E', [9999]); });
  await page.waitForTimeout(300);
  const diagText = await page.locator('#clusterDiag_zzztest').textContent().catch(() => '');
  record('Diagnóstico de cluster: el frontend pinta la respuesta simulada de /analyze_patterns', /Diagnóstico simulado E2E/.test(diagText), diagText);
  await page.unroute('**/analyze_patterns');

  await browser.close();

  console.log('\n── Errores de consola del navegador (console.error) ──');
  if (!consoleErrors.length) console.log('(ninguno)');
  consoleErrors.forEach(e => console.log('  •', e.slice(0, 300)));

  console.log('\n── Excepciones no capturadas (pageerror) ──');
  if (!pageErrors.length) console.log('(ninguna)');
  pageErrors.forEach(e => console.log('  •', e.slice(0, 300)));

  console.log('\n── Respuestas HTTP >= 400 ──');
  if (!badResponses.length) console.log('(ninguna)');
  badResponses.forEach(e => console.log('  •', e));

  const totalFails = fails + consoleErrors.length + pageErrors.length + badResponses.length;
  console.log('\n' + checks + ' comprobaciones — ' + (totalFails === 0 ? 'TODO OK, 0 errores' : totalFails + ' PROBLEMA(S) ENCONTRADO(S)'));
  process.exit(totalFails === 0 ? 0 : 1);
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
