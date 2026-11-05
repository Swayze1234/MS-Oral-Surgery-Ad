"""Builds a 15-second 1080p Happy Birthday ad for Michael Joe.
Run: python3 make_ad.py  -> happy_birthday_michael_joe.mp4
"""
import math, random, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1920, 1080, 30, 15
N = FPS * DUR
FRAMES = os.path.join(HERE, "_frames")
os.makedirs(FRAMES, exist_ok=True)

NAVY, GOLD, PINK, WHITE = (10, 22, 60), (245, 196, 66), (236, 64, 122), (255, 255, 255)
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_SCRIPT = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
if not os.path.exists(FONT_BLACK):
    FONT_BLACK = FONT_BOLD

def font(path, size):
    return ImageFont.truetype(path, size)

photo = Image.open(os.path.join(HERE, "michael_joe.jpg")).convert("RGB")

# ---------- helpers ----------
def ease(t):  # ease-out cubic, clamped
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def back(t):  # overshoot "pop"
    t = max(0.0, min(1.0, t))
    c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def text_layer(txt, fnt, fill, scale=1.0, alpha=1.0, shadow=True, stroke=0, stroke_fill=None):
    """Render text to an RGBA image (with soft shadow), scaled & faded."""
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = d.textbbox((0, 0), txt, font=fnt, stroke_width=stroke)
    pad = 40
    img = Image.new("RGBA", (r - l + pad * 2, b - t + pad * 2), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + 6, pad - t + 8), txt, font=fnt, fill=(0, 0, 0, 170),
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(img).text((pad - l, pad - t), txt, font=fnt, fill=fill,
                             stroke_width=stroke, stroke_fill=stroke_fill)
    if scale != 1.0 and scale > 0.01:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
    if alpha < 1.0:
        a = img.getchannel("A").point(lambda v: int(v * max(0, alpha)))
        img.putalpha(a)
    return img

def paste_center(base, layer, cx, cy):
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def cover(img, w, h, zoom=1.0, fx=0.5, fy=0.5):
    """Crop/scale img to fill w x h, with zoom around focus point."""
    s = max(w / img.width, h / img.height) * zoom
    rw, rh = img.width * s, img.height * s
    x0 = min(max(fx * rw - w / 2, 0), rw - w)
    y0 = min(max(fy * rh - h / 2, 0), rh - h)
    return img.resize((int(rw), int(rh)), Image.LANCZOS).crop((int(x0), int(y0), int(x0) + w, int(y0) + h))

def gradient(w, h, top, bottom):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / (h - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))
    return g.resize((w, h)).convert("RGBA")

# ---------- confetti ----------
random.seed(7)
COLORS = [GOLD, PINK, (80, 200, 255), (130, 230, 120), WHITE, (180, 120, 255)]
confetti = [dict(x=random.uniform(0, W), y=random.uniform(-H, 0), vy=random.uniform(140, 320),
                 sway=random.uniform(20, 70), ph=random.uniform(0, 6.28), spin=random.uniform(2, 7),
                 w=random.randint(10, 20), h=random.randint(18, 34), c=random.choice(COLORS))
            for _ in range(160)]

def draw_confetti(base, t, start, density=1.0):
    if t < start:
        return
    lt = t - start
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, p in enumerate(confetti):
        if i > len(confetti) * density:
            break
        y = (p["y"] + p["vy"] * lt) % (H + 200) - 100
        x = p["x"] + math.sin(p["ph"] + lt * 2) * p["sway"]
        a = p["ph"] + lt * p["spin"]
        hw, hh = p["w"] / 2, p["h"] / 2 * abs(math.cos(a))  # flip effect
        ca, sa = math.cos(a * 0.6), math.sin(a * 0.6)
        pts = [(x + dx * ca - dy * sa, y + dx * sa + dy * ca) for dx, dy in
               [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]]
        d.polygon(pts, fill=p["c"] + (235,))
    base.alpha_composite(layer)

# ---------- balloons ----------
def balloon(d, x, y, r, col):
    d.line([(x, y + r * 1.2), (x + 10, y + r * 1.2 + 120), (x - 6, y + r * 1.2 + 240)], fill=(255, 255, 255, 160), width=3)
    d.ellipse([x - r, y - r * 1.2, x + r, y + r * 1.2], fill=col + (255,))
    d.polygon([(x - 12, y + r * 1.2 + 14), (x + 12, y + r * 1.2 + 14), (x, y + r * 1.2 - 4)], fill=col + (255,))
    d.ellipse([x - r * 0.55, y - r * 0.85, x - r * 0.2, y - r * 0.35], fill=(255, 255, 255, 110))

# ---------- pre-built assets ----------
bg_navy = gradient(W, H, (18, 34, 90), (6, 12, 36))
bottom_fade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bfd = ImageDraw.Draw(bottom_fade)
for y in range(H):
    k = max(0, (y - H * 0.45) / (H * 0.55))
    bfd.line([(0, y), (W, y)], fill=(5, 10, 30, int(225 * k ** 1.3)))

# circular portrait for scenes 2 & 3
def circle_portrait(size):
    face = cover(photo, size, size, zoom=1.0, fx=0.535, fy=0.45)
    # zoom into head/torso area
    s = photo.height / 552
    box = (int(250 * s), int(80 * s), int(560 * s), int(390 * s))
    face = photo.crop(box).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([0, 0, size + 39, size + 39], fill=GOLD + (255,))
    face_rgba = face.convert("RGBA")
    face_rgba.putalpha(mask)
    out.alpha_composite(face_rgba, (20, 20))
    return out

