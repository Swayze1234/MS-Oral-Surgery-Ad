"""
One-time helper: builds the photo assets in photos/ for the Stan Little proposal.

It takes room photos and Oxford photos out of MCTV's Schwartz 2027 proposal PDF
(not kept in this repo, since it is another client's proposal), renders two
mock ads from mockup_ads.html, and warps each ad onto a real MCTV screen.

    python3 build/little_holland/make_mockups.py /path/to/Schwartz-MCTV-2027-Exclusivity.pdf

Outputs (committed):  photos/cover_mockup.jpg, photos/rental_mockup.jpg,
photos/oxford_aerial.jpg, photos/oxford_lights.jpg, photos/swayze.jpg,
photos/traffic_board.jpg
"""
import io, os, sys
import numpy as np
import pymupdf as fitz
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
ASSETS = os.path.join(HERE, "_assets")
CHROMIUM = "/opt/pw-browsers/chromium"

# image xrefs inside the Schwartz PDF
X_COVER_ROOM, X_STATION, X_AERIAL, X_LIGHTS, X_SWAYZE, X_TRAFFIC = 4, 110, 147, 330, 60, 204

# screen corners (TL, TR, BR, BL) in each room photo, in that photo's pixels
COVER_QUAD = [(389, 530), (1471, 592), (1616, 1142), (356, 1123)]
STATION_QUAD = [(270, 94), (824, 119), (824, 414), (245, 404)]

def pdf_image(doc, xref):
    return Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("RGB")

def render_ads():
    """Screenshot the two 1920x1080 ads in mockup_ads.html."""
    src = os.path.join(ASSETS, "mockup_ads.html")
    with open(os.path.join(HERE, "mockup_ads.html")) as f:
        html = f.read()
    with open(src, "w") as f:                      # sits next to lh_logo.png in _assets
        f.write(html)
    ads = {}
    with sync_playwright() as pw:
        exe = CHROMIUM if os.path.exists(CHROMIUM) else None
        browser = pw.chromium.launch(executable_path=exe)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("file://" + src)
        page.wait_for_load_state("networkidle")
        for ad in ("lh", "rent"):
            ads[ad] = Image.open(io.BytesIO(page.locator(f"#{ad}").screenshot())).convert("RGB")
        browser.close()
    return ads

def perspective_coeffs(dst, src):
    """Coefficients for Image.transform(PERSPECTIVE): maps output (dst) points to input (src) points."""
    a = []
    for (x, y), (u, v) in zip(dst, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = [c for p in src for c in p]
    return np.linalg.solve(np.array(a, float), np.array(b, float)).tolist()

def place(photo, ad, quad, shade=0.92):
    w, h = ad.size
    coeffs = perspective_coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    warped = ad.transform(photo.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    mask = Image.new("L", ad.size, 255).transform(photo.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    warped = Image.eval(warped, lambda c: int(c * shade)).filter(ImageFilter.GaussianBlur(0.6))
    out = photo.copy()
    out.paste(warped, (0, 0), mask.filter(ImageFilter.GaussianBlur(0.8)))
    return out

def main(schwartz_pdf):
    os.makedirs(PHOTOS, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)
    sys.path.insert(0, HERE)
    from build_proposal import client_logo      # writes _assets/lh_logo.png
    client_logo()
    doc = fitz.open(schwartz_pdf)
    ads = render_ads()
    place(pdf_image(doc, X_COVER_ROOM), ads["lh"], COVER_QUAD).save(os.path.join(PHOTOS, "cover_mockup.jpg"), quality=88)
    place(pdf_image(doc, X_STATION), ads["rent"], STATION_QUAD).save(os.path.join(PHOTOS, "rental_mockup.jpg"), quality=88)
    for xref, name in [(X_AERIAL, "oxford_aerial.jpg"), (X_LIGHTS, "oxford_lights.jpg"),
                       (X_SWAYZE, "swayze.jpg"), (X_TRAFFIC, "traffic_board.jpg")]:
        pdf_image(doc, xref).save(os.path.join(PHOTOS, name), quality=88)
    print("wrote", sorted(os.listdir(PHOTOS)))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
