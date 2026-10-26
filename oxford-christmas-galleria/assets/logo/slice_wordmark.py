"""Cut the client's wordmark out of wordmark-original-1200.jpg with transparency and slice it
into animatable pieces (OXFORD letters, the script, the tree, GALLERIA letters).

Writes: ocg-wordmark.png, slices/<piece>.png, slices/manifest.json, slices-preview.jpg
Run from this folder: python3 slice_wordmark.py   (needs pillow, numpy, scipy)
"""
import json, os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
src = np.asarray(Image.open(os.path.join(HERE, 'wordmark-original-1200.jpg')).convert('RGB')).astype(np.float32)
lum = 0.299*src[..., 0] + 0.587*src[..., 1] + 0.114*src[..., 2]
alpha = np.clip((245 - lum) / (245 - 150), 0, 1)                      # ink is opaque, white is clear
rgb = np.where(alpha[..., None] > 0.02,
               np.clip((src - (1 - alpha[..., None]) * 255) / np.maximum(alpha[..., None], 0.02), 0, 255), src)
rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
ys, xs = np.where(alpha > 0.5)
pad = 6
y0, y1 = max(0, ys.min() - pad), min(rgba.shape[0], ys.max() + 1 + pad)
x0, x1 = max(0, xs.min() - pad), min(rgba.shape[1], xs.max() + 1 + pad)
crop = rgba[y0:y1, x0:x1]
Image.fromarray(crop, 'RGBA').save(os.path.join(HERE, 'ocg-wordmark.png'))

mask = ndimage.binary_dilation(crop[..., 3] > 128, iterations=2)
lab, n = ndimage.label(mask)
comps = []
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    if int((lab[sl] == i).sum()) < 40:
        continue
    comps.append(dict(id=i, x=sl[1].start, y=sl[0].start, w=sl[1].stop - sl[1].start, h=sl[0].stop - sl[0].start,
                      cy=(sl[0].start + sl[0].stop) // 2, cx=(sl[1].start + sl[1].stop) // 2))
top = sorted([c for c in comps if c['cy'] < 80], key=lambda c: c['cx'])          # OXFORD
bot = sorted([c for c in comps if c['cy'] > 300], key=lambda c: c['cx'])         # GALLERIA
mid = [c for c in comps if 80 <= c['cy'] <= 300]
script = max(mid, key=lambda c: c['w']); tree = [c for c in mid if c is not script][0]
named = [(c, f'ox{k}') for k, c in enumerate(top)] + [(script, 'script'), (tree, 'tree')] + [(c, f'ga{k}') for k, c in enumerate(bot)]

out = os.path.join(HERE, 'slices'); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
manifest = []
for c, name in named:
    sl = (slice(c['y'], c['y'] + c['h']), slice(c['x'], c['x'] + c['w']))
    piece = crop[sl].copy(); piece[..., 3] = np.where(lab[sl] == c['id'], piece[..., 3], 0)
    Image.fromarray(piece, 'RGBA').save(os.path.join(out, f'{name}.png'))
    manifest.append(dict(name=name, x=int(c['x']), y=int(c['y']), w=int(c['w']), h=int(c['h'])))
json.dump(dict(width=int(crop.shape[1]), height=int(crop.shape[0]), pieces=manifest), open(os.path.join(out, 'manifest.json'), 'w'), indent=1)

bg = Image.new('RGBA', (crop.shape[1], crop.shape[0]), (245, 239, 228, 255))
for m in manifest:
    bg.alpha_composite(Image.open(os.path.join(out, f"{m['name']}.png")), (m['x'], m['y']))
bg.convert('RGB').save(os.path.join(HERE, 'slices-preview.jpg'), quality=92)
print(f"{len(manifest)} pieces -> {out}")
