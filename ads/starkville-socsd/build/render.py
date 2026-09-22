#!/usr/bin/env python3
"""
Render the 30-second SOCSD ad at 1920x1080, 30 fps, H.264.

Usage:  python3 render.py            (from ads/starkville-socsd/build)
Output: ../SOCSD_30s_1920x1080.mp4  and  ../SOCSD_keyframes.png

Assets (all optional) go in ../assets/:
  logo.png                 district logo, transparent PNG, shown on end card
  scene1.jpg ... scene5.jpg  photo for each scene (Ken Burns zoom applied)
  music.mp3 / music.wav    background track (trimmed/faded to 30 s)
If a scene photo is missing a black-and-gold motion background is used instead.
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1920, 1080, 30, 30
N = FPS * DUR
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
OUT = os.path.join(HERE, "..", "SOCSD_30s_1920x1080.mp4")
SHEET = os.path.join(HERE, "..", "SOCSD_keyframes.png")

GOLD = (253, 185, 39)
BLACK = (10, 10, 12)
WHITE = (255, 255, 255)

FONT_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# ---- Script: (start_s, end_s, headline, subline) ---------------------------
SCENES = [
    (0,  5,  "EVERY STUDENT.\nEVERY DAY.",            "Starkville Oktibbeha Consolidated School District"),
    (5,  10, "LEARNING THAT\nLEADS THE WAY.",         "Pre-K through 12th grade, right here at home"),
    (10, 15, "CHAMPIONS IN THE\nCLASSROOM & BEYOND.", "Academics  |  Arts  |  Athletics"),
    (15, 20, "PARTNERED WITH\nMISSISSIPPI STATE.",    "Real-world learning, powered by our community"),
    (20, 25, "YOUR CHILD.\nOUR PROMISE.",             "Safe, supported, and ready for what's next"),
]
END = (25, 30, "PROUD TO BE SOCSD", "starkvillesd.com")

def font(path, size):
    return ImageFont.truetype(path, size)

def ease(t):  # smoothstep
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

def load_photo(i):
    for ext in ("jpg", "jpeg", "png"):
        p = os.path.join(ASSETS, f"scene{i}.{ext}")
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            # cover-fit to slightly larger than frame so Ken Burns can zoom
            s = max(W * 1.12 / im.width, H * 1.12 / im.height)
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
            return im
    return None

def gradient_bg():
    """Static black->charcoal diagonal base used when no photo is supplied."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = (x / W * 0.6 + y / H * 0.4)
    base = np.stack([12 + 18 * d, 12 + 18 * d, 14 + 22 * d], axis=-1)
    return Image.fromarray(base.clip(0, 255).astype(np.uint8))

BASE_BG = gradient_bg()

def motion_bg(t_local, seed):
    """Gold light streaks drifting across a dark field."""
    im = BASE_BG.copy()
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rng = np.random.RandomState(seed)
    for k in range(6):
        w = int(rng.uniform(140, 420))
        speed = rng.uniform(60, 140)
        x0 = int((rng.uniform(-W, W) + t_local * speed) % (W + 1200)) - 600
        alpha = int(rng.uniform(18, 40))
        d.polygon([(x0, -50), (x0 + w, -50), (x0 + w - 700, H + 50), (x0 - 700, H + 50)],
                  fill=GOLD + (alpha,))
    ov = ov.filter(ImageFilter.GaussianBlur(60))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    return im

def photo_frame(photo, t_local, dur):
    """Ken Burns: slow zoom-in from 1.00 to 1.10 with slight drift."""
    z = 1.0 + 0.10 * (t_local / dur)
    cw, ch = int(W / z * 1.0), int(H / z * 1.0)
    cx = (photo.width - cw) // 2 + int(40 * t_local / dur)
    cy = (photo.height - ch) // 2
    crop = photo.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.BILINEAR)
    # darken for legibility
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.blend(crop, dark, 0.35)

