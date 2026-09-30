// Renders ad.html frame-by-frame with headless Chromium and encodes an H.264 MP4.
//   node render.cjs                      -> out/uno-mas-oxford-30s-1920x1080.mp4
//   node render.cjs --preview 1,2.5,4    -> out/preview_<t>.png stills for a quick look
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const FPS = 30, DUR = 30, W = 1920, H = 1080;
const args = process.argv.slice(2);
const arg = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const preview = args.includes('--preview') ? arg('--preview').split(',').map(Number) : null;
const outFile = arg('--out', 'out/uno-mas-oxford-30s-1920x1080.mp4');
const ffmpeg = process.env.FFMPEG ||
  execSync('python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"').toString().trim();

(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('pageerror', e => { console.error('PAGE ERROR', e); process.exit(1); });
  page.on('console', m => { if (m.type() === 'error' && !/ERR_FILE_NOT_FOUND/.test(m.text())) console.error('CONSOLE', m.text()); });
  await page.goto('file://' + path.resolve(__dirname, 'ad.html'));
  await page.evaluate(() => window.adReady);
  fs.mkdirSync(path.dirname(path.resolve(outFile)), { recursive: true });
  fs.mkdirSync(path.resolve('out'), { recursive: true });

  if (preview) {
    for (const t of preview) {
      await page.evaluate(t => window.render(t), t);
      await page.screenshot({ path: `out/preview_${t.toFixed(2)}.png`, type: 'png' });
      console.log('preview', t);
    }
    await browser.close();
    return;
  }

  const ff = spawn(ffmpeg, [
    '-y', '-hide_banner', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-level', '4.1',
    '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', '-an',
    outFile,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const write = buf => new Promise(res => (ff.stdin.write(buf) ? res() : ff.stdin.once('drain', res)));

  const total = FPS * DUR, t0 = Date.now();
  for (let i = 0; i < total; i++) {
    const t = i / FPS;
    await page.evaluate(t => window.render(t), t);
    await write(await page.screenshot({ type: 'png' }));
    if (i % 90 === 0) console.log(`frame ${i}/${total}  t=${t.toFixed(2)}s  ${((Date.now() - t0) / 1000).toFixed(0)}s elapsed`);
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
  await browser.close();
  console.log('wrote', outFile, `in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})().catch(e => { console.error(e); process.exit(1); });
