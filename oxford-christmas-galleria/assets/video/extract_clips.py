"""Cut the two 4.5-second footage slots out of last year's reel into JPEG frame folders.

reel-2025.mp4 is the Oxford Christmas Galleria reel (720x1280, 30 fps, 18.6 s).
Each clip is a list of (start, duration) segments joined in order; 4.5 s = 135 frames.
Run from anywhere: python3 assets/video/extract_clips.py
"""
import os, shutil, subprocess, glob
import imageio_ffmpeg
HERE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
SRC = os.path.join(HERE, 'reel-2025.mp4')
FPS = 30
CLIPS = {
    # free admission / free parking beat: shoppers at the booths, artist waving, ornament close-up
    'clipA': [(2.0, 4.5)],
    # tote-bag beat: the embroidered tote first, then Santa with the kids, then the ribbon wall
    'clipB': [(17.0, 1.6), (15.0, 1.5), (11.0, 1.4)],
}
for name, segs in CLIPS.items():
    out = os.path.join(HERE, name); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    n = 0
    for i, (start, dur) in enumerate(segs):
        tmp = os.path.join(HERE, f'_{name}_{i}'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(start), '-t', str(dur), '-i', SRC,
                        '-vf', f'fps={FPS}', '-q:v', '3', os.path.join(tmp, 'f%04d.jpg')], check=True)
        for f in sorted(glob.glob(os.path.join(tmp, 'f*.jpg'))):
            n += 1; shutil.move(f, os.path.join(out, f'f{n:04d}.jpg'))
        shutil.rmtree(tmp)
    print(f'{name}: {n} frames from {segs}')
