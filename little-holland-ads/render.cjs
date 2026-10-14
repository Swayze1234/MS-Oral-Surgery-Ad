// Renders an ad page (index.html with window.seek(t)) to video, frame by frame.
//
//   node render.cjs ad1-dui-students --name LittleHolland_DUI_Students_15s
//   node render.cjs ad1-dui-students --stills 0.5,2.5,6,9.5,13.5      # preview PNGs only
//
// Options: --scale 2 (supersample factor), --workers 4 (parallel browser pages)
// Frames are captured at 2x (3840x2160) and downsampled to 1920x1080 for extra-clean edges.
// If the ad folder has a prepare.sh, it runs first (ad1 uses it to extract its footage frames).
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn, execFileSync } = require('child_process');

let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

const adDir = process.argv[2];
if (!adDir) { console.error('usage: node render.cjs <ad-folder> [--name N] [--stills t1,t2] [--scale 2] [--workers 4]'); process.exit(1); }
const arg = (name, def) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : def; };
const SCALE = Number(arg('--scale', '2'));
const WORKERS = Number(arg('--workers', String(Math.max(1, os.cpus().length))));
const stills = arg('--stills', null);
const name = arg('--name', adDir);

const root = __dirname;
const pageUrl = 'file://' + path.join(root, adDir, 'index.html') + '?render';
const outDir = path.join(root, 'out');
const workDir = path.join(root, '.work', adDir);
const framesDir = path.join(workDir, 'frames');
fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(workDir, { recursive: true });

const ffmpeg = (args) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args], { stdio: 'inherit' });

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: SCALE });
  await page.goto(pageUrl);
  await page.evaluate(() => window.ready);
  return page;
}

// optional per-ad prep step (e.g. extracting footage frames)
const prep = path.join(root, adDir, 'prepare.sh');
if (fs.existsSync(prep)) execFileSync(prep, { stdio: 'inherit' });

(async () => {
  const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none'] });

  if (stills) {
    const page = await openPage(browser);
    for (const s of stills.split(',').map(Number)) {
      await page.evaluate(t => window.seek(t), s);
      const raw = path.join(workDir, `_raw.png`), file = path.join(workDir, `still_${s.toFixed(2)}.png`);
      await page.screenshot({ path: raw, type: 'png' });
      ffmpeg(['-i', raw, '-vf', 'scale=1920:1080:flags=lanczos', file]);
      console.log('wrote', file);
    }
    await browser.close();
    return;
  }

  // 1) capture every frame (parallel pages, interleaved frames)
  const page0 = await openPage(browser);
  const { FPS, DURATION } = await page0.evaluate(() => ({ FPS: window.FPS, DURATION: window.DURATION }));
  const total = Math.round(FPS * DURATION);
  fs.rmSync(framesDir, { recursive: true, force: true });
  fs.mkdirSync(framesDir, { recursive: true });
  const pages = [page0, ...await Promise.all(Array.from({ length: WORKERS - 1 }, () => openPage(browser)))];
  const t0 = Date.now();
  let done = 0;
  await Promise.all(pages.map(async (page, w) => {
    for (let f = w; f < total; f += WORKERS) {
      await page.evaluate(t => window.seek(t), f / FPS);
      await page.screenshot({ path: path.join(framesDir, `${String(f).padStart(5, '0')}.png`), type: 'png' });
      if (++done % 30 === 0) console.log(`frame ${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
  await browser.close();
  console.log(`captured ${total} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);

  // 2) downsample to 1080p into a lossless intermediate
  const master = path.join(workDir, 'master_rgb.mkv');
  ffmpeg(['-framerate', String(FPS), '-i', path.join(framesDir, '%05d.png'), '-vf', 'scale=1920:1080:flags=lanczos',
    '-c:v', 'ffv1', '-pix_fmt', 'bgr0', master]);

  // 3) encode deliverables (BT.709, yuv420p, H.264 High, no audio)
  const color = ['-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv'];
  const hq = path.join(outDir, `${name}_1080p_MASTER.mp4`);
  ffmpeg(['-i', master, ...color, '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-profile:v', 'high', '-level', '4.2',
    '-tune', 'animation', '-r', String(FPS), '-movflags', '+faststart', '-an', hq]);
  console.log('wrote', hq);

  // MCTV network spec: 1920x1080 MP4, 300–700 kb/s, < 20 MB. Two-pass for best quality at that bitrate.
  const net = path.join(outDir, `${name}_1080p_MCTV_700k.mp4`);
  const passlog = path.join(workDir, 'x264pass');
  const common = ['-i', master, ...color, '-c:v', 'libx264', '-preset', 'veryslow', '-tune', 'animation', '-profile:v', 'high',
    '-level', '4.2', '-b:v', '640k', '-maxrate', '700k', '-bufsize', '1400k', '-x264-params', 'aq-mode=3',
    '-r', String(FPS), '-passlogfile', passlog, '-an'];
  ffmpeg([...common, '-pass', '1', '-f', 'mp4', '/dev/null']);
  ffmpeg([...common, '-pass', '2', '-movflags', '+faststart', net]);
  console.log('wrote', net);
})().catch(e => { console.error(e); process.exit(1); });
