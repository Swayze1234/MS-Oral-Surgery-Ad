#!/usr/bin/env python3
"""
Render the 30-second SOSD Discovery Center / Project CARE ad.
1920x1080, 30 fps, H.264 + AAC.   Run:  python3 render.py   (from build/)
Source art lives in build/src/ (flyer, brochure pages, CARE_Logo.docx export).
Output: ../ProjectCARE_30s_1920x1080.mp4 and ../ProjectCARE_keyframes.png
"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1920, 1080, 30, 30
N = FPS * DUR
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = os.path.join(HERE, "..", "ProjectCARE_30s_1920x1080.mp4")
SHEET = os.path.join(HERE, "..", "ProjectCARE_keyframes.png")

TEAL = (41, 165, 158); TEAL_D = (30, 130, 125); LIME = (141, 178, 55)
YELLOW = (247, 201, 72); WHITE = (255, 255, 255); INK = (40, 40, 40)
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# ---------------- source crops ----------------
def crop(name, box, path=None):
    im = Image.open(os.path.join(SRC, path)).convert("RGB").crop(box)
    return im
outp, insp, flyp, logop = "brochure_outside.png", "brochure_inside.png", "flyer.png", "docx_media/image1.png"
PHOTOS = {
    "family":  crop("family", (1380, 560, 1955, 1140), outp),
    "podium":  crop("podium", (355, 225, 595, 775), insp),
    "shelves": crop("shelves", (35, 285, 570, 995), outp),
    "rug":     crop("rug", (1360, 1020, 1950, 1495), insp),
    "roy":     crop("roy", (355, 225, 595, 775), insp),
}
LOCKUP = Image.open(os.path.join(SRC, logop)).convert("RGB")          # Discovery Center + CARE badge
BADGE = Image.open(os.path.join(SRC, flyp)).convert("RGBA").crop((470, 30, 662, 217))

# ---------------- script ----------------
# each scene: (start, end, kicker, headline lines, body lines, yellow_tag, photo)
SCENES = [
    (0, 5,  "SOSD Discovery Center · Family Resource Center",
            ["PROJECT", "CARE"], ["Healthy Families.", "Happy Families."], None, "family"),
    (5, 10, "Join our parenting class",
            ["ACTIVE", "PARENTING"], ["Attend two classes and receive", "FREE diapers & wipes while supplies last"],
            ("Wednesdays & Thursdays", "11:00 am – 12:00 pm"), "podium"),
    (10, 15, "Discovery Center",
            ["FAMILY RESOURCE", "LIBRARY"], ["Children's books  ·  Manipulatives", "Educational games  ·  Skill-building activities"],
            ("Monday – Friday", "8:00 am – 4:30 pm"), "shelves"),
    (15, 20, "Programs & Support",
            ["MORE WAYS", "WE HELP"], ["Dolly Parton's Imagination Library: free books", "mailed to children birth to age 5",
                                        "Teen parent classes  ·  Family events  ·  Free adult therapy"], None, "rug"),
    (20, 25, "For more information, contact Roy Ann Bell",
            ["CALL", "TODAY"], ["1504 Louisville Street", "Starkville, MS"],
            ("662-615-0033", "662-320-4607"), "family"),
]

def font(p, s): return ImageFont.truetype(p, s)
def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

# ---------------- background ----------------
def make_base():
    """Teal field with faint family silhouettes echoing the flyer."""
    im = Image.new("RGB", (W, H), TEAL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    c = (255, 255, 255, 22)
    def person(x, y, s):
        d.ellipse([x - 0.18*s, y, x + 0.18*s, y + 0.36*s], fill=c)
        d.rounded_rectangle([x - 0.32*s, y + 0.40*s, x + 0.32*s, y + 1.4*s], radius=int(0.3*s), fill=c)
    person(1250, 120, 420); person(1520, 200, 360); person(1400, 480, 240); person(1650, 520, 200)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
BASE = make_base()

def background(t):
    im = BASE.copy(); d = ImageDraw.Draw(im, "RGBA")
    # slow-drifting lime chevron band along the bottom, like the flyer's green wedge
    dx = int(60 * np.sin(t * 0.6))
    d.polygon([(0, H - 150 + dx // 3), (760 + dx, H - 210), (820 + dx, H - 120), (0, H - 60)], fill=LIME)
    d.rectangle([0, H - 60, W, H], fill=LIME)
    return im

def photo_card(fr, key, tl, dur, a):
    """Rounded, white-bordered photo card on the right, gentle zoom, slides in."""
    ph = PHOTOS[key]
    cw, ch = 700, 690
    z = 1.0 + 0.08 * tl / dur
    s = max(cw / ph.width, ch / ph.height) * z
    big = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)
    x0 = (big.width - cw) // 2; y0 = 0 if big.height > big.width else (big.height - ch) // 2
    img = big.crop((x0, y0, x0 + cw, y0 + ch))
    card = Image.new("RGBA", (cw + 28, ch + 28), (0, 0, 0, 0))
    m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw + 27, ch + 27], radius=42, fill=255)
    card.paste(WHITE + (255,), (0, 0, cw + 28, ch + 28), m)
    m2 = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m2).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=32, fill=255)
    card.paste(img, (14, 14), m2)
    # drop shadow
    sh = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([46, 60, cw + 74, ch + 88], radius=42, fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    slide = int(120 * (1 - a))
    X, Y = 1120 + slide, 215
    A = int(255 * a)
    sh.putalpha(sh.split()[-1].point(lambda v: v * A // 255)); card.putalpha(card.split()[-1].point(lambda v: v * A // 255))
    fr.alpha_composite(sh, (X - 46, Y - 60)); fr.alpha_composite(card, (X, Y))

def text_block(fr, kicker, head, body, tag, a):
    d = ImageDraw.Draw(fr)
    A = int(255 * a); slide = int(50 * (1 - a))
    x, y = 110, 150 + slide
    d.text((x, y), kicker, font=font(FR, 40), fill=WHITE + (A,)); y += 70
    MAXW = 960
    hs = 132
    while any(d.textlength(ln, font=font(FB, hs)) > MAXW for ln in head): hs -= 4
    for i, ln in enumerate(head):
        f = font(FR, hs) if (len(head) == 2 and i == 0 and head[0] in ("ACTIVE", "PROJECT")) else font(FB, hs)
        d.text((x, y), ln, font=f, fill=WHITE + (A,)); y += int(hs * 1.06)
    y += 20
    if tag:
        f1, f2 = font(FB, 72), font(FB, 60)
        w = max(d.textlength(tag[0], font=f1), d.textlength(tag[1], font=f2)) + 90
        d.polygon([(x - 20, y), (x + w, y), (x + w + 60, y + 90), (x + w, y + 180), (x - 20, y + 180)], fill=YELLOW + (A,))
        d.text((x + 20, y + 10), tag[0], font=f1, fill=INK + (A,))
        d.text((x + 20, y + 100), tag[1], font=f2, fill=INK + (A,))
        y += 215
    bs = 42
    while any(d.textlength(ln, font=font(FR, bs)) > MAXW for ln in body): bs -= 2
    fb = font(FR, bs)
    for ln in body:
        d.text((x, y), ln, font=fb, fill=WHITE + (A,)); y += int(bs * 1.35)

def scene_frame(t):
    for s, e, kicker, head, body, tag, photo in SCENES:
        if s <= t < e:
            tl, dur = t - s, e - s
            a_in = ease(tl / 0.7); a_out = ease((dur - tl) / 0.4); a = min(a_in, a_out)
            fr = background(t).convert("RGBA")
            photo_card(fr, photo, tl, dur, a)
            text_block(fr, kicker, head, body, tag, a)
            # small CARE badge, top-right, persistent
            b = BADGE.resize((170, 166), Image.LANCZOS); fr.alpha_composite(b, (W - 210, 32))
            return fr.convert("RGB")
    return end_card(t - SCENES[-1][1])

def end_card(tl):
    a = ease(tl / 0.8); A = int(255 * a)
    fr = background(SCENES[-1][1] + tl).convert("RGBA")
    d = ImageDraw.Draw(fr)
    # white panel with logo lockup
    lw = 1100; lh = int(LOCKUP.height * lw / LOCKUP.width)
    lock = LOCKUP.resize((lw, lh), Image.LANCZOS).convert("RGBA")
    px, py = (W - lw) // 2 - 60, 120 - int(40 * (1 - a))
    panel = Image.new("RGBA", (lw + 120, lh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle([0, 0, lw + 119, lh + 79], radius=40, fill=(255, 255, 255, A))
    lock.putalpha(lock.split()[-1].point(lambda v: v * A // 255))
    panel.alpha_composite(lock, (60, 40))
    fr.alpha_composite(panel, (px, py))
    y = py + lh + 130
    a2 = ease((tl - 0.5) / 0.7); A2 = int(255 * a2)
    f = font(FB, 64); s = "StarkvilleSD.com/DiscoveryCenter"; tw = d.textlength(s, font=f)
    d.rounded_rectangle([(W - tw) // 2 - 50, y, (W + tw) // 2 + 50, y + 100], radius=50, fill=YELLOW + (A2,))
    d.text(((W - tw) // 2, y + 14), s, font=f, fill=INK + (A2,)); y += 130
    f = font(FB, 50); s = "662-615-0033   ·   1504 Louisville Street, Starkville, MS"; tw = d.textlength(s, font=f)
    d.text(((W - tw) // 2, y), s, font=f, fill=WHITE + (A2,)); y += 70
    f = font(FR, 38); s = "Find us on Facebook: SOSD Discovery Center"; tw = d.textlength(s, font=f)
    d.text(((W - tw) // 2, y), s, font=f, fill=WHITE + (A2,))
    f = font(FR, 30); s = "Funded by MS Department of Child Protection Services"; tw = d.textlength(s, font=f)
    d.text(((W - tw) // 2, H - 48), s, font=f, fill=INK + (A2,))
    return fr.convert("RGB")

def build_frame(i):
    t = i / FPS
    fr = scene_frame(t)
    if t < 0.5:
        fr = Image.blend(Image.new("RGB", (W, H), TEAL_D), fr, ease(t / 0.5))
    if t > DUR - 0.6:
        fr = Image.blend(fr, Image.new("RGB", (W, H), TEAL_D), ease((t - (DUR - 0.6)) / 0.6))
    return fr

def main():
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    music = next((os.path.join(SRC, f) for f in os.listdir(SRC) if f.startswith("music.")), None)
    cmd = [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    cmd += (["-i", music, "-af", f"afade=t=in:d=1,afade=t=out:st={DUR-2}:d=2"] if music
            else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"])
    cmd += ["-map", "0:v", "-map", "1:a", "-t", str(DUR), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.1", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", OUT]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    keys = []
    for i in range(N):
        fr = build_frame(i); p.stdin.write(fr.tobytes())
        if i % (FPS * 5) == FPS * 2: keys.append(fr.resize((640, 360), Image.LANCZOS))
        if i % 150 == 0: print(f"  {i}/{N}", flush=True)
    p.stdin.close(); p.wait()
    sheet = Image.new("RGB", (1920, 720), INK)
    for k, im in enumerate(keys[:6]): sheet.paste(im, ((k % 3) * 640, (k // 3) * 360))
    sheet.save(SHEET); print("wrote", OUT)

if __name__ == "__main__":
    main()
