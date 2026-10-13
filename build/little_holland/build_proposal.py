"""
Builds MCTV_Proposal_Little_Holland_PLLC.pdf — a 9-page landscape proposal for
Stan Little covering two businesses:

  * Little & Holland, PLLC — 15-second spots, four options (20 / 40 / 80
    screens, or 80 screens + MCTV Traffic sponsorship in Oxford). One spot on
    every screen, or two split by venue type (DUI in college-crowd venues,
    The Oxford Family Membership in family/professional venues), same price.
  * Stan's rental car business — a 15-second spot at 50% off the matching
    screen package, on the same screens

Styled after MCTV's Schwartz 2027 proposal.

Pipeline: pull logos/headshot out of the original media kit, knock out the
client logo's background, fill template.html (Jinja2), print with Chromium.

Run from anywhere:  python3 build/little_holland/build_proposal.py
Needs:  pip install pymupdf jinja2 playwright pillow numpy
Output is written to the repo root.
"""
import json, os
import numpy as np
import pymupdf as fitz
from PIL import Image
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KIT = os.path.join(ROOT, "build", "source", "MCTV_Media_Kit_Oxford_original.pdf")
ASSETS = os.path.join(HERE, "_assets")
HTML_OUT = os.path.join(ASSETS, "proposal.html")
OUT = os.path.join(ROOT, "MCTV_Proposal_Little_Holland_PLLC.pdf")
CHROMIUM = "/opt/pw-browsers/chromium"
CLIENT_LOGO = os.path.join(HERE, "little_holland_logo.png")   # supplied by the client (navy bg)

# ---------- pricing ----------
SCREEN_RATE = {20: 500, 40: 800, 80: 1400}       # media kit package page
PLAYS = {20: "30K", 40: "60K", 80: "120K"}       # 1,500 plays per screen per month
PER_SCREEN = {20: "$25", 40: "$20", 80: "$17.50"}
RENTAL_DISCOUNT = 0.50                           # rental car :15: 50% off the matching screen rate, same plays

OPTIONS = [  # Little & Holland's four options; "where"/"foot" are the card's last lines
    {"n": 1, "title": "20 Screens", "short": "20 screens", "screens": 20, "monthly": 500,
     "where": "Can run entirely inside Oxford's host venues.", "foot": "Entry network reach."},
    {"n": 2, "title": "40 Screens", "short": "40 screens", "screens": 40, "monthly": 800,
     "where": "Can run entirely inside Oxford's host venues.", "foot": "Market saturation."},
    {"n": 3, "title": "80 Screens", "short": "80 screens", "screens": 80, "monthly": 1400,
     "where": "Oxford, plus Tupelo and the Golden Triangle.", "foot": "Deep saturation."},
    {"n": 4, "title": "80 Screens + Traffic", "long": "80 Screens + MCTV Traffic", "short": "80 + Traffic", "screens": 80,
     "monthly": 2000, "traffic": True,
     "where": "Oxford, plus Tupelo and the Golden Triangle, and your name on Oxford's traffic board.",
     "foot": "Credited to the business you pick."},
]

def money(v):
    return f"${v:,.0f}"

def pricing():
    rows = []
    for o in OPTIONS:
        s = o["screens"]
        lh = o["monthly"]
        rental = round(SCREEN_RATE[s] * (1 - RENTAL_DISCOUNT))
        both = lh + rental
        rows.append({"long": o["title"], **o,
            "plays": PLAYS[s], "per_screen": PER_SCREEN[s],
            "lh": lh, "rental": rental, "both": both,
            "lh_s": money(lh), "rental_s": money(rental), "both_s": money(both), "lh_num": f"{lh:,}",
            "rental_reg_s": money(SCREEN_RATE[s]),
            # pay up front: 6 months -> 7 on air, 12 months -> 14 on air
            "lh6_s": money(6 * lh), "both6_s": money(6 * both),
            "lh12_s": money(12 * lh), "both12_s": money(12 * both),
            "save6_lh_s": money(lh), "save6_both_s": money(both),
            "save12_lh_s": money(2 * lh), "save12_both_s": money(2 * both)})
    return rows

def rental_tiers():
    return [{"screens": s, "price_s": money(round(r * (1 - RENTAL_DISCOUNT))), "reg_s": money(r),
             "plays": PLAYS[s]} for s, r in SCREEN_RATE.items()]

# ---------- assets ----------
LOGOS = {84: (85, "logo_white.png"),     # (image xref, soft-mask xref) in the media kit
         86: (87, "logo_navy.png")}
HEADSHOT = 416                           # Swayze headshot

def extract_assets():
    os.makedirs(ASSETS, exist_ok=True)
    kit = fitz.open(KIT)
    with open(os.path.join(ASSETS, "swayze.jpg"), "wb") as f:
        f.write(kit.extract_image(HEADSHOT)["image"])
    for xref, (mask, name) in LOGOS.items():
        fitz.Pixmap(fitz.Pixmap(kit, xref), fitz.Pixmap(kit, mask)).save(os.path.join(ASSETS, name))

def client_logo():
    """Knock out the logo's navy background (colour-to-alpha) and upscale it,
    so it sits cleanly on any dark MCTV background."""
    im = np.asarray(Image.open(CLIENT_LOGO).convert("RGB")).astype(float)
    bg = np.array([0x00, 0x10, 0x2c], float)
    room = np.where(im >= bg, 255 - bg, bg)                 # distance to white or black per channel
    a = np.clip((np.abs(im - bg) / room).max(axis=2), 0, 1)
    fg = bg + (im - bg) / np.maximum(a, 1e-6)[..., None]
    rgba = np.dstack([np.clip(fg, 0, 255), a * 255]).astype("uint8")
    out = Image.fromarray(rgba, "RGBA")
    out = out.resize((out.width * 4, out.height * 4), Image.LANCZOS)
    out.save(os.path.join(ASSETS, "lh_logo.png"))

# ---------- render ----------
def render_html(copy):
    kit_venues = fitz.open(KIT)[4].get_text()          # media kit host-network page
    unknown = [v for v in copy["venues_dui"] + copy["venues_member"] if v not in kit_venues]
    assert not unknown, f"venues not on the media kit's host list: {unknown}"
    env = Environment(loader=FileSystemLoader(HERE), autoescape=True)
    page = env.get_template("template.html").render(c=copy, opts=pricing(), rental=rental_tiers())
    with open(HTML_OUT, "w") as f:
        f.write(page)

def print_pdf():
    with sync_playwright() as pw:
        exe = CHROMIUM if os.path.exists(CHROMIUM) else None
        browser = pw.chromium.launch(executable_path=exe)
        page = browser.new_page()
        page.goto("file://" + HTML_OUT)
        page.wait_for_load_state("networkidle")
        page.pdf(path=OUT, width="11in", height="6.5in", print_background=True,
                 prefer_css_page_size=True)
        browser.close()
    doc = fitz.open(OUT)
    doc.set_metadata({"title": "MCTV Digital — Advertising Proposal for Stan Little",
                      "author": "Swayze Hollingsworth · MCTV Digital",
                      "subject": "Little & Holland, PLLC and rental car :15 spots on the MCTV screen network"})
    doc.saveIncr()
    print("saved", OUT, f"({len(doc)} pages)")

if __name__ == "__main__":
    with open(os.path.join(HERE, "copy.json")) as f:
        copy = json.load(f)
    extract_assets()
    client_logo()
    render_html(copy)
    print_pdf()