portrait_big = circle_portrait(620)

F_HB = font(FONT_BLACK, 150)
F_NAME = font(FONT_SCRIPT, 170)
F_SUB = font(FONT_BOLD, 56)
F_SMALL = font(FONT_BOLD, 44)

# ---------- scenes ----------
def scene1(t):  # 0-5s: full photo, Ken Burns, title pops in
    zoom = 1.0 + 0.10 * (t / 5)
    img = cover(photo, W, H, zoom=zoom, fx=0.53, fy=0.42).convert("RGBA")
    img.alpha_composite(bottom_fade)
    a = ease((t - 0.4) / 0.6)
    paste_center(img, text_layer("HAPPY BIRTHDAY", F_HB, GOLD, scale=0.6 + 0.4 * back((t - 0.4) / 0.7), alpha=a), W / 2, 790)
    b = ease((t - 1.4) / 0.8)
    paste_center(img, text_layer("Michael Joe", F_NAME, WHITE, alpha=b), W / 2, 950 + 40 * (1 - b))
    draw_confetti(img, t, 0.4, density=0.6)
    return img

def scene2(t):  # 5-10s: portrait left, message right
    lt = t - 5
    img = bg_navy.copy()
    d = ImageDraw.Draw(img)
    # soft glow behind portrait
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([170, 160, 930, 920], fill=GOLD + (90,))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    s = 0.85 + 0.15 * back(lt / 0.8)
    p = portrait_big.resize((int(portrait_big.width * s), int(portrait_big.height * s)), Image.LANCZOS)
    paste_center(img, p, 550, 540)
    lines = [("Cheers to", F_SUB, WHITE, 0.4, 300),
             ("Michael Joe!", font(FONT_SCRIPT, 140), GOLD, 0.9, 420),
             ("Wishing you a year full of", F_SUB, WHITE, 1.6, 590),
             ("joy, laughter & great", F_SUB, WHITE, 1.9, 665),
             ("times on the road ahead!", F_SUB, WHITE, 2.2, 740)]
    for txt, f, col, st, y in lines:
        a = ease((lt - st) / 0.6)
        lay = text_layer(txt, f, col, alpha=a)
        img.alpha_composite(lay, (int(1010 + 80 * (1 - a)), int(y - lay.height / 2)))
    # gold underline
    u = ease((lt - 1.2) / 0.7)
    d.rounded_rectangle([1050, 505, 1050 + int(640 * u), 515], radius=5, fill=GOLD)
    draw_confetti(img, t, 5, density=0.35)
    return img

def scene3(t):  # 10-15s: celebration end card
    lt = t - 10
    img = gradient(W, H, (120, 20, 70), (20, 12, 60))
    bl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bl)
    rise = (1 - ease(lt / 1.6)) * 700
    for x, y, r, c in [(170, 300, 95, GOLD), (360, 230, 80, (80, 200, 255)), (1580, 260, 90, PINK),
                       (1760, 340, 80, GOLD), (250, 520, 70, (180, 120, 255)), (1700, 560, 70, (130, 230, 120))]:
        balloon(bd, x, y + rise + 12 * math.sin(lt * 2 + x), r, c)
    img.alpha_composite(bl)
    pr = portrait_big.resize((300, 300), Image.LANCZOS)
    pa = ease(lt / 0.6)
    pr.putalpha(pr.getchannel("A").point(lambda v: int(v * pa)))
    paste_center(img, pr, W / 2, 230)
    paste_center(img, text_layer("HAPPY BIRTHDAY", F_HB, WHITE, scale=0.5 + 0.5 * back((lt - 0.3) / 0.7),
                                 alpha=ease((lt - 0.3) / 0.5), stroke=4, stroke_fill=PINK), W / 2, 520)
    paste_center(img, text_layer("Michael Joe", font(FONT_SCRIPT, 180), GOLD, alpha=ease((lt - 1.0) / 0.7)), W / 2, 700)
    paste_center(img, text_layer("Here's to another great year!", F_SMALL, WHITE, alpha=ease((lt - 1.8) / 0.7)), W / 2, 860)
    draw_confetti(img, t, 10, density=1.0)
    return img

def crossfade(a, b, k):
    return Image.blend(a, b, k)

# ---------- render ----------
for i in range(N):
    t = i / FPS
    if t < 4.6:
        f = scene1(t)
    elif t < 5.2:
        f = crossfade(scene1(t), scene2(t), (t - 4.6) / 0.6)
    elif t < 9.6:
        f = scene2(t)
    elif t < 10.2:
        f = crossfade(scene2(t), scene3(t), (t - 9.6) / 0.6)
    else:
        f = scene3(t)
    # fade in / fade out
    k = min(1.0, t / 0.4, (DUR - t) / 0.6)
    if k < 1.0:
        f = Image.blend(Image.new("RGBA", f.size, (0, 0, 0, 255)), f, max(0, k))
    f.convert("RGB").save(os.path.join(FRAMES, f"f{i:04d}.png"), compress_level=1)
    if i % 60 == 0:
        print("frame", i)

out = os.path.join(HERE, "happy_birthday_michael_joe.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%04d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                "-an", "-movflags", "+faststart", out], check=True)
print("done ->", out)