def draw_text_block(frame, headline, sub, a, slide, big=104, small=44, align="left"):
    """Draw headline+subline with alpha a (0-1) and vertical slide px."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    fb, fr = font(FONT_B, big), font(FONT_R, small)
    lines = headline.split("\n")
    lh = int(big * 1.08)
    total = lh * len(lines) + 30 + small
    y = (H - total) // 2 + slide
    A = int(255 * a)
    x = 160
    # gold accent bar
    d.rectangle([x - 40, y + 8, x - 26, y + lh * len(lines) - 6], fill=GOLD + (A,))
    for ln in lines:
        d.text((x, y), ln, font=fb, fill=WHITE + (A,))
        y += lh
    d.text((x, y + 30), sub, font=fr, fill=GOLD + (A,))
    return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

def draw_endcard(frame, t_local, dur, logo):
    a = ease(t_local / 0.8)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    A = int(255 * a)
    cy = 300
    if logo is not None:
        lg = logo.copy()
        s = min(520 / lg.width, 300 / lg.height)
        lg = lg.resize((int(lg.width * s), int(lg.height * s)), Image.LANCZOS)
        lg.putalpha(lg.split()[-1].point(lambda v: int(v * a)))
        ov.alpha_composite(lg, ((W - lg.width) // 2, cy - lg.height // 2))
        cy += lg.height // 2 + 70
    else:
        # monogram placeholder: gold ring with "SOCSD"
        d.ellipse([W//2 - 150, cy - 150, W//2 + 150, cy + 150], outline=GOLD + (A,), width=10)
        f = font(FONT_B, 82); tw = d.textlength("SOCSD", font=f)
        d.text(((W - tw) // 2, cy - 48), "SOCSD", font=f, fill=WHITE + (A,))
        cy += 240
    f1 = font(FONT_B, 96); tw = d.textlength(END[2], font=f1)
    d.text(((W - tw) // 2, cy), END[2], font=f1, fill=WHITE + (A,))
    f2 = font(FONT_R, 48)
    name = "Starkville Oktibbeha Consolidated School District"
    tw = d.textlength(name, font=f2)
    d.text(((W - tw) // 2, cy + 130), name, font=f2, fill=(220, 220, 220, A))
    # website pill
    a2 = ease((t_local - 0.6) / 0.8)
    A2 = int(255 * a2)
    f3 = font(FONT_B, 56); tw = d.textlength(END[3], font=f3)
    px, py = (W - tw) // 2 - 50, cy + 230
    d.rounded_rectangle([px, py, px + tw + 100, py + 96], radius=48, fill=GOLD + (A2,))
    d.text((px + 50, py + 16), END[3], font=f3, fill=BLACK + (A2,))
    return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

def build_frame(i, photos, logo):
    t = i / FPS
    # global fade-in at start and fade-out at very end
    for si, (s, e, head, sub) in enumerate(SCENES):
        if s <= t < e:
            tl, dur = t - s, e - s
            bg = photo_frame(photos[si], tl, dur) if photos[si] else motion_bg(t, si)
            a = min(ease(tl / 0.6), ease((dur - tl) / 0.5))
            slide = int(40 * (1 - ease(tl / 0.6)))
            fr = draw_text_block(bg, head, sub, a, slide)
            break
    else:
        s, e = END[0], END[1]
        tl, dur = t - s, e - s
        bg = motion_bg(t, 9)
        fr = draw_endcard(bg, tl, dur, logo)
    # thin gold footer stripe throughout
    d = ImageDraw.Draw(fr)
    d.rectangle([0, H - 14, W, H], fill=GOLD)
    if t < 0.5:
        fr = Image.blend(Image.new("RGB", (W, H), BLACK), fr, ease(t / 0.5))
    if t > DUR - 0.6:
        fr = Image.blend(fr, Image.new("RGB", (W, H), BLACK), ease((t - (DUR - 0.6)) / 0.6))
    return fr

def main():
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    photos = [load_photo(i + 1) for i in range(len(SCENES))]
    lp = os.path.join(ASSETS, "logo.png")
    logo = Image.open(lp).convert("RGBA") if os.path.exists(lp) else None
    music = next(iter(glob.glob(os.path.join(ASSETS, "music.*"))), None)
    print("photos:", [bool(p) for p in photos], "logo:", bool(logo), "music:", music)

    cmd = [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-"]
    if music:
        cmd += ["-i", music, "-af", f"afade=t=in:d=1,afade=t=out:st={DUR-2}:d=2"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    cmd += ["-map", "0:v", "-map", "1:a", "-t", str(DUR), "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.1",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    keyframes = []
    for i in range(N):
        fr = build_frame(i, photos, logo)
        p.stdin.write(fr.tobytes())
        if i % (FPS * 5) == FPS * 2:      # 2 s into each scene
            keyframes.append(fr.resize((640, 360), Image.LANCZOS))
        if i % 150 == 0:
            print(f"  {i}/{N} frames", flush=True)
    p.stdin.close(); p.wait()
    sheet = Image.new("RGB", (640 * 3, 360 * 2), BLACK)
    for k, im in enumerate(keyframes[:6]):
        sheet.paste(im, ((k % 3) * 640, (k // 3) * 360))
    sheet.save(SHEET)
    print("wrote", OUT, "and", SHEET)

if __name__ == "__main__":
    main()
