// Genera la imagen del flujo (PNG) y el documento (PDF) a partir de los HTML de esta carpeta.
// Uso: node fuentes/render.js   (desde la carpeta ventanilla-unica)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const out = path.join(dir, '..');
  const browser = await chromium.launch();

  const flujo = await browser.newPage({ viewport: { width: 1900, height: 1000 }, deviceScaleFactor: 2 });
  await flujo.goto('file://' + path.join(dir, 'flujo.html'));
  await flujo.screenshot({ path: path.join(out, 'flujo_ventanilla_unica.png'), fullPage: true });

  const doc = await browser.newPage();
  await doc.goto('file://' + path.join(dir, 'documento.html'));
  await doc.waitForLoadState('networkidle');
  await doc.pdf({
    path: path.join(out, 'documento_funcionamiento.pdf'),
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '18mm', bottom: '18mm', left: '16mm', right: '16mm' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#6b7280;">Ventanilla Única Inteligente · Documento de funcionamiento · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
  });

  await browser.close();
})();
