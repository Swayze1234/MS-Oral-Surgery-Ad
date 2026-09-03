"""
Builds MCTV_Proposal_HOTWORX_Oxford.pdf — an advertising proposal for
HOTWORX Oxford, MS, branded with the HOTWORX and MCTV logos.

Pricing, network stats and the Oxford host-location list are taken from the
MCTV advertiser media kit (build/source/MCTV_Media_Kit_Oxford_original.pdf).
Regular monthly rates only (no seasonal specials).

Run from anywhere:  python3 build/hotworx/build_proposal.py
Requires:  pip install pymupdf playwright   (uses the pre-installed Chromium)
"""
import base64, os, sys, datetime
import fitz  # pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KIT = os.path.join(ROOT, "build", "source", "MCTV_Media_Kit_Oxford_original.pdf")
OUT = os.path.join(ROOT, "MCTV_Proposal_HOTWORX_Oxford.pdf")
HTML_OUT = os.path.join(HERE, "proposal.html")
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

# ------------------------------------------------------------- HTML ---------
CSS = """
@page { size: 13.333in 7.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Liberation Sans', Arial, Helvetica, sans-serif; color: #12213a;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 13.333in; height: 7.5in; position: relative; overflow: hidden;
        page-break-after: always; background: #f6f2e9; padding: 0.55in 0.75in; }
.page:last-child { page-break-after: auto; }
.dark { background: #0b2a5b; color: #fff;
        background-image: radial-gradient(ellipse at 85% 15%, #163d7d 0%, #0b2a5b 45%, #071b3d 100%); }
.serif { font-family: 'DejaVu Serif', 'Liberation Serif', Georgia, serif; font-weight: normal; }
.eyebrow { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #c9962e; font-weight: bold; }
.dark .eyebrow { color: #e8b84b; }
h1.title { font-size: 44px; line-height: 1.08; margin: 8px 0 0; color: #0b2a5b; }
.dark h1.title { color: #fff; }
h1.title .gold { color: #c9962e; } .dark h1.title .gold { color: #e8b84b; }
.rule { width: 64px; height: 3px; background: #e8b84b; margin: 16px 0 22px; }
.hdr { display: flex; justify-content: space-between; align-items: flex-end;
       border-bottom: 1px solid #d9c9a3; padding-bottom: 14px; margin-bottom: 18px; }
.dark .hdr { border-bottom-color: rgba(232,184,75,.45); }
.hdr .section { font-size: 10.5px; letter-spacing: 3px; text-transform: uppercase; color: #6a7891; }
.dark .hdr .section { color: #b8c7de; }
.mctv-navy { height: 46px; } .mctv-white { height: 32px; display: block; }
.mctv-lock { display: flex; flex-direction: column; gap: 6px; align-items: flex-start; }
.mctv-lock img { width: auto; }
.mctv-lock .ea { font-size: 10px; letter-spacing: 5px; color: #e8b84b; font-weight: bold; }
.foot { position: absolute; left: 0.75in; right: 0.75in; bottom: 0.32in; display: flex;
        justify-content: space-between; font-size: 9px; letter-spacing: 2px; color: #6a7891; text-transform: uppercase; }
.dark .foot { color: #b8c7de; }
.hw { display: inline-block; }
.hw svg { display: block; width: 100%; height: auto; }
.hw-card { background: #262626; border-radius: 6px; padding: 14px 22px; display: inline-block; }
p { line-height: 1.5; }
.two { display: grid; grid-template-columns: 1.1fr 1fr; gap: 40px; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.stat { border: 1px solid rgba(232,184,75,.5); border-radius: 4px; padding: 18px 16px; background: rgba(255,255,255,.04); }
.stat .n { font-size: 30px; color: #e8b84b; } .stat .l { font-size: 9.5px; letter-spacing: 2.5px; text-transform: uppercase; color: #dbe6f5; margin-top: 4px; }
.light .stat { background: #fff; border-color: #e0d3b1; } .light .stat .n { color: #0b2a5b; } .light .stat .l { color: #6a7891; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.card { background: #0b2a5b; color: #fff; padding: 22px 20px 18px; position: relative; min-height: 215px;
        background-image: linear-gradient(160deg, #123a7c, #0b2a5b 60%); }
.card.rec { outline: 3px solid #e8b84b; outline-offset: -3px; }
.card .sc { font-size: 10.5px; letter-spacing: 3px; text-transform: uppercase; color: #dbe6f5; }
.card .pr { font-size: 40px; color: #e8b84b; margin: 10px 0 14px; }
.card .pr small { font-size: 15px; color: #dbe6f5; }
.card .row { display: flex; justify-content: space-between; font-size: 12px; color: #dbe6f5; padding: 4px 0; border-top: 1px solid rgba(255,255,255,.12); }
.card .row b { color: #fff; } .card .row .g { color: #e8b84b; font-weight: bold; }
.card .nt { font-style: italic; color: #e8b84b; font-size: 13px; margin-top: 14px; font-family: 'DejaVu Serif', serif; }
.tag { position: absolute; top: 0; right: 0; background: #e8b84b; color: #12213a; font-size: 8.5px; font-weight: bold; letter-spacing: 1.5px; padding: 4px 8px; }
.band { border: 1px solid #c9962e; background: #fbf6e9; padding: 13px 16px; font-size: 13.5px; margin-top: 20px; text-align: center; }
.band b { color: #0b2a5b; } .band .g { color: #c9962e; font-weight: bold; }
.incl { display: flex; gap: 34px; font-size: 12.5px; margin-top: 14px; }
.incl span::before { content: '✓  '; color: #c9962e; font-weight: bold; }
.hosts { columns: 3; column-gap: 28px; font-size: 12px; line-height: 1.7; }
.hosts .grp { break-inside: avoid; margin-bottom: 18px; }
.hosts .gt { font-family: 'DejaVu Serif', serif; font-weight: bold; color: #0b2a5b; letter-spacing: 1.5px; text-transform: uppercase; font-size: 11.5px;
             border-bottom: 2px solid #e8b84b; padding-bottom: 4px; margin-bottom: 7px; display: flex; justify-content: space-between; }
.hosts .gt span { color: #c9962e; }
.bars { margin-top: 6px; }
.bar { display: grid; grid-template-columns: 180px 1fr 70px; align-items: center; gap: 14px; margin: 14px 0; font-size: 13.5px; }
.bar .tr { background: rgba(255,255,255,.12); height: 24px; border-radius: 2px; }
.bar .fl { height: 100%; background: #6f8fbf; border: 1px solid #9fb8dd; }
.bar.me .fl { background: #e8b84b; border-color: #f4d27a; } .bar.me { font-weight: bold; } .bar.me .v { color: #e8b84b; }
.bar .v { font-family: 'DejaVu Serif', serif; font-size: 15px; text-align: right; }
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 16px; }
.step { background: #fff; border-top: 3px solid #e8b84b; padding: 14px 16px; font-size: 12px; }
.step .k { font-family: 'DejaVu Serif', serif; color: #c9962e; font-size: 20px; } .step b { display: block; color: #0b2a5b; margin: 4px 0 4px; font-size: 12.5px; }
table.inv { width: 100%; border-collapse: collapse; font-size: 13px; background: #fff; }
table.inv th { text-align: left; font-size: 9.5px; letter-spacing: 2.5px; text-transform: uppercase; color: #6a7891; padding: 9px 12px; border-bottom: 2px solid #e8b84b; }
table.inv td { padding: 13px 12px; border-bottom: 1px solid #ece3cf; vertical-align: top; }
table.inv td.r, table.inv th.r { text-align: right; font-family: 'DejaVu Serif', serif; font-size: 13px; white-space: nowrap; }
table.inv tr.tot td { background: #0b2a5b; color: #fff; font-weight: bold; border: 0; }
table.inv tr.tot td.r { color: #e8b84b; font-size: 15px; }
.spec { border: 1px solid rgba(255,255,255,.25); background: rgba(255,255,255,.06); padding: 12px 16px; font-size: 11px; line-height: 1.6; }
.cta { background: linear-gradient(90deg, #e8b84b, #d9a63a); color: #12213a; padding: 12px 18px; font-family: 'DejaVu Serif', serif; font-size: 15px; }
/* order form */
.form { font-size: 11.5px; }
.form .lbl { font-size: 8.5px; letter-spacing: 2px; text-transform: uppercase; color: #6a7891; margin-bottom: 2px; }
.form .fld { border-bottom: 1px solid #9aa7bd; height: 24px; margin-bottom: 12px; font-size: 12px; padding-left: 2px; color: #0b2a5b; font-weight: bold; }
.form h3 { font-family: 'DejaVu Serif', serif; font-weight: normal; color: #0b2a5b; font-size: 15px; margin: 0 0 8px; border-bottom: 2px solid #e8b84b; padding-bottom: 4px; }
.box { display: inline-block; width: 10px; height: 10px; border: 1px solid #12213a; vertical-align: -1px; margin-right: 5px; background: #fff; }
.form ul { list-style: none; padding: 0; margin: 0 0 8px; } .form li { margin: 6px 0; }
.fine { font-size: 9px; line-height: 1.5; color: #3f4c62; }
"""

