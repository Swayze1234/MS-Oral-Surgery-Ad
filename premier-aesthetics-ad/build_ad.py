"""Build the refreshed Premier Aesthetics :30 spot (1920x1080, 29.97 fps).

Timeline
  0.0 - 2.6s  original PA logo intro, cross-dissolves into...
  2.6 - 10s   NEW team group photo, full-bleed with slow push-in + welcome copy
  10  - 20s   microneedling footage + "Summer Skin Prep" panel
  20  - 27s   injectables footage + "Premier Perks" panel
  27  - 30s   end card: logo, tagline, phone, socials

Usage:  cd premier-aesthetics-ad && python3 build_ad.py
Needs:  pillow, numpy, ffmpeg on PATH (pip install imageio-ffmpeg works too).
"""
import os
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "MCTV_PremierAesthetics_FS_2026.mp4")

W, H = 1920, 1080
FPS = "30000/1001"
TOTAL = 900  # 30.03s

GOLD = (165, 121, 75)
GOLD_DK = (143, 105, 64)
INK = (38, 30, 26)
CREAM = (250, 247, 243)
WHITE = (255, 255, 255)

# Frame ranges (output frame numbers)
GROUP = (60, 312)       # group photo scene (fades in 60..78)
SKIN = (296, 596)       # microneedling scene (fades in 296..312)
PERKS = (580, 818)      # injectables scene (fades in 580..596)
END = (800, 900)        # end card (fades in 800..818)
FADE = 18


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_EYEBROW = font("Montserrat-SemiBold.ttf", 28)
F_BODY = font("Montserrat-Regular.ttf", 34)
F_ITEM = font("Montserrat-SemiBold.ttf", 46)
F_PHONE = font("Montserrat-Bold.ttf", 46)
F_HEAD = font("Playfair-SemiBold.ttf", 86)
F_HEAD_IT = font("Playfair-Italic.ttf", 86)
F_TEAM_HEAD = font("Playfair-SemiBold.ttf", 92)
F_TEAM_SUB = font("Playfair-Italic.ttf", 42)
F_END = font("Playfair-Italic.ttf", 70)


# ---------------------------------------------------------------- helpers
def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def spaced_text(draw, xy, text, fnt, fill, spacing=0, anchor_right=False):
    x, y = xy
    if anchor_right:
        x -= sum(fnt.getlength(c) + spacing for c in text) - spacing
    for c in text:
        draw.text((x, y), c, font=fnt, fill=fill)
        x += fnt.getlength(c) + spacing
    return x


def text_el(text, fnt, fill, xy, spacing=0, shadow=False):
    """A full-frame RGBA layer holding one piece of text."""
    im = layer()
    d = ImageDraw.Draw(im)
    if shadow:
        sh = layer()
        spaced_text(ImageDraw.Draw(sh), (xy[0] + 2, xy[1] + 4), text, fnt, (0, 0, 0, 170), spacing)
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6)))
        d = ImageDraw.Draw(im)
    spaced_text(d, xy, text, fnt, fill, spacing)
    return im


def shape_el(fn):
    im = layer()
    fn(ImageDraw.Draw(im), im)
    return im


def masked_crop(img, box, shape, radius=None, ss=4):
    """Crop box from img and cut it out as an ellipse or stadium."""
    c = img.crop(box).convert("RGBA")
    w, h = c.size
    m = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(m)
    if shape == "ellipse":
        d.ellipse((0, 0, w * ss - 1, h * ss - 1), fill=255)
    else:
        d.rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), radius=radius * ss, fill=255)
    c.putalpha(m.resize((w, h), Image.LANCZOS))
    return c


