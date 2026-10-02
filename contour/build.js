// Renders the Contour one-pager and insertion order from HTML to PDF.
// Usage:  node contour/build.js            (renders every *.html in this folder)
//         node contour/build.js onepager   (renders just onepager.html)
// Needs the playwright package (node) and its bundled Chromium.
// Exits 1 if any .page block holds more content than fits on it: Chromium's
// multicolumn and absolute-position fragmentation can paint overflow under the
// next page's header without changing the PDF page count, so the count alone
// does not catch it.
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
  let failed = false;
  for (const f of targets) {
    const page = await browser.newPage();
    await page.emulateMedia({ media: 'print' });
    // Load by file URL so relative assets (the fonts/ folder) resolve.
    await page.goto('file://' + path.join(here, f), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const overflow = await page.evaluate(() => {
      const PT = 72 / 96;
      return Array.from(document.querySelectorAll('.page'))
        .map((pg, i) => ({ page: i + 1, scroll: pg.scrollHeight * PT, client: pg.clientHeight * PT }))
        .filter(p => p.scroll > p.client + 0.5);
    });
    for (const o of overflow) {
      console.error(`${f}: .page ${o.page} overflows, content ${o.scroll.toFixed(1)}pt in a ${o.client.toFixed(1)}pt page`);
      failed = true;
    }
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
  if (failed) process.exit(1);
})().catch(e => { console.error(e); process.exit(1); });