def header(section, dark=False):
    if dark:
        return f'''<div class="hdr"><div class="mctv-lock"><img class="mctv-white" src="{MCTV_WHITE}"><span class="ea">ELITE ADVERTISING</span></div>
                   <span class="section">{section}</span></div>'''
    return f'<div class="hdr"><img class="mctv-navy" src="{MCTV_NAVY}"><span class="section">{section}</span></div>'

def footer(n):
    return f'<div class="foot"><span>{n:02d}</span><span>Proposal for HOTWORX Oxford &nbsp;·&nbsp; MCTV Digital, Inc · The Indoor Billboard Company</span></div>'

pages = []

# 1 — Cover
pages.append(f'''
<section class="page dark" style="padding:0">
  <img src="{COVER_PHOTO}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,18,40,.94) 0%,rgba(6,18,40,.82) 45%,rgba(6,18,40,.35) 100%)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,18,40,.55),rgba(6,18,40,0) 40%,rgba(6,18,40,.6))"></div>
  <div style="position:relative;padding:0.6in 0.85in;height:100%;display:flex;flex-direction:column;justify-content:space-between">
    <div class="mctv-lock"><img class="mctv-white" src="{MCTV_WHITE}" style="height:42px"><span class="ea" style="font-size:12px">ELITE ADVERTISING</span></div>
    <div>
      <div class="eyebrow" style="color:#e8b84b">Advertising Proposal &nbsp;·&nbsp; Oxford, Mississippi</div>
      <h1 class="title serif" style="font-size:58px;margin-top:10px">Prepared for<br><span class="gold">HOTWORX</span> Oxford.</h1>
      <div class="rule"></div>
      <div class="hw-card" style="width:400px"><div class="hw">{HOTWORX_SVG}</div></div>
      <p style="font-size:12px;letter-spacing:3.5px;text-transform:uppercase;color:#dbe6f5;margin:22px 0 0">The Indoor Billboard Company &nbsp;·&nbsp; North Mississippi</p>
    </div>
    <div style="display:flex;justify-content:space-between;font-size:12px;color:#dbe6f5">
      <span><b style="color:#fff">{CONTACT['name']}</b> · {CONTACT['title']} · {CONTACT['email']} · {CONTACT['phone']}</span>
      <span>{DATE} &nbsp;·&nbsp; <span style="color:#e8b84b;font-weight:bold">{CONTACT['web']}</span></span>
    </div>
  </div>
</section>''')

