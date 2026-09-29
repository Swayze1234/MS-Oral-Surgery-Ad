"""Turns the supplied 500x500 logo JPEG (assets/source/tom-smith-logo.jpg) into
transparent, high-resolution layers so the intro can build the logo piece by
piece:

    roof, tom, smith, trees, landand, homes, tagline

The green circle around the logo is removed and the white background is made
transparent.  Pixels keep their original colours (upscaled 4x, Lanczos); the
flat-colour classification is only used to decide which layer a piece belongs
to.

Output: assets/img/logo/<layer>.png, logo.png (composite), layers.js (geometry).

    pip install pillow numpy scipy
    python3 prepare_logo.py
"""
import os, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "assets", "source", "tom-smith-logo.jpg")
OUT  = os.path.join(BASE, "assets", "img", "logo")
DBG  = os.environ.get("LOGO_DEBUG")          # optional path for a tinted debug sheet
os.makedirs(OUT, exist_ok=True)

SCALE = 4
WHITE = np.array((252, 253, 252), np.float32)
INKS  = {"green": (122, 153, 61), "blue": (10, 84, 138), "dark": (20, 20, 20)}   # sampled from the file

src = Image.open(SRC).convert("RGB")
W0, H0 = src.size
big = src.resize((W0 * SCALE, H0 * SCALE), Image.LANCZOS)
big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
px  = np.asarray(big).astype(np.float32)
H, W = px.shape[:2]

# ink class by hue/saturation (robust to JPEG halos), then "how far from
# white" relative to that ink (0 = white, 1 = full ink)
r, g, b = px[..., 0], px[..., 1], px[..., 2]
mean = (r + g + b) / 3
is_dark  = (mean < 45) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 40)
is_blue  = ~is_dark & (b > g + 8)
is_green = ~is_dark & ~is_blue & ((g - np.minimum(r, b)) > 25)
cls = np.zeros(mean.shape, np.int8); cls[is_green] = 1; cls[is_blue] = 2; cls[is_dark] = 3
span = np.array([400.0] + [np.linalg.norm(np.array(c, np.float32) - WHITE) for c in INKS.values()])[cls]
d_white = np.linalg.norm(px - WHITE, axis=2)
nw = np.clip(d_white / span, 0, 1)

alpha = np.clip((nw - 0.22) / 0.40, 0, 1)            # soft edge, faint JPEG halos removed
colored = nw > 0.5                                    # hard mask for labelling
masks = {"green": colored & is_green, "blue": colored & is_blue, "dark": colored & is_dark}

def s(v): return v * SCALE           # 500-px coords -> working coords
cx, cy = W / 2, H / 2

def components(mask, split=0):
    """Connected components. With split>0 the mask is eroded first so thin
    bridges break, then every original pixel is handed to its nearest core."""
    if split:
        core = ndi.binary_erosion(mask, iterations=split)
        lab, _ = ndi.label(core)
        _, (iy, ix) = ndi.distance_transform_edt(lab == 0, return_indices=True)
        lab = lab[iy, ix] * mask
    else:
        lab, _ = ndi.label(mask)
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl is None: continue
        m = lab[sl] == i
        ys, xs = np.nonzero(m)
        out.append(dict(id=i, area=int(m.sum()), top=sl[0].start, bottom=sl[0].stop,
                        left=sl[1].start, right=sl[1].stop,
                        cx=sl[1].start + xs.mean(), cy=sl[0].start + ys.mean()))
    return lab, out

layers = {k: np.zeros((H, W), bool) for k in ("roof", "tom", "smith", "trees", "landand", "homes", "tagline")}
MIN = s(1) ** 2 * 2                      # ignore JPEG speckle

