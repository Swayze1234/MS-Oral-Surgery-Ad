"""
Builds MCTV_Proposal_Little_Holland_PLLC.pdf — a client proposal for
Little & Holland PLLC (Oxford, MS; contact Stan Little): two 15-second
commercials on 20, 40 or 80 screens.

Pipeline:
  1. Pull brand assets (logos, Oxford photos, Swayze headshot) straight out of
     the original Oxford media kit, so nothing is duplicated in the repo.
  2. Fill template.html with copy.json + pricing math (Jinja2).
  3. Print the HTML to PDF with headless Chromium (Playwright).
  4. Splice in two pages from the media kit as-is (partner logos, CPM
     comparison) and renumber them.

Run from anywhere:  python3 build/little_holland/build_proposal.py
Needs:  pip install pymupdf jinja2 playwright
Output is written to the repo root.
"""
import html, json, os, re
import pymupdf as fitz
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KIT = os.path.join(ROOT, "build", "source", "MCTV_Media_Kit_Oxford_original.pdf")
ASSETS = os.path.join(HERE, "_assets")
HTML_OUT = os.path.join(ASSETS, "proposal.html")
PDF_TMP = os.path.join(ASSETS, "proposal_html.pdf")
OUT = os.path.join(ROOT, "MCTV_Proposal_Little_Holland_PLLC.pdf")
LIB = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
CHROMIUM = "/opt/pw-browsers/chromium"

# ---------- 1. assets from the media kit ----------
# xref -> filename (xrefs found with page.get_image_info(xrefs=True))
PHOTOS = {83: "oxford_stadium.jpg",     # Oxford cover: Vaught-Hemingway at night
          414: "oxford_tower.jpg",      # Oxford back page: water tower
          89: "in_the_wild.jpg",        # "Your ad, in the wild" (airport lobby)
          416: "swayze.jpg"}            # Swayze headshot (footer block)
LOGOS = {84: (85, "logo_white.png"),     # (image xref, soft-mask xref)
         86: (87, "logo_navy.png")}

def extract_assets():
    os.makedirs(ASSETS, exist_ok=True)
    kit = fitz.open(KIT)
    for xref, name in PHOTOS.items():
        with open(os.path.join(ASSETS, name), "wb") as f:
            f.write(kit.extract_image(xref)["image"])
    for xref, (mask, name) in LOGOS.items():
        fitz.Pixmap(fitz.Pixmap(kit, xref), fitz.Pixmap(kit, mask)).save(os.path.join(ASSETS, name))

# ---------- 2. pricing ----------
PLANS = [  # straight from the media kit's package page
    {"screens": 20, "monthly": 500,  "plays": "30K",  "per_screen": "$25",    "tag": "",             "label": "Entry network reach"},
    {"screens": 40, "monthly": 800,  "plays": "60K",  "per_screen": "$20",    "tag": "MOST POPULAR", "label": "Market saturation"},
    {"screens": 80, "monthly": 1400, "plays": "120K", "per_screen": "$17.50", "tag": "",             "label": "Deep saturation"},
]

def money(v, cents=False):
    return f"${v:,.2f}" if cents else f"${v:,.0f}"

def pricing():
    rows = []
    for p in PLANS:
        m = p["monthly"]
        six, twelve = 6 * m, 12 * m
        eff = twelve / 14           # prepaid 12 -> 14 months on air (same ratio as 6 -> 7)
        rows.append({**p,
                     "monthly_s": money(m),
                     "six_s": money(six),
                     "twelve_s": money(twelve),
                     "eff_s": money(round(eff)),
                     "eff_exact": abs(eff - round(eff)) < 1e-9,
                     "bonus6_s": money(m),
                     "bonus12_s": money(2 * m)})
    return rows