def fit_h(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


# ---------------------------------------------------------------- brand assets
brand_logo = Image.open(os.path.join(SRC, "brand_frame_logo.png")).convert("RGB")
brand_icons = Image.open(os.path.join(SRC, "brand_frame_icons.png")).convert("RGB")

LOGO = masked_crop(brand_logo, (717, 166, 1204, 912), "stadium", radius=243)
FB = masked_crop(brand_icons, (1658, 966, 1728, 1036), "ellipse")
IG = masked_crop(brand_icons, (1757, 966, 1827, 1036), "ellipse")
PHONE_ICON = masked_crop(brand_icons, (1283, 858, 1341, 916), "ellipse")

# Soft silk texture (right side of the intro frame, mirrored) for the panels
_silk = brand_logo.crop((1220, 0, 1920, 1080))
SILK = Image.new("RGB", (1400, 1080))
SILK.paste(_silk, (0, 0))
SILK.paste(_silk.transpose(Image.FLIP_LEFT_RIGHT), (700, 0))
SILK = SILK.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
SILK = Image.blend(SILK, Image.new("RGB", (W, H), CREAM), 0.35)


def phone_pill(cx=None, x=None, y=0, scale=1.0):
    """Gold pill with phone icon + number. Returns an RGBA layer."""
    fnt = F_PHONE if scale == 1.0 else font("Montserrat-Bold.ttf", round(46 * scale))
    num = "(662) 871-4677"
    icon = fit_h(PHONE_ICON, round(58 * scale))
    pad = round(26 * scale)
    tw = fnt.getlength(num)
    pw = round(pad + icon.width + 18 * scale + tw + pad * 1.3)
    ph = round(88 * scale)
    if cx is not None:
        x = round(cx - pw / 2)
    im = layer()
    # soft shadow
    sh = layer()
    ImageDraw.Draw(sh).rounded_rectangle((x, y + 8, x + pw, y + ph + 8), radius=ph // 2, fill=(60, 40, 20, 90))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + pw, y + ph), radius=ph // 2, fill=GOLD + (255,))
    im.alpha_composite(icon, (x + pad, y + (ph - icon.height) // 2))
    bb = fnt.getbbox(num)
    d.text((x + pad + icon.width + 18 * scale, y + (ph - (bb[3] - bb[1])) / 2 - bb[1]), num, font=fnt, fill=WHITE)
    return im, (x, y, pw, ph)


def socials(x, y, size=62, gap=18):
    im = layer()
    im.alpha_composite(fit_h(FB, size), (x, y))
    im.alpha_composite(fit_h(IG, size), (x + size + gap, y))
    return im


# ---------------------------------------------------------------- scene layers
class El:
    """An animated overlay: fades + slides up starting at frame `start`."""

    def __init__(self, img, start, dur=16, dy=28, dx=0):
        self.img, self.start, self.dur, self.dy, self.dx = img, start, dur, dy, dx
        self.bbox = img.getbbox()

    def draw(self, base, f):
        t = ease((f - self.start) / self.dur)
        if t <= 0 or not self.bbox:
            return
        piece = self.img.crop(self.bbox)
        if t < 1:
            a = np.asarray(piece).copy()
            a[..., 3] = (a[..., 3] * t).astype(np.uint8)
            piece = Image.fromarray(a)
        ox = self.bbox[0] + round(self.dx * (1 - t))
        oy = self.bbox[1] + round(self.dy * (1 - t))
        base.alpha_composite(piece, (ox, oy))


def draw_diamond(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


# --- Scene 2: team photo
team = Image.open(os.path.join(SRC, "team_group_photo_2026.jpg")).convert("RGB")
_g = np.zeros((H, W, 4), np.uint8)
_rows = np.clip((np.arange(H) - 560) / 440, 0, 1) ** 1.4
_g[..., 0], _g[..., 1], _g[..., 2] = 26, 18, 12
_g[..., 3] = (_rows[:, None] * 238).astype(np.uint8)
team_grad = Image.fromarray(_g)
# a whisper of vignette on the top edge too
_top = np.zeros((H, W, 4), np.uint8)
_top[..., 3] = (np.clip((140 - np.arange(H)) / 140, 0, 1)[:, None] * 70).astype(np.uint8)
team_grad = Image.alpha_composite(team_grad, Image.fromarray(_top))

g0 = GROUP[0] + FADE
team_els = [
    El(shape_el(lambda d, im: d.rectangle((110, 772, 190, 776), fill=GOLD + (255,))), g0 + 8, dx=-40, dy=0),
    El(text_el("MEET OUR TEAM", F_EYEBROW, (226, 196, 158), (110, 730), spacing=7), g0 + 4),
    El(text_el("Welcome to Premier Aesthetics", F_TEAM_HEAD, WHITE, (104, 790), shadow=True), g0 + 12),
    El(text_el("Where the art of enhancing your natural beauty takes center stage.",
               F_TEAM_SUB, (240, 228, 214), (110, 918), shadow=True), g0 + 24),
]
_, _pb = phone_pill(x=0, y=0)  # measure width first
_pill, _pb = phone_pill(x=W - 110 - _pb[2], y=60)
team_els.append(El(_pill, g0 + 34, dy=-20))
_team_logo = layer()
_team_logo.alpha_composite(fit_h(LOGO, 150), (110, 50))
team_els.insert(0, El(_team_logo, g0, dy=-20))


def team_frame(f):
    t = (f - GROUP[0]) / (GROUP[1] - GROUP[0])
    s = 1.0 + 0.07 * t
    # fit photo to 1920 wide, then zoom around a point near the faces
    base = W / team.width
    k = base * s
    cx, cy = team.width * 0.5, team.height * 0.47
    ox = W / 2 - cx * k
    oy = H * 0.42 - cy * k + (1 - t) * 18
    img = team.transform((W, H), Image.AFFINE, (1 / k, 0, -ox / k, 0, 1 / k, -oy / k), Image.BICUBIC)
    img = img.convert("RGBA")
    img.alpha_composite(team_grad)
    for e in team_els:
        e.draw(img, f)
    return img


# --- Panel scenes (footage left, copy right)
PANEL_X = 960
TX = 1040


def panel_bg():
    im = SILK.crop((0, 0, W, H)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle((PANEL_X, 0, PANEL_X + 5, H), fill=GOLD + (255,))
    return im


PANEL_BG = panel_bg()


def footer_els(start):
    logo = layer()
    logo.alpha_composite(fit_h(LOGO, 190), (TX, 842))
    pill, pb = phone_pill(x=TX + 170, y=870)
    soc = socials(pb[0] + pb[2] + 28, 883)
    return [El(logo, start, dy=20), El(pill, start + 6, dy=20), El(soc, start + 12, dy=20)]


def list_els(items, y0, step, start, stagger=9):
    els = []
    for i, it in enumerate(items):
        y = y0 + i * step
        im = layer()
        d = ImageDraw.Draw(im)
        draw_diamond(d, TX + 12, y + 30, 11, GOLD + (255,))
        d.text((TX + 46, y), it, font=F_ITEM, fill=INK + (255,))
        els.append(El(im, start + i * stagger, dx=-40, dy=0))
    return els


def rule_el(y, start):
    return El(shape_el(lambda d, im: d.rectangle((TX, y, TX + 90, y + 4), fill=GOLD + (255,))), start, dx=-50, dy=0)


s0 = SKIN[0] + FADE
skin_els = [
    El(text_el("SUMMER SKIN PREP", F_EYEBROW, GOLD_DK, (TX, 108), spacing=7), s0),
    El(text_el("Essentials that", F_HEAD, INK, (TX - 4, 150)), s0 + 6),
    El(text_el("aren’t SPF.", F_HEAD_IT, GOLD, (TX - 4, 252)), s0 + 12),
    rule_el(392, s0 + 18),
] + list_els(["Preventative Tox", "Microneedling + PRF", "VI Peel"], 440, 96, s0 + 26, stagger=12) \
  + footer_els(s0 + 60)

p0 = PERKS[0] + FADE
perks_els = [
    El(text_el("INTRODUCING", F_EYEBROW, GOLD_DK, (TX, 92), spacing=7), p0),
    El(text_el("Premier Perks", F_HEAD_IT, GOLD, (TX - 4, 132)), p0 + 6),
    El(text_el("Ask us which treatment is right for you.", F_BODY, INK, (TX, 260)), p0 + 12),
    rule_el(330, p0 + 18),
] + list_els(["Reset & Restore", "Brighten & Tighten", "Longevity & Wellness", "Clean & Intentional"],
             368, 86, p0 + 24, stagger=10) \
  + footer_els(p0 + 56)


def panel_frame(footage, f, scene, els):
    img = PANEL_BG.copy()
    t = (f - scene[0]) / (scene[1] - scene[0])
    k = 1.0 + 0.05 * t  # gentle push-in on the footage
    fw, fh = footage.size
    ox = fw / 2 - fw / 2 * k
    oy = fh / 2 - fh / 2 * k
    fr = footage.transform((PANEL_X, H), Image.AFFINE, (1 / k, 0, -ox / k, 0, 1 / k, -oy / k), Image.BICUBIC)
    img.paste(fr, (0, 0))
    for e in els:
        e.draw(img, f)
    return img


# --- End card
e0 = END[0] + FADE
_end_logo = layer()
_lg = fit_h(LOGO, 330)
_end_logo.alpha_composite(_lg, ((W - _lg.width) // 2, 110))


def centered_text(text, fnt, fill, y, spacing=0):
    w = sum(fnt.getlength(c) + spacing for c in text) - spacing
    return text_el(text, fnt, fill, (round((W - w) / 2), y), spacing)


_end_pill, _epb = phone_pill(cx=W / 2, y=770, scale=1.15)
end_els = [
    El(_end_logo, e0 - 6, dy=30),
    El(centered_text("Your natural beauty, elevated.", F_END, INK, 485), e0 + 8),
    El(shape_el(lambda d, im: d.rectangle((W // 2 - 45, 612, W // 2 + 45, 616), fill=GOLD + (255,))), e0 + 14, dy=0),
    El(centered_text("BOOK YOUR CONSULTATION TODAY", F_EYEBROW, GOLD_DK, 650, spacing=8), e0 + 18),
    El(_end_pill, e0 + 24),
    El(socials(W // 2 - 71, 900), e0 + 30),
]
END_BG = SILK.convert("RGBA")


def end_frame(f):
    img = END_BG.copy()
    for e in end_els:
        e.draw(img, f)
    return img


# ---------------------------------------------------------------- video I/O
def ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


FF = ffmpeg_bin()


class Reader:
    def __init__(self, path, w, h):
        self.w, self.h, self.n, self.last = w, h, -1, None
        self.p = subprocess.Popen([FF, "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)

    def get(self, i):
        while self.n < i:
            b = self.p.stdout.read(self.w * self.h * 3)
            if len(b) < self.w * self.h * 3:
                break  # hold last frame
            self.last = Image.frombuffer("RGB", (self.w, self.h), b, "raw", "RGB", 0, 1)
            self.n += 1
        return self.last


def blend(a, b, t):
    return Image.blend(a.convert("RGB"), b.convert("RGB"), ease(t)) if t < 1 else b.convert("RGB")


def main():
    intro = Reader(os.path.join(SRC, "intro_logo.mp4"), W, H)
    skin = Reader(os.path.join(SRC, "footage_microneedling.mp4"), 960, H)
    perks = Reader(os.path.join(SRC, "footage_injectables.mp4"), 960, H)

    enc = subprocess.Popen([
        FF, "-v", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-f", "lavfi", "-t", "30.03", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "15",
        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT,
    ], stdin=subprocess.PIPE)

    for f in range(TOTAL):
        if f < GROUP[0]:
            frame = intro.get(min(f, 65)).convert("RGB")
        elif f < GROUP[0] + FADE:
            frame = blend(intro.get(65), team_frame(f), (f - GROUP[0]) / FADE)
        elif f < SKIN[0]:
            frame = team_frame(f)
        elif f < SKIN[0] + FADE:
            frame = blend(team_frame(f), panel_frame(skin.get(f - SKIN[0]), f, SKIN, skin_els),
                          (f - SKIN[0]) / FADE)
        elif f < PERKS[0]:
            frame = panel_frame(skin.get(f - SKIN[0]), f, SKIN, skin_els)
        elif f < PERKS[0] + FADE:
            frame = blend(panel_frame(skin.get(f - SKIN[0]), f, SKIN, skin_els),
                          panel_frame(perks.get(f - PERKS[0]), f, PERKS, perks_els), (f - PERKS[0]) / FADE)
        elif f < END[0]:
            frame = panel_frame(perks.get(f - PERKS[0]), f, PERKS, perks_els)
        elif f < END[0] + FADE:
            frame = blend(panel_frame(perks.get(f - PERKS[0]), f, PERKS, perks_els), end_frame(f),
                          (f - END[0]) / FADE)
        else:
            frame = end_frame(f)
        enc.stdin.write(frame.convert("RGB").tobytes())
        if f % 100 == 0:
            print(f"frame {f}/{TOTAL}", flush=True)

    enc.stdin.close()
    enc.wait()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
