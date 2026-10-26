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
# Segment edges sit exactly on the reel's own shot changes (found by frame differencing):
#   2.00 3.13 4.30 5.07 6.30 7.63 8.60 9.60 10.97 12.17 12.90 15.20 16.37 17.17 18.60
CLIPS = {
    # free admission / free parking beat: shoppers at the tent, artist waving, ornament close-up, Santa waving
    'clipA': [(3.13, 4.50)],
    # tote-bag beat: the embroidered tote first, then Santa with the kids, the ribbon wall, a nutcracker tail
    'clipB': [(17.17, 1.43), (15.20, 1.13), (10.97, 1.16), (16.37, 0.77)],
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
