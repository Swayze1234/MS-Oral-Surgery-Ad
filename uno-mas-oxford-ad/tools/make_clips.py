#!/usr/bin/env python3
"""Cut the 1-second shots we use out of the client's Vimeo video, slow them down with
motion interpolation, crop them to the size each scene needs, and write them out as
30 fps JPEG frame sequences under assets/clips/<name>/f0001.jpg ... plus a manifest.

    python3 tools/make_clips.py            # builds every clip (a few minutes)
    python3 tools/make_clips.py b_aerial   # rebuild just one

The source video is 1280x640 (2:1) at 23.976 fps and cuts every 1.0 s.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets/source/uno_mas_vimeo_720p.mp4')
OUT = os.path.join(ROOT, 'assets/clips')
try:
    import imageio_ffmpeg
    FFMPEG = os.environ.get('FFMPEG') or imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = os.environ.get('FFMPEG', 'ffmpeg')

# name: (source start s, duration s, slow factor, out w, out h, crop offset)
# crop offset is x for portrait-ish targets (source scaled to height) and y for
# wide targets (source scaled to width).
SHOTS = {
    # scene 3 — inside the polaroid card (924x617)
    'p_tacos':   (43.07, 0.94, 2.3, 924, 617, 155),
    'p_fries':   (30.06, 0.94, 2.3, 924, 617, 155),
    'p_fajitas': ( 4.03, 0.94, 2.3, 924, 617, 155),
    # scene 4 — full bleed (1920x1080)
    'f_bar':     (18.05, 0.94, 2.6, 1920, 1080, 120),   # Cathead shelf (shot 17 and 36 have holiday decor)
    'f_spread':  (45.08, 2.95, 1.1, 1920, 1080, 120),
    # scene 5 — the white Oxford building, postcard strip (1920x720)
    'b_aerial':  ( 0.03, 0.94, 2.2, 1920, 720, 110),
    'b_side':    (14.04, 1.06, 2.0, 1920, 720,   0),   # side view (shot 8 has a wreath + tree in frame)
    'b_wide':    (41.07, 0.94, 2.2, 1920, 720,  70),
}

def build(name):
    start, dur, slow, w, h, off = SHOTS[name]
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    if w / h > 2:   # wider than the 2:1 source -> scale to width, crop height
        sw, sh, cx, cy = w, w // 2, 0, off
    else:           # scale to height, crop width
        sw, sh, cx, cy = 2 * h, h, off, 0
    vf = (f"setpts={slow}*PTS,"
          "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
          f"scale={sw}:{sh}:flags=lanczos,crop={w}:{h}:{cx}:{cy},unsharp=5:5:0.5")
    cmd = [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{start:.3f}', '-t', f'{dur:.3f}',
           '-i', SRC, '-vf', vf, '-q:v', '2', os.path.join(d, 'f%04d.jpg')]
    subprocess.run(cmd, check=True)
    n = len([f for f in os.listdir(d) if f.endswith('.jpg')])
    print(f'{name}: {n} frames ({n/30:.2f}s) {w}x{h}', flush=True)
    return name, n

if __name__ == '__main__':
    names = sys.argv[1:] or list(SHOTS)
    os.makedirs(OUT, exist_ok=True)
    mpath = os.path.join(OUT, 'manifest.js')
    manifest = {}
    if os.path.exists(mpath):
        txt = open(mpath).read()
        manifest = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
    with ThreadPoolExecutor(max_workers=4) as ex:
        for name, n in ex.map(build, names):
            manifest[name] = n
    open(mpath, 'w').write('window.CLIP_MANIFEST=' + json.dumps(manifest) + ';\n')
    print('wrote', mpath, manifest)