# 2 — The opportunity
pages.append(f'''
<section class="page light">
  {header("The Opportunity")}
  <div class="two">
    <div>
      <div class="eyebrow">Why HOTWORX × MCTV</div>
      <h1 class="title serif">Put HOTWORX in front of Oxford <span class="gold">every 15 minutes.</span></h1>
      <div class="rule"></div>
      <p style="font-size:14px;margin:0 0 12px">HOTWORX's members are already in Oxford's salons, nail studios, wellness clinics, tanning studios, restaurants and rooftop bars. MCTV's indoor billboard screens run in those exact venues — so a custom HOTWORX spot plays on repeat to the people most likely to book a session.</p>
      <p style="font-size:14px;margin:0 0 12px">Your ad shares the screen with no one. It can't be skipped, blocked, or scrolled past — and with 55+ minutes of average dwell time, it's seen again and again during a single visit.</p>
      <p style="font-size:14px;margin:0"><b style="color:#0b2a5b">Ideal messaging:</b> 24-hour access, infrared sauna workouts, new-member and student offers, and the Oxford studio location — refreshed every quarter at no charge.</p>
    </div>
    <div>
      <div class="stats" style="grid-template-columns:repeat(2,1fr)">
        <div class="stat"><div class="n serif">1,500+</div><div class="l">Plays per screen / month</div></div>
        <div class="stat"><div class="n serif">15 min</div><div class="l">Loop · 15–30 sec spot</div></div>
        <div class="stat"><div class="n serif">55+</div><div class="l">Min average dwell</div></div>
        <div class="stat"><div class="n serif">44</div><div class="l">Oxford host venues</div></div>
      </div>
      <div class="steps">
        <div class="step"><div class="k serif">1</div><b>We build your ad</b>Custom HD 15–30 second spot designed by our in-house team. You own it forever.</div>
        <div class="step"><div class="k serif">2</div><b>It runs on repeat</b>Unlimited rotation across your chosen Oxford screens, on a 15-minute loop.</div>
        <div class="step"><div class="k serif">3</div><b>You see the proof</b>Proof-of-play reporting, plus a fresh ad build every quarter.</div>
      </div>
    </div>
  </div>
  {footer(2)}
</section>''')

