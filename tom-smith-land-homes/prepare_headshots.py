"""Upscales the headshot and removes its background (rembg) so it can sit over
the green wave / blue band like the cut-out photo on the business card.

    pip install pillow rembg onnxruntime
    python3 prepare_headshots.py
"""
import os
from PIL import Image, ImageFilter
from rembg import remove, new_session

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "assets", "source")
OUT = os.path.join(BASE, "assets", "img")
session = new_session("u2net_human_seg")

def prep(name, scale):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    if scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
    cut = remove(im, session=session, post_process_mask=True)
    return im, cut

for src, dst, scale in [("chance-headshot.jpg", "chance", 1.5)]:
    im, cut = prep(src, scale)
    im.save(os.path.join(OUT, dst + "-upscaled.jpg"), quality=94)
    cut.save(os.path.join(OUT, dst + "-cutout.png"))
    print(dst, im.size, "->", cut.size)
