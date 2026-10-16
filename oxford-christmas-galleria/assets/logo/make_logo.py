"""Rebuild the Oxford Christmas Galleria wreath logo as vector SVG.

Every leaf, berry and dot is its own element with data attributes so the ad
can animate them one by one. Deterministic (seeded) so re-runs are identical.
"""
import math, random, os
random.seed(20261128)

W = H = 1000
CX = CY = 500
R = 330                      # wreath ring radius
SAGE, DEEP, LIGHT, DARK = '#A9B894', '#5E8A6A', '#C3CDAE', '#4F7B5C'
CORAL, BERRY = '#E5705A', '#C8463E'

def leaf_path(L, w):
    """Pointed leaf from (0,0) to (L,0), width w."""
    return (f"M0,0 C{L*0.25:.1f},{-w*0.55:.1f} {L*0.75:.1f},{-w*0.55:.1f} {L:.1f},0 "
            f"C{L*0.75:.1f},{w*0.55:.1f} {L*0.25:.1f},{w*0.55:.1f} 0,0 Z")

els = []
idx = 0
N_SPRIGS = 18
for s in range(N_SPRIGS):
    a = 2*math.pi*s/N_SPRIGS + random.uniform(-0.05, 0.05)
    # sprig base point on the ring, slight radial jitter
    r0 = R + random.uniform(-18, 18)
    bx, by = CX + r0*math.cos(a), CY + r0*math.sin(a)
    # stem runs along the tangent (counter-clockwise visually)
    tang = a + math.pi/2
    stem_len = random.uniform(95, 125)
    n_leaves = random.choice([5, 6, 7])
    main, alt = (SAGE, DEEP) if s % 2 == 0 else (DEEP, SAGE)
    if s % 5 == 0: main = LIGHT
    if s % 7 == 3: alt = DARK
    # stem
    ex, ey = bx + stem_len*math.cos(tang), by + stem_len*math.sin(tang)
    # gentle curve: control point bent slightly toward the centre
    mx, my = (bx+ex)/2, (by+ey)/2
    cx_, cy_ = mx + 14*math.cos(a+math.pi), my + 14*math.sin(a+math.pi)
    els.append(f'<path class="stem" data-sprig="{s}" d="M{bx:.1f},{by:.1f} Q{cx_:.1f},{cy_:.1f} {ex:.1f},{ey:.1f}" '
               f'fill="none" stroke="{DARK}" stroke-width="3.2" stroke-linecap="round"/>')
    for k in range(n_leaves):
        f = (k+0.6)/n_leaves
        px = bx + stem_len*f*math.cos(tang) + 7*f*math.cos(a+math.pi)
        py = by + stem_len*f*math.sin(tang) + 7*f*math.sin(a+math.pi)
        side = 1 if k % 2 == 0 else -1
        L = random.uniform(44, 62) * (1 - 0.35*f)       # leaves shrink toward the tip
        w = random.uniform(15, 21) * (1 - 0.25*f)
        rot = math.degrees(tang) + side*random.uniform(38, 55)
        col = main if k % 2 == 0 else alt
        els.append(f'<path class="leaf" data-i="{idx}" data-sprig="{s}" data-k="{k}" '
                   f'transform="translate({px:.1f},{py:.1f}) rotate({rot:.1f})" d="{leaf_path(L, w)}" fill="{col}"/>')
        idx += 1
    # tip leaf
    els.append(f'<path class="leaf" data-i="{idx}" data-sprig="{s}" data-k="{n_leaves}" '
               f'transform="translate({ex:.1f},{ey:.1f}) rotate({math.degrees(tang):.1f})" d="{leaf_path(34, 12)}" fill="{alt}"/>')
    idx += 1

# berry clusters
b = 0
for c in range(7):
    a = 2*math.pi*(c+0.5)/7 + random.uniform(-0.15, 0.15)
    r0 = R + random.uniform(-30, 30)
    bx, by = CX + r0*math.cos(a), CY + r0*math.sin(a)
    for k, (dx, dy, rr) in enumerate([(0, 0, 8.5), (14, -9, 7), (-4, 15, 6.5)]):
        col = CORAL if (c+k) % 2 == 0 else BERRY
        els.append(f'<circle class="berry" data-i="{b}" cx="{bx+dx:.1f}" cy="{by+dy:.1f}" r="{rr}" fill="{col}"/>')
        b += 1
# little dots
d = 0
for k in range(26):
    a = random.uniform(0, 2*math.pi)
    r0 = R + random.uniform(-70, 70)
    els.append(f'<circle class="dot" data-i="{d}" cx="{CX+r0*math.cos(a):.1f}" cy="{CY+r0*math.sin(a):.1f}" r="{random.uniform(2.6,3.6):.1f}" fill="{CORAL}"/>')
    d += 1

wreath = '\n'.join(els)
FONT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts'))
text = f'''
<text class="word-oxford" x="500" y="482" text-anchor="middle" font-family="Pacifico" font-size="132" fill="{CORAL}">Oxford</text>
<text class="word-cg" x="500" y="576" text-anchor="middle" font-family="Bree Serif" font-size="60" fill="{CORAL}" letter-spacing="1">Christmas Galleria</text>
'''
svg_inner = f'<g class="wreath">\n{wreath}\n</g>\n<g class="wordmark">{text}</g>'
standalone = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
@font-face{{font-family:'Pacifico';src:url('file://{FONT_DIR}/Pacifico-400.ttf');}}
@font-face{{font-family:'Bree Serif';src:url('file://{FONT_DIR}/BreeSerif-400.ttf');}}
</style>
<rect width="{W}" height="{H}" fill="#F5EFE4"/>
{svg_inner}
</svg>'''
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, 'logo.svg'), 'w').write(standalone)
# inner markup for inlining into the ad / one-pager (no fonts, no background)
open(os.path.join(here, 'logo-inner.svg.fragment'), 'w').write(svg_inner)
print('leaves', idx, 'berries', b, 'dots', d)