# 3 — Network & value
bars = "".join(
    f'<div class="bar{" me" if n.startswith("MCTV") else ""}"><span>{n}</span><div class="tr"><div class="fl" style="width:{v/65*100:.1f}%"></div></div><span class="v">${v:g}</span></div>'
    for n, v in CPM)
pages.append(f'''
<section class="page dark">
  {header("The Network & The Value", dark=True)}
  <div class="stats" style="grid-template-columns:repeat(5,1fr);margin-bottom:22px">
    <div class="stat"><div class="n serif">125+</div><div class="l">Digital screens</div></div>
    <div class="stat"><div class="n serif">100+</div><div class="l">Premier venues</div></div>
    <div class="stat"><div class="n serif">1.9M+</div><div class="l">Impressions / mo</div></div>
    <div class="stat"><div class="n serif">55+</div><div class="l">Min avg dwell</div></div>
    <div class="stat"><div class="n serif">3</div><div class="l">Growth markets</div></div>
  </div>
  <div class="eyebrow">Cost per 1,000 impressions</div>
  <h1 class="title serif" style="font-size:36px">Local <span class="gold">CPM</span> comparison.</h1>
  <div class="rule" style="margin-bottom:12px"></div>
  <div class="bars">{bars}</div>
  <p style="font-size:9px;color:#b8c7de;margin-top:10px">*CPM = Cost Per Thousand Impressions. MCTV figure is the network blended average (campaigns priced as low as $1.64 CPM at scale). Comparison figures are typical U.S. local CPM ranges by channel (industry estimates).</p>
  {footer(3)}
</section>''')

# 4 — Oxford host locations
groups = "".join(
    f'<div class="grp"><div class="gt">{g}<span>{len(v)}</span></div>' + "".join(f"<div>{h}</div>" for h in v) + "</div>"
    for g, v in OXFORD_HOSTS.items())
pages.append(f'''
<section class="page light">
  {header("Host Network · Oxford / Lafayette")}
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div>
      <div class="eyebrow">Where your ad runs</div>
      <h1 class="title serif" style="font-size:38px">Oxford host locations. <span class="gold">44 venues.</span></h1>
    </div>
    <div style="font-size:11.5px;color:#3f4c62;max-width:340px;text-align:right;padding-bottom:6px">Every venue below is part of the MCTV network today. Your package can be concentrated on the Oxford screens that best match HOTWORX's members.</div>
  </div>
  <div class="rule" style="margin-bottom:14px"></div>
  <div class="hosts">{groups}</div>
  {footer(4)}
</section>''')

