"""Render ad/index.html frame-by-frame with Chromium, pipe frames to ffmpeg.

Usage: python3 render.py [--fps 30] [--dur 30] [--start S] [--stills] [--only-stills] [--preview]
  --stills       also save key frames as JPEG into output/stills
  --only-stills  just refresh those key frames, no video
  --preview      render at 10 fps for a quick check (writes *_preview.mp4, no spec encode)
  --start S      begin rendering at second S
"""
import argparse, os, subprocess, sys, time
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'output')
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

ap = argparse.ArgumentParser()
ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--dur', type=float, default=30.0)
ap.add_argument('--stills', action='store_true')
ap.add_argument('--preview', action='store_true')
ap.add_argument('--start', type=float, default=0.0)
ap.add_argument('--only-stills', action='store_true')
args = ap.parse_args()
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, 'stills'), exist_ok=True)

fps = args.fps if not args.preview else 10
n = int(round((args.dur - args.start) * fps))
master = os.path.join(OUT, 'OCG_30s_1920x1080_master' + ('_preview' if args.preview else '') + '.mp4')

STILL_TIMES = [0.9, 1.8, 3.2, 6.0, 12.0, 16.5, 21.5, 25.5, 29.0]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
    pg.goto('file://' + os.path.join(HERE, 'index.html'))
    pg.evaluate('window.__ready')
    pg.wait_for_timeout(300)

    if args.stills or args.only_stills:
        for st in STILL_TIMES:
            pg.evaluate(f'render({st})')
            pg.screenshot(path=os.path.join(OUT, 'stills', f'frame_{st:05.2f}s.jpg'), type='jpeg', quality=92)
        print('stills written')
    if args.only_stills:
        b.close(); sys.exit(0)

    cmd = [FFMPEG, '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-r', str(fps), master]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(n):
        t = args.start + i / fps
        pg.evaluate(f'render({t:.5f})')
        ff.stdin.write(pg.screenshot(type='jpeg', quality=96))
        if i % (fps * 2) == 0:
            print(f'  frame {i}/{n}  t={t:5.2f}s  {time.time()-t0:5.1f}s elapsed', flush=True)
    ff.stdin.close(); ff.wait()
    b.close()
print('master:', master, os.path.getsize(master) // 1024, 'KB')

if not args.preview:
    # MCTV spec version: 300-700 kb/s, <= 20 MB (two-pass, capped at 700 kb/s)
    spec = os.path.join(OUT, 'OCG_30s_1920x1080_MCTV.mp4')
    log = os.path.join(OUT, 'ffpass')
    common = ['-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.1', '-refs', '4', '-b:v', '650k', '-maxrate', '700k', '-bufsize', '1400k', '-pix_fmt', 'yuv420p', '-r', str(fps), '-an']
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', master, *common, '-pass', '1', '-passlogfile', log, '-f', 'null', '/dev/null'], check=True)
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', master, *common, '-pass', '2', '-passlogfile', log, '-movflags', '+faststart', spec], check=True)
    for f in os.listdir(OUT):
        if f.startswith('ffpass'): os.remove(os.path.join(OUT, f))
    print('spec:', spec, os.path.getsize(spec) // 1024, 'KB')
