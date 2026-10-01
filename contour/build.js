// Renders the Contour one-pager and insertion order from HTML to PDF.
// Usage:  node contour/build.js            (renders every *.html in this folder)
//         node contour/build.js onepager   (renders just onepager.html)
// Needs the playwright package (node) and its bundled Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const here = __dirname;
const only = process.argv[2];
const targets = fs.readdirSync(here)
  .filter(f => f.endsWith('.html'))
  .filter(f => !only || f === only || f === only + '.html');

(async () => {
  const browser = await chromium.launch();
  for (const f of targets) {
    const page = await browser.newPage();
    const html = fs.readFileSync(path.join(here, f), 'utf8');
    await page.setContent(html, { waitUntil: 'load' });
    const out = path.join(here, f.replace(/\.html$/, '.pdf'));
    await page.pdf({
      path: out,
      format: 'Letter',
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      preferCSSPageSize: true,
    });
    await page.close();
    console.log('wrote', path.relative(process.cwd(), out));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
