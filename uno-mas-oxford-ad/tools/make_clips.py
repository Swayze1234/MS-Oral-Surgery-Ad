#!/usr/bin/env python3
"""Cut the 1-second shots we use out of the client's Vimeo video, slow them down with
motion interpolation, grade and crop them to the size each scene needs, and write them
out as 30 fps JPEG frame sequences under assets/clips/<name>/f0001.jpg ... plus a manifest.

    python3 tools/make_clips.py            # builds every clip (a few minutes)
    python3 tools/make_clips.py b_aerial   # rebuild just one

The source video is 1280x640 (2:1) at 23.976 fps and cuts every 1.0 s. The last shot
(45.05 s on) fades to black from ~46.45 s, so f_spread stops before that.
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

# Light, per-type grades (applied after the crop, before the final sharpen).
GRADE = {
    'food': 'eq=contrast=1.06:saturation=1.14:gamma=0.98,colorbalance=rs=0.02:bs=-0.02:rm=0.02:bm=-0.03',
    'bar': 'eq=contrast=1.04:saturation=1.05',
    'ext': 'eq=saturation=1.06',
    'ext_warm': 'colorbalance=rm=0.04:bm=-0.04:rs=0.02:bs=-0.02,eq=saturation=1.06',
    'ext_lift': 'eq=gamma=1.12:brightness=0.02:saturation=1.08',
}

# start: source time (s); dur: source seconds; slow: slow-motion factor; w,h: output size;
# off: crop offset (x when the source is scaled to height, y when scaled to width);
# scale: optional explicit (sw, sh, cx, cy) override to zoom/crop differently.
SHOTS = {
    # scene 3 — inside the polaroid card (924x617): torta -> fajitas -> fries (headline order)
    'p_torta':   dict(start=20.05, dur=0.94, slow=2.3, w=924, h=617, off=155, grade='food'),
    'p_fajitas': dict(start=4.03,  dur=0.94, slow=2.3, w=924, h=617, off=155, grade='food'),
    'p_fries':   dict(start=30.06, dur=0.94, slow=2.3, w=924, h=617, off=155, grade='food'),
    # scene 4 — full bleed (1920x1080)
    'f_bar':     dict(start=18.05, dur=0.94, slow=2.6, w=1920, h=1080, off=120, grade='bar'),    # Cathead shelf (17 s / 36 s have holiday decor)
    'f_spread':  dict(start=45.08, dur=1.40, slow=2.4, w=1920, h=1080, off=120, grade='food'),   # stops before the baked-in fade to black
    # scene 5 — the white Oxford building, postcard strip (1920x720): wide -> side -> aerial
    'b_wide':    dict(start=41.07, dur=0.94, slow=2.4, w=1920, h=720, off=70, grade='ext_warm'),
    'b_side':    dict(start=14.04, dur=1.06, slow=2.0, w=1920, h=720, off=0, grade='ext',
                      scale=(2160, 1080, 0, 0)),                                                 # zoom pushes the wreath at the right edge out of frame
    'b_aerial':  dict(start=0.03,  dur=0.94, slow=2.2, w=1920, h=720, off=110, grade='ext_lift'),
}

def build(name):
    s = SHOTS[name]
    w, h, off = s['w'], s['h'], s['off']
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    if 'scale' in s:
        sw, sh, cx, cy = s['scale']
    elif w / h > 2:   # wider than the 2:1 source -> scale to width, crop height
        sw, sh, cx, cy = w, w // 2, 0, off
    else:             # scale to height, crop width
        sw, sh, cx, cy = 2 * h, h, off, 0
    grade = GRADE.get(s.get('grade', ''), '')
    vf = (f"setpts={s['slow']}*PTS,"
          "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
          f"scale={sw}:{sh}:flags=lanczos,crop={w}:{h}:{cx}:{cy},"
          + (grade + ',' if grade else '') + "unsharp=5:5:0.5")
    cmd = [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y',
           '-ss', f"{s['start']:.3f}", '-t', f"{s['dur']:.3f}", '-i', SRC,
           '-vf', vf, '-q:v', '2', os.path.join(d, 'f%04d.jpg')]
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
    manifest = {k: v for k, v in manifest.items() if k in SHOTS}
    open(mpath, 'w').write('window.CLIP_MANIFEST=' + json.dumps(manifest) + ';\n')
    print('wrote', mpath, manifest)