# ---- green: ring (dropped), trees, Smith --------------------------------
# The white keyline between the letters and the trees is sub-pixel in the
# 500 px source, so they cannot be separated by connectivity.  Instead the
# green artwork is cut at the letters' cap line: above it is "trees", below it
# is "smith" (which therefore also carries the bottoms of the trunks).
CAP = s(250.5)
lab, comps = components(masks["green"])
for c in comps:
    r = np.hypot(c["cx"] - cx, c["cy"] - cy)
    if c["area"] < MIN or r > s(205) or (c["right"] - c["left"]) > s(300):
        continue                                     # the circle, and speckle
    m = lab == c["id"]
    rows = np.arange(H)[:, None]
    layers["trees"] |= m & (rows < CAP)
    layers["smith"] |= m & (rows >= CAP)

# ---- blue: roof, Tom, LAND AND, HOMES -----------------------------------
lab, comps = components(masks["blue"])
for c in comps:
    if c["area"] < MIN: continue
    if c["top"] < s(190):      key = "roof"
    elif c["top"] < s(262):    key = "tom"
    elif c["top"] < s(335.5):  key = "landand"
    else:                      key = "homes"
    layers[key][lab == c["id"]] = True

# ---- dark: tagline ---------------------------------------------------------
lab, comps = components(masks["dark"])
for c in comps:
    if c["area"] < MIN // 2: continue
    if c["top"] > s(370): layers["tagline"][lab == c["id"]] = True

# each layer takes its own pixels plus a small margin (the anti-aliased edge),
# but never pixels that belong to another layer
regions = {}
for k, m in layers.items():
    others = np.zeros((H, W), bool)
    for k2, m2 in layers.items():
        if k2 != k: others |= m2
    regions[k] = ndi.binary_dilation(m, iterations=4) & ~others

union = np.zeros((H, W), bool)
for m in regions.values(): union |= m
ys, xs = np.nonzero(union & (alpha > 0))
PAD = 4
X0, X1 = max(0, xs.min() - PAD), min(W, xs.max() + PAD + 1)
Y0, Y1 = max(0, ys.min() - PAD), min(H, ys.max() + PAD + 1)
CW, CH = int(X1 - X0), int(Y1 - Y0)

geom = {"canvas": [CW, CH], "layers": {}}
composite = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
dbg = Image.new("RGB", (CW, CH), "white") if DBG else None
tints = dict(roof=(220, 40, 40), tom=(40, 120, 220), smith=(40, 170, 60), trees=(160, 60, 200),
             landand=(230, 140, 20), homes=(20, 170, 170), tagline=(0, 0, 0))
for name, reg in regions.items():
    a = (alpha * reg)[Y0:Y1, X0:X1]
    ys, xs = np.nonzero(a > 0.02)
    if len(xs) == 0:
        raise SystemExit(f"layer {name} is empty - check the thresholds")
    lx0, lx1, ly0, ly1 = int(xs.min()), int(xs.max() + 1), int(ys.min()), int(ys.max() + 1)
    rgba = np.zeros((ly1 - ly0, lx1 - lx0, 4), np.uint8)
    rgba[..., :3] = np.clip(px[Y0 + ly0:Y0 + ly1, X0 + lx0:X0 + lx1], 0, 255).astype(np.uint8)
    rgba[..., 3] = (a[ly0:ly1, lx0:lx1] * 255).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    img.save(os.path.join(OUT, f"{name}.png"))
    composite.alpha_composite(img, (lx0, ly0))
    if dbg is not None:
        dbg.paste(Image.new("RGB", img.size, tints[name]), (lx0, ly0), img.split()[3])
    geom["layers"][name] = {"x": lx0, "y": ly0, "w": lx1 - lx0, "h": ly1 - ly0}
    print(f"{name:8s} {lx1-lx0:5d}x{ly1-ly0:<5d} at ({lx0},{ly0})")

composite.save(os.path.join(OUT, "logo.png"))
with open(os.path.join(OUT, "layers.js"), "w") as f:
    f.write("window.LOGO_LAYERS = " + json.dumps(geom) + ";\n")
if dbg is not None: dbg.save(DBG)
print("canvas", CW, "x", CH)
