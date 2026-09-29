/*
 * Renders ad.html to a 30-second, silent, 1920x1080 H.264 MP4 (MCTV spec:
 * 16:9, 300-700 kb/s, < 20 MB).  Every frame is produced by seeking the page's
 * CSS animations to an exact time, so the output is deterministic.
 *
 *   NODE_PATH=/opt/node22/lib/node_modules node render.js            # full video
 *   NODE_PATH=... STILLS=3,12,24 node render.js                        # preview PNGs only
 *   FFMPEG=/path/to/ffmpeg node render.js                             # custom ffmpeg
 */
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const FPS = 30, DURATION = 30, TOTAL = FPS * DURATION;
const OUT_DIR = path.join(__dirname, 'output');
const OUT = path.join(OUT_DIR, 'Tom_Smith_Land_Homes_30s.mp4');
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const STILLS = process.env.STILLS ? process.env.STILLS.split(',').map(Number) : null;

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'ad.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await page.waitForTimeout(400);
  await page.evaluate(() => window.__pauseAll());
  // let the compositor commit two frames after each seek so every tile is painted before capture
  const settle = () => page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));

  if (STILLS) {
    for (const sec of STILLS) {
      await page.evaluate(t => window.__seek(t), sec * 1000);
      await settle();
      const file = path.join(OUT_DIR, `still_${String(sec).replace('.', '_')}s.png`);
      await page.screenshot({ path: file });
      console.log('wrote', file);
    }
    await browser.close();
    return;
  }

  const ff = spawn(FFMPEG, [
    '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0',
    '-pix_fmt', 'yuv420p', '-b:v', '650k', '-maxrate', '700k', '-bufsize', '2100k',
    '-g', String(FPS * 2), '-an', '-movflags', '+faststart', OUT,
  ]);
  ff.stderr.on('data', d => process.stderr.write(d));
  const done = new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));

  for (let i = 0; i < TOTAL; i++) {
    await page.evaluate(t => window.__seek(t), i * 1000 / FPS);
    await settle();
    const buf = await page.screenshot({ type: 'jpeg', quality: 97 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${TOTAL}`);
  }
  ff.stdin.end();
  await done;
  await browser.close();
  console.log('wrote', OUT, (fs.statSync(OUT).size / 1e6).toFixed(2), 'MB');
})();
