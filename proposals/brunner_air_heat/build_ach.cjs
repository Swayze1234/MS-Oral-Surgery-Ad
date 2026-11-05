// Renders ach_form.html to PDF and records each [data-field] box (in PDF points).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = __dirname;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'ach_form.html'), { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  const fields = await page.$$eval('[data-field]', els => els.map(e => {
    const r = e.getBoundingClientRect();
    return { name: e.dataset.field, type: e.dataset.type || 'text', x0: r.left, y0: r.top, x1: r.right, y1: r.bottom };
  }));
  const pt = v => +(v * 0.75).toFixed(2);
  fs.writeFileSync(path.join(dir, 'ach_fields.json'), JSON.stringify(fields.map(f => ({ ...f, x0: pt(f.x0), y0: pt(f.y0), x1: pt(f.x1), y1: pt(f.y1) })), null, 1));
  await page.pdf({ path: path.join(dir, 'ach_form_flat.pdf'), preferCSSPageSize: true, printBackground: true });
  await browser.close();
  console.log('fields:', fields.length);
})();