# ---------- 3. render ----------
OXFORD_VENUES = [  # media kit, host network page (Oxford / Lafayette, 44)
    "4 Corner's Chevron (Chicken On A Stick)", "Amara Salon & Aesthetics", "B's Hickory Smoke BBQ",
    "Bep Haus", "Booth's Barbeque and Yard", "Built Different Fitness",
    "Cannon Chevrolet Buick Cadillac of Oxford", "Cannon Collision Center", "Casa Mexicana of Oxford",
    "El Charro Cocina & Cantina", "Element Hair Studio", "Finch & Kelly",
    "Internal Medicine Associates of Oxford", "James Food Center Post Office", "LandShark Seafood & Catfish",
    "Luxe Styling Studio", "Magnolia Wine & Spirits", "MARATHON South Lamar",
    "Mississippi Asthma & Allergy Clinic, P.A.", "Nail E!", "Nail Thology", "Oxford Dental",
    "Oxford Park Commission", "Oxford Super Tan", "Oxford T-Shirt Co.",
    "Oxford-Lafayette County Chamber of Commerce", "Party in the Sip", "Rafters Music and Food",
    "Rainbow Cleaners", "Rebel Body Fitness", "Rebel Yell Rooftop Bar",
    "RedMed Urgent Clinic of Oxford - Jackson Ave", "Revive Wellness of Oxford",
    "Right Track Medical Group - Oxford", "Rosati's Pizza", "Sip Oxford", "Southern Coop",
    "Stouts Carpet & Flooring", "Texaco Lamar Express", "The Blind Pig Pub",
    "The Children's Dental Center", "The Oxford Growler", "The Velvet Ditch - Sports Bar & Seafood",
    "Uno Mas Tacos y Tequila Jackson Ave"]

def accent(text):
    """Escape, then turn *words* into the gold accent used in kit headlines."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(text))

def render_html(copy):
    assert len(OXFORD_VENUES) == 44
    picks = [v["venue"] for v in copy["venue_picks"]]
    missing = [v for v in picks if v not in OXFORD_VENUES]
    assert not missing, f"venue picks not in the Oxford host list: {missing}"
    copy = {**copy,
            "cover_title_html": accent(copy["cover_title"]),
            "intro_headline_html": accent(copy["intro_headline"]),
            "oxford_venues": OXFORD_VENUES,
            "pick_names": picks}
    env = Environment(loader=FileSystemLoader(HERE), autoescape=True)
    page = env.get_template("template.html").render(c=copy, plans=pricing())
    with open(HTML_OUT, "w") as f:
        f.write(page)

def print_pdf():
    with sync_playwright() as pw:
        exe = CHROMIUM if os.path.exists(CHROMIUM) else None
        browser = pw.chromium.launch(executable_path=exe)
        page = browser.new_page()
        page.goto("file://" + HTML_OUT)
        page.wait_for_load_state("networkidle")
        page.pdf(path=PDF_TMP, width="13.3333in", height="7.5in",   # 960 x 540 pt
                 print_background=True, prefer_css_page_size=True)
        browser.close()

# ---------- 4. splice kit pages + renumber ----------
# final order: (source, page index). "html" pages come from our render in order.
ORDER = ["html", "html", ("kit", 1), "html", "html", "html", ("kit", 3), "html", "html", "html"]
NUM_COLOR = {1: (0x6a, 0x78, 0x91), 3: (0x9e, 0xc1, 0xec)}   # page-number colour on each kit page

def assemble():
    src = fitz.open(PDF_TMP)
    kit = fitz.open(KIT)
    out = fitz.open()
    h = 0
    for n, item in enumerate(ORDER, start=1):
        if item == "html":
            out.insert_pdf(src, from_page=h, to_page=h)
            h += 1
            continue
        _, idx = item
        out.insert_pdf(kit, from_page=idx, to_page=idx)
        pg = out[-1]
        # swap the kit's page number for this proposal's page number
        pg.add_redact_annot(fitz.Rect(48, 512, 62, 521), fill=False)
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                            graphics=fitz.PDF_REDACT_LINE_ART_NONE)
        pg.insert_text((50.4, 518.1), f"{n:02d}", fontfile=LIB, fontname="lib",
                       fontsize=6.38, color=tuple(c / 255 for c in NUM_COLOR[idx]))
    assert h == len(src), f"template has {len(src)} pages, ORDER expects {h}"
    out.set_metadata({"title": "MCTV Digital — Advertising Proposal for Little & Holland PLLC",
                      "author": "Swayze Hollingsworth · MCTV Digital",
                      "subject": "Two 15-second commercials on the MCTV indoor screen network"})
    out.save(OUT, garbage=4, deflate=True)
    print("saved", OUT, f"({len(out)} pages)")

if __name__ == "__main__":
    with open(os.path.join(HERE, "copy.json")) as f:
        copy = json.load(f)
    extract_assets()
    render_html(copy)
    print_pdf()
    assemble()