# 5 — Packages & pricing (regular rates)
cards = "".join(f'''
  <div class="card{" rec" if p.get("tag","").startswith("REC") else ""}">
    {f'<div class="tag">{p["tag"]}</div>' if p.get("tag") else ""}
    <div class="sc">{p["screens"]}</div>
    <div class="pr serif">{p["price"]}<small>/mo</small></div>
    <div class="row"><span>Ad Plays / Mo</span><b>{p["plays"]}</b></div>
    <div class="row"><span>Per Screen</span><span class="g serif">{p["per"]}</span></div>
    <div class="nt">{p["note"]}</div>
  </div>''' for p in PACKAGES)
pages.append(f'''
<section class="page light">
  {header("Packages & Pricing")}
  <div class="eyebrow">Monthly network rates · 6-month minimum · volume pricing</div>
  <h1 class="title serif" style="font-size:38px">Choose your <span class="gold">footprint.</span></h1>
  <div class="rule" style="margin-bottom:16px"></div>
  <div class="cards">{cards}</div>
  <div class="band"><b>Pay In Full &amp; Save</b> — Prepay a <span class="g">6-month</span> contract, get your <span class="g">7th month FREE</span> &nbsp;·&nbsp; Prepay <span class="g">12 months</span>, get your <span class="g">13th &amp; 14th months FREE</span>.</div>
  <div class="eyebrow" style="margin-top:16px">Every campaign includes</div>
  <div class="incl"><span>Custom 15–30 Sec Ad Production</span><span>Unlimited Rotation</span><span>Proof-of-Play Reporting</span><span>Quarterly Ad Refresh</span><span>You Own Your Ad Forever</span></div>
  {footer(5)}
</section>''')

# 6 — Next steps / contact
pages.append(f'''
<section class="page dark" style="padding:0">
  <div style="position:absolute;left:0;top:0;width:42%;height:100%">
    <img src="{BACK_PHOTO}" style="width:100%;height:100%;object-fit:cover;object-position:60% 50%">
  </div>
  <div style="position:absolute;left:42%;top:0;right:0;height:100%;padding:0.6in 0.75in;display:flex;flex-direction:column;justify-content:center">
    <div class="hw-card" style="width:330px;margin-bottom:22px"><div class="hw">{HOTWORX_SVG}</div></div>
    <h1 class="title serif" style="font-size:40px">Let's launch <span class="gold">HOTWORX Oxford</span> this month.</h1>
    <div class="rule"></div>
    <div style="font-size:13px;line-height:1.7;margin-bottom:16px">
      <b style="color:#e8b84b">{CONTACT['name']}</b> · {CONTACT['title']} · MCTV Digital<br>
      {CONTACT['email']} &nbsp;·&nbsp; {CONTACT['phone']}<br>{CONTACT['web']}
    </div>
    <div class="cta">Next steps: pick your package → sign the order form → we build your ad → you approve → HOTWORX goes live across Oxford.</div>
    <div class="spec" style="margin-top:16px"><b>Ad Specs &amp; Sizes</b><br>Dimensions: 1920×1080 HD · 16:9 aspect ratio<br>File formats: MP4 video or JPG static · Bitrate 300–700 kb/s · Max file size 20 MB</div>
  </div>
  <div class="foot" style="left:calc(42% + 0.75in)"><span>06</span><span>MCTV Digital, Inc · The Indoor Billboard Company</span></div>
</section>''')

