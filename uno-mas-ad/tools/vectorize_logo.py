# Vectorizes assets/logo.png into per-glyph SVG paths (assets/logo_glyphs.json).
# Run from uno-mas-ad/: pip install potracer pillow numpy && python3 tools/vectorize_logo.py
# Then regenerate the JS wrapper: (printf "window.LOGO_GLYPHS="; cat assets/logo_glyphs.json; printf ";\n") > assets/logo_glyphs.js
import numpy as np, potrace, json
from PIL import Image
im = Image.open('assets/logo.png').convert('RGBA')
S = 8
al = im.split()[3].resize((im.width*S, im.height*S), Image.BICUBIC)
bm = ~(np.array(al) > 128)
path = potrace.Bitmap(bm).trace(turdsize=4, alphamax=1.0, opttolerance=0.2)
curves = []
for curve in path:
    d = []; pts = []
    sp = curve.start_point
    d.append(f"M{sp.x/S:.2f},{sp.y/S:.2f}"); pts.append((sp.x/S, sp.y/S))
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f"L{seg.c.x/S:.2f},{seg.c.y/S:.2f}L{seg.end_point.x/S:.2f},{seg.end_point.y/S:.2f}")
            pts += [(seg.c.x/S, seg.c.y/S), (seg.end_point.x/S, seg.end_point.y/S)]
        else:
            d.append(f"C{seg.c1.x/S:.2f},{seg.c1.y/S:.2f} {seg.c2.x/S:.2f},{seg.c2.y/S:.2f} {seg.end_point.x/S:.2f},{seg.end_point.y/S:.2f}")
            pts += [(seg.c1.x/S, seg.c1.y/S), (seg.c2.x/S, seg.c2.y/S), (seg.end_point.x/S, seg.end_point.y/S)]
    d.append('Z')
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    curves.append({'d':''.join(d), 'bbox':[min(xs),min(ys),max(xs),max(ys)]})
# group: a curve contained in another curve's bbox is a hole -> same glyph
def contains(a,b):  # a contains b
    return a[0]<=b[0]+0.5 and a[1]<=b[1]+0.5 and a[2]>=b[2]-0.5 and a[3]>=b[3]-0.5
roots = []
for i,c in enumerate(curves):
    parent = None
    for j,o in enumerate(curves):
        if i!=j and contains(o['bbox'], c['bbox']):
            area_o=(o['bbox'][2]-o['bbox'][0])*(o['bbox'][3]-o['bbox'][1])
            if parent is None or area_o < parent[1]:
                parent=(j,area_o)
    c['parent'] = parent[0] if parent else None
glyphs = {}
def root_of(i):
    while curves[i]['parent'] is not None: i = curves[i]['parent']
    return i
for i,c in enumerate(curves):
    r = root_of(i)
    glyphs.setdefault(r, []).append(i)
out = []
for r, members in glyphs.items():
    bb = curves[r]['bbox']
    out.append({'d':' '.join(curves[m]['d'] for m in members), 'bbox':[round(v,2) for v in bb],
                'cx': round((bb[0]+bb[2])/2,2), 'cy': round((bb[1]+bb[3])/2,2)})
out.sort(key=lambda g:(g['bbox'][1]>118, g['cx']))
for g in out: print(g['bbox'], 'w',round(g['bbox'][2]-g['bbox'][0],1),'h',round(g['bbox'][3]-g['bbox'][1],1))
json.dump({'w':im.width,'h':im.height,'glyphs':out}, open('assets/logo_glyphs.json','w'))
print('glyphs', len(out))
