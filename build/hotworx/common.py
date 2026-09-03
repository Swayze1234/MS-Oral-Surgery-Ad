"""Shared assets and data for the HOTWORX Oxford proposals (landscape + portrait)."""
import base64, os, datetime
import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KIT = os.path.join(ROOT, "build", "source", "MCTV_Media_Kit_Oxford_original.pdf")
CHROME = os.environ.get("CHROME_PATH",
         "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

# ---------------------------------------------------------------- assets ----
def kit_image(xref):
    """Pull an embedded image out of the media kit as a data URI (keeps alpha)."""
    doc = fitz.open(KIT)
    pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4:            # CMYK -> RGB
        pix = fitz.Pixmap(fitz.csRGB, pix)
    smask = doc.extract_image(xref).get("smask", 0)
    if smask:                             # merge the /SMask so logos stay transparent
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
    return "data:image/png;base64," + base64.b64encode(pix.tobytes("png")).decode()

MCTV_WHITE = kit_image(84)   # white 'MCTV' wordmark (cover / dark pages)
MCTV_NAVY  = kit_image(86)   # navy 'MCTV · ELITE ADVERTISING' lockup (light pages)
COVER_PHOTO = kit_image(83)  # Oxford stadium, night
BACK_PHOTO  = kit_image(414) # Oxford water tower

# HOTWORX wordmark, recreated as vector art from the supplied logo
# (gradient H, flame-O, T · white WORX · ® · tagline).
HOTWORX_SVG = """
<svg viewBox="0 0 1240 330" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HOTWORX 24 Hour Infrared Fitness Studio">
  <defs>
    <linearGradient id="hwfire" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#E4232B"/><stop offset="0.55" stop-color="#F26522"/><stop offset="1" stop-color="#FBA21B"/>
    </linearGradient>
    <linearGradient id="hwflame" x1="0.3" y1="1" x2="0.7" y2="0">
      <stop offset="0" stop-color="#E4232B"/><stop offset="0.5" stop-color="#F26522"/><stop offset="1" stop-color="#FCB040"/>
    </linearGradient>
  </defs>
  <g font-family="'DejaVu Sans','Liberation Sans',Arial,sans-serif" font-weight="bold" font-size="196" letter-spacing="-6">
    <text x="10" y="210" fill="url(#hwfire)">H</text>
    <text x="365" y="210" fill="url(#hwfire)">T</text>
    <text x="500" y="210" fill="#FFFFFF">WORX</text>
  </g>
  <!-- flame O -->
  <path transform="translate(259,150) scale(1.12) translate(-259,-150)" fill="url(#hwflame)" fill-rule="evenodd"
        d="M262 20 C 238 60, 178 82, 178 146 C 178 192, 216 218, 258 218 C 306 218, 340 186, 340 140 C 340 118, 330 100, 318 88 C 322 106, 314 122, 302 128 C 310 100, 296 78, 280 66 C 286 88, 276 104, 264 110 C 276 78, 274 46, 262 20 Z
           M259 108 C 240 124, 226 138, 226 156 C 226 174, 240 186, 258 186 C 278 186, 292 172, 292 156 C 292 142, 282 130, 274 124 C 276 138, 268 146, 260 148 C 266 132, 264 118, 259 108 Z"/>
  <circle cx="332" cy="42" r="22" fill="#E4232B"/>
  <circle cx="332" cy="42" r="22" fill="none" stroke="#F26522" stroke-width="4"/>
  <circle cx="1190" cy="200" r="16" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <text x="1190" y="208" fill="#FFFFFF" font-family="'Liberation Sans',Arial,sans-serif" font-weight="bold" font-size="20" text-anchor="middle">R</text>
  <text x="620" y="300" fill="#FFFFFF" text-anchor="middle" font-family="'Liberation Sans',Arial,sans-serif" font-weight="bold" font-size="46" letter-spacing="6">24 HOUR INFRARED FITNESS STUDIO</text>
</svg>
"""

# ------------------------------------------------------------ content -------
CONTACT = dict(name="Swayze Hollingsworth", title="Director of Sales",
               email="swayze@mctvofms.com", phone="662-907-0404",
               web="www.mctvofms.com")
DATE = datetime.date.today().strftime("%B %Y")

# Regular monthly network rates (6-month minimum) — from the media kit.
PACKAGES = [
    dict(screens="20 Screens",   price="$500",   plays="30K",   per="$25",    note="Entry network reach"),
    dict(screens="40 Screens",   price="$800",   plays="60K",   per="$20",    note="Market saturation", tag="RECOMMENDED FOR HOTWORX"),
    dict(screens="80 Screens",   price="$1,400", plays="120K",  per="$17.50", note="Deep saturation"),
    dict(screens="125+ Screens", price="$2,000", plays="187.5K",per="$16",    note="Entire network", tag="BEST VALUE"),
]

# All 44 Oxford / Lafayette host locations from the media kit, grouped.
OXFORD_HOSTS = {
    "Fitness, Wellness & Medical": [
        "Built Different Fitness", "Rebel Body Fitness", "Revive Wellness of Oxford",
        "Internal Medicine Associates of Oxford", "Mississippi Asthma & Allergy Clinic, P.A.",
        "Oxford Dental", "RedMed Urgent Clinic of Oxford - Jackson Ave",
        "Right Track Medical Group - Oxford", "The Children's Dental Center",
    ],
    "Beauty & Personal Care": [
        "Amara Salon & Aesthetics", "Element Hair Studio", "Luxe Styling Studio",
        "Nail E!", "Nail Thology", "Oxford Super Tan",
    ],
    "Restaurants & Bars": [
        "B's Hickory Smoke BBQ", "Bep Haus", "Booth's Barbeque and Yard",
        "Casa Mexicana of Oxford", "El Charro Cocina & Cantina", "Finch & Kelly",
        "LandShark Seafood & Catfish", "Rafters Music and Food", "Rebel Yell Rooftop Bar",
        "Rosati's Pizza", "Sip Oxford", "The Blind Pig Pub", "The Oxford Growler",
        "The Velvet Ditch - Sports Bar & Seafood", "Uno Mas Tacos y Tequila Jackson Ave",
    ],
    "Retail, Auto & Everyday Stops": [
        "4 Corner's Chevron (Chicken On A Stick)", "Cannon Chevrolet Buick Cadillac of Oxford",
        "Cannon Collision Center", "James Food Center Post Office", "Magnolia Wine & Spirits",
        "MARATHON South Lamar", "Oxford T-Shirt Co.", "Party in the Sip", "Rainbow Cleaners",
        "Southern Coop", "Stouts Carpet & Flooring", "Texaco Lamar Express",
    ],
    "Community": [
        "Oxford Park Commission", "Oxford-Lafayette County Chamber of Commerce",
    ],
}
assert sum(len(v) for v in OXFORD_HOSTS.values()) == 44

CPM = [("Magazine", 65), ("Television", 35), ("Radio", 27), ("Social Media", 19.51),
       ("Outdoor Billboards", 6), ("MCTV Indoor Network", 2.63)]