# 7 — Agreement & order form (regular packages only, HOTWORX pre-filled)
pages.append(f'''
<section class="page light form">
  {header("Agreement & Order Form")}
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px">
    <div>
      <h3>Advertiser Information</h3>
      <div class="lbl">Business name</div><div class="fld">HOTWORX Oxford, MS</div>
      <div class="lbl">Contact name</div><div class="fld"></div>
      <div class="lbl">Phone</div><div class="fld"></div>
      <div class="lbl">Email</div><div class="fld"></div>
      <div class="lbl">Billing address</div><div class="fld"></div>
      <div class="lbl">Term (months)</div><div class="fld"></div>
      <div class="lbl">Start date</div><div class="fld"></div>
    </div>
    <div>
      <h3>Select Your Package</h3>
      <ul>
        <li><span class="box"></span>20 Screens — $500/mo</li>
        <li><span class="box"></span>40 Screens — $800/mo &nbsp;<span style="color:#c9962e;font-weight:bold;font-size:9px;letter-spacing:1px">RECOMMENDED</span></li>
        <li><span class="box"></span>80 Screens — $1,400/mo</li>
        <li><span class="box"></span>125+ Screens — $2,000/mo</li>
      </ul>
      <div class="lbl" style="margin-top:8px">Add-ons</div>
      <ul>
        <li><span class="box"></span>Animated Logo — $10/screen/mo + $150 setup</li>
        <li><span class="box"></span>Cause / Organization Sponsorship — $10/screen/mo</li>
      </ul>
      <h3 style="margin-top:12px">Payment Authorization</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
        <div><div class="lbl">Monthly total</div><div class="fld">$</div></div>
        <div><div class="lbl">One-time setup</div><div class="fld">$</div></div>
      </div>
      <div><span class="box"></span>Paid in Full (Prepay) &nbsp;&nbsp; <span class="box"></span>Monthly Billing</div>
      <p class="fine" style="margin:6px 0 0">Prepay bonus: Pay in full on a 6-month term → 7th month FREE. Pay in full on a 12-month term → 13th &amp; 14th months FREE.</p>
    </div>
    <div>
      <h3>Payment Method</h3>
      <div style="margin-bottom:8px"><span class="box"></span>Check &nbsp;&nbsp; <span class="box"></span>Bank Draft (ACH) &nbsp;&nbsp; <span class="box"></span>Credit Card</div>
      <div class="lbl">Name on acct / card</div><div class="fld"></div>
      <div class="lbl">Acct / card number</div><div class="fld"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px">
        <div><div class="lbl">Routing / exp.</div><div class="fld"></div></div>
        <div><div class="lbl">CVV</div><div class="fld"></div></div>
        <div><div class="lbl">Billing zip</div><div class="fld"></div></div>
      </div>
      <p class="fine">I authorize MCTV Digital, Inc. to charge the payment method above according to the plan selected. Billing: upon signing, the first month — or the full amount if paying in full — is billed immediately. For monthly plans, the remaining billing cycle begins 30 days after creative is approved and pushed live. Minimum 90-day term; continues month-to-month thereafter with 30-day written cancellation notice. Setup fees are non-refundable. Each campaign includes a custom ad with a quarterly refresh; additional creative revisions billed at $200/round after three rounds. Pay-in-full bonus: 6-month agreements receive the 7th month free; 12-month agreements receive the 13th and 14th months free.</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">
        <div><div class="fld"></div><div class="lbl">Client signature / date</div></div>
        <div><div class="fld"></div><div class="lbl">Swayze Hollingsworth · MCTV Digital / date</div></div>
      </div>
    </div>
  </div>
  {footer(7)}
</section>''')

html = f"<!doctype html><html><head><meta charset='utf-8'><title>MCTV × HOTWORX Oxford — Advertising Proposal</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
with open(HTML_OUT, "w") as f:
    f.write(html)

# ------------------------------------------------------------- render -------
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    kw = {"args": ["--no-sandbox"]}
    if os.path.exists(CHROME):
        kw["executable_path"] = CHROME
    b = p.chromium.launch(**kw)
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.goto("file://" + HTML_OUT)
    pg.wait_for_load_state("networkidle")
    pg.pdf(path=OUT, width="13.333in", height="7.5in", print_background=True,
           prefer_css_page_size=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    b.close()
print("saved", OUT, f"({os.path.getsize(OUT)/1e6:.1f} MB)")
