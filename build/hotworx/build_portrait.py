"""
Builds MCTV_Proposal_HOTWORX_Oxford_Letter.pdf — a 3-page US Letter (portrait)
advertising proposal for HOTWORX Oxford, in the same style as the Parlor 1858
one-pager (Playfair Display + Inter, navy/gold, white paper, navy footer).

Regular media-kit pricing only. Includes all 44 Oxford host venues.
Run:  python3 build/hotworx/build_portrait.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = os.path.join(ROOT, "MCTV_Proposal_HOTWORX_Oxford_Letter.pdf")
HTML_OUT = os.path.join(HERE, "proposal_letter.html")
FONTS = open(os.path.join(HERE, "fonts", "embedded.css")).read()

CSS = """
:root{ --navy:#13203a; --navy2:#1c2f57; --gold:#e8b84b; --gold-d:#c79a3b; --gold-ink:#9a6a12;
       --slate:#6a7891; --line:#dfe5ee; --paper:#fff; --soft:#f5f7fb; --ink:#2b3752; }
@page{ size: Letter; margin:0; }
*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; background:#fff; }
body{ font-family:'Inter','Liberation Sans',Arial,sans-serif; color:var(--navy); font-size:10.5pt; line-height:1.45;
      -webkit-print-color-adjust:exact; print-color-adjust:exact; font-variant-numeric:lining-nums; }
.serif{ font-family:'Playfair Display','DejaVu Serif',serif; }
.page{ width:8.5in; height:11in; background:var(--paper); position:relative; overflow:hidden; page-break-after:always; display:flex; flex-direction:column; }
.page:last-child{ page-break-after:auto; }
.brandbar{ padding:0.42in 0.7in 0.22in; display:flex; align-items:center; justify-content:space-between; }
.brandbar .x{ font-family:'Playfair Display',serif; color:var(--gold-d); font-size:26pt; }
.brandbar .mctv{ height:0.66in; display:block; }
.hw-card{ background:#262626; border-radius:6px; padding:12px 20px; width:2.9in; }
.hw-card svg{ display:block; width:100%; height:auto; }
.rule{ height:3px; background:linear-gradient(90deg,var(--gold),var(--gold-d)); margin:0 0.7in; }
.kicker{ font-size:7.5pt; letter-spacing:0.28em; text-transform:uppercase; color:var(--gold-ink); font-weight:600; }
h1{ margin:6px 0 8px; font-size:26pt; line-height:1.12; font-weight:500; color:var(--navy); }
h1 em, h2 em{ font-style:normal; color:var(--gold-d); }
h2{ font-family:'Playfair Display',serif; font-weight:500; font-size:17pt; margin:6px 0 10px; color:var(--navy); }
.lead{ font-size:10.3pt; color:#33415c; margin:0; }
.content{ padding:0.24in 0.7in 0; flex:1; min-height:0; overflow:hidden; }
.page3 .content{ padding-top:0.24in; }
.page3 .tbl{ font-size:9.4pt; } .page3 .tbl td{ padding:7px 0; }
.page3 .choice{ font-size:9pt; } .page3 .fields div{ margin-top:20px; } .page3 .sig div{ margin-top:30px; } .page3 .fine{ font-size:7.4pt; }
.stats{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:18px 0 0; }
.stat{ border-top:2px solid var(--gold); padding-top:6px; }
.stat b{ display:block; font-family:'Playfair Display',serif; font-size:18pt; font-weight:500; line-height:1.1; }
.stat span{ font-size:7.5pt; letter-spacing:0.16em; text-transform:uppercase; color:var(--slate); }
/* package cards */
.options{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:16px; }
.card{ border:1px solid var(--line); border-radius:6px; overflow:hidden; background:#fff; position:relative; display:flex; flex-direction:column; }
.card .top{ background:var(--navy); color:#fff; padding:12px 12px 11px; }
.card.best{ border:2px solid var(--gold); box-shadow:0 6px 18px rgba(19,32,58,.12); }
.card.best .top{ background:linear-gradient(135deg,var(--navy),var(--navy2)); }
.card .opt{ font-size:7pt; letter-spacing:0.22em; text-transform:uppercase; color:var(--gold); font-weight:600; }
.card .price{ font-family:'Playfair Display',serif; font-size:22pt; font-weight:500; line-height:1; color:var(--gold); margin-top:8px; }
.card .price small{ font-family:'Inter',sans-serif; font-size:7.5pt; color:#cfe0f5; letter-spacing:0.08em; margin-left:4px; }
.card .sub{ font-size:7.8pt; color:#bcd2ec; margin-top:6px; font-style:italic; }
.badge{ position:absolute; top:0; right:0; background:var(--gold); color:var(--navy); font-size:6.3pt; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; padding:3px 8px; border-radius:0 0 0 4px; }
.card.tagged .top{ padding-top:24px; }
.card .body{ padding:12px 12px; flex:1; font-size:8.8pt; color:var(--ink); }
.card .row{ display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--line); }
.card .row:last-child{ border-bottom:0; }
.card .row b{ color:var(--navy); }
.card .row .g{ color:var(--gold-d); font-weight:700; }
.note{ background:var(--soft); border-left:3px solid var(--gold); padding:11px 14px; font-size:9.3pt; color:var(--ink); margin-top:14px; }
.note b{ color:var(--navy); }
.incl{ display:flex; justify-content:space-between; gap:8px; margin-top:18px; font-size:8.8pt; color:var(--ink); }
.incl span::before{ content:'✓ '; color:var(--gold-d); font-weight:700; }
/* footer */
.foot{ margin-top:auto; flex:none; background:var(--navy); color:#fff; padding:12px 0.7in; display:flex; align-items:center; justify-content:space-between; font-size:8.5pt; }
.foot .who b{ display:block; font-family:'Playfair Display',serif; font-size:12pt; font-weight:500; }
.foot .who i{ font-style:normal; color:var(--gold); letter-spacing:0.16em; text-transform:uppercase; font-size:7pt; }
.foot .who span{ display:block; color:#cfe0f5; margin-top:2px; }
.foot .co{ text-align:right; color:#bcd2ec; font-size:7.5pt; letter-spacing:0.14em; text-transform:uppercase; line-height:1.6; }
.foot .co b{ color:#fff; font-family:'Playfair Display',serif; letter-spacing:0.3em; font-size:11pt; font-weight:400; display:block; }
/* page 2 */
.two{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }
.steps{ counter-reset:s; list-style:none; margin:0; padding:0; }
.steps li{ counter-increment:s; position:relative; padding-left:34px; margin:0 0 7px; font-size:8.6pt; color:var(--ink); }
.steps li::before{ content:counter(s,decimal-leading-zero); position:absolute; left:0; top:-1px; font-family:'Playfair Display',serif; font-size:15pt; color:var(--gold-d); }
.steps b{ color:var(--navy); display:block; font-weight:600; }
.hosts{ columns:3; column-gap:18px; font-size:8.1pt; line-height:1.5; color:var(--ink); }
.grp{ break-inside:avoid; margin-bottom:11px; }
.gt{ font-family:'Playfair Display',serif; font-weight:600; color:var(--navy); font-size:8pt; letter-spacing:0.04em; text-transform:uppercase;
     border-bottom:2px solid var(--gold); padding-bottom:3px; margin-bottom:5px; display:flex; justify-content:space-between; }
.gt span{ color:var(--gold-d); }
.cpm{ margin-top:6px; }
.cpm .bar{ display:grid; grid-template-columns:120px 1fr 46px; gap:10px; align-items:center; font-size:8.2pt; margin:4px 0; color:var(--ink); }
.cpm .tr{ background:var(--soft); height:12px; border-radius:2px; } .cpm .fl{ height:100%; background:#8fa6cc; }
.cpm .me{ font-weight:700; color:var(--navy); } .cpm .me .fl{ background:var(--gold); } .cpm .me .v{ color:var(--gold-ink); }
.cpm .v{ text-align:right; font-family:'Playfair Display',serif; }
/* page 3 */
.addons{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:4px; }
.addon{ border:1px solid var(--line); border-radius:6px; padding:8px 14px; font-size:8.6pt; color:var(--ink); }
.addon b.t{ display:block; font-family:'Playfair Display',serif; font-weight:500; color:var(--navy); font-size:13pt; margin-bottom:4px; }
.addon .p{ font-family:'Playfair Display',serif; color:var(--gold-d); font-size:15pt; margin-top:6px; }
.addon .p small{ font-family:'Inter',sans-serif; font-size:7.5pt; color:var(--slate); letter-spacing:0.08em; }
.tbl{ width:100%; border-collapse:collapse; font-size:8.6pt; margin-top:4px; }
.tbl th{ text-align:left; font-size:7.5pt; letter-spacing:0.2em; text-transform:uppercase; color:var(--gold-ink); padding:0 0 6px; border-bottom:1px solid var(--line); }
.tbl td{ padding:3.5px 0; border-bottom:1px solid var(--line); vertical-align:top; color:var(--ink); }
.tbl td:first-child{ color:var(--navy); font-weight:600; }
.tbl td.c, .tbl th.c{ text-align:center; }
.tbl td.c{ color:var(--gold-d); font-weight:700; }
.tbl td.c.no{ color:#c4cbd6; font-weight:400; }
.accept{ margin-top:22px; border:1px solid var(--line); border-radius:6px; padding:14px 20px 12px; }
.choose{ display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:10px; margin:8px 0 10px; }
.choice{ display:flex; gap:7px; align-items:flex-start; font-size:8.4pt; color:var(--ink); }
.choice.rec{ background:var(--soft); border:1px solid var(--gold); border-radius:4px; padding:7px; margin:-7px -8px; }
.choice b{ display:block; color:var(--navy); } .choice b em{ font-style:normal; color:var(--gold-ink); font-size:6.5pt; letter-spacing:0.14em; text-transform:uppercase; margin-left:4px; }
.box{ width:13px; height:13px; border:1.5px solid var(--navy); border-radius:2px; flex:none; margin-top:2px; }
.fields{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px; margin-top:6px; }
.fields div{ border-bottom:1px solid var(--navy); padding-bottom:3px; font-size:6.8pt; letter-spacing:0.16em; text-transform:uppercase; color:var(--slate); margin-top:12px; }
.fields div.f{ color:var(--navy); font-weight:700; font-size:9pt; letter-spacing:0; text-transform:none; }
.sig{ display:grid; grid-template-columns:1fr 1fr; gap:26px; margin-top:4px; }
.sig div{ border-top:1px solid var(--navy); padding-top:4px; font-size:7pt; letter-spacing:0.16em; text-transform:uppercase; color:var(--slate); margin-top:20px; }
.fine{ font-size:6.9pt; color:var(--slate); margin:8px 0 0; line-height:1.4; }
"""

def brandbar(small=False):
    return f'''<div class="brandbar"{' style="padding-top:0.34in;padding-bottom:0.14in"' if small else ''}>
      <div class="hw-card"{' style="width:2.4in"' if small else ''}>{HOTWORX_SVG}</div>
      {'' if small else '<div class="x">&times;</div>'}
      <img class="mctv" src="{MCTV_NAVY}" alt="MCTV Elite Advertising"{' style="height:0.55in"' if small else ''}>
    </div><div class="rule"></div>'''

FOOT = f'''<div class="foot">
    <div class="who"><b>{CONTACT['name']}</b><i>{CONTACT['title']} · MCTV Digital</i>
      <span>{CONTACT['email']} &nbsp;·&nbsp; {CONTACT['phone']} &nbsp;·&nbsp; {CONTACT['web']}</span></div>
    <div class="co"><b>MCTV</b>The Indoor Billboard Company<br>North Mississippi</div>
  </div>'''

cards = "".join(f'''
  <div class="card{' best' if p.get('tag','').startswith('REC') else ''}{' tagged' if p.get('tag') else ''}">
    {f'<div class="badge">{"Recommended" if p["tag"].startswith("REC") else p["tag"].title()}</div>' if p.get('tag') else ''}
    <div class="top"><div class="opt">{p['screens']}</div>
      <div class="price">{p['price']}<small>/ MO</small></div><div class="sub">{p['note']}</div></div>
    <div class="body">
      <div class="row"><span>Ad plays / mo</span><b>{p['plays']}</b></div>
      <div class="row"><span>Per screen</span><span class="g">{p['per']}</span></div>
      <div class="row"><span>Custom ad</span><b>Included</b></div>
    </div>
  </div>''' for p in PACKAGES)

page1 = f'''
<section class="page">
  {brandbar()}
  <div class="content">
    <div class="kicker">Advertising Proposal &nbsp;·&nbsp; Oxford, Mississippi</div>
    <h1 class="serif">Your brand on repeat.<br>In front of <em>all of Oxford.</em></h1>
    <p class="lead">MCTV runs high-definition indoor billboard screens inside the salons, wellness clinics, restaurants, bars and everyday stops Oxford already visits. We design a custom 15–30 second HOTWORX spot, then play it on a 15-minute loop across the screens you choose — unskippable, unblockable, impossible to scroll past. Pick your footprint below.</p>
    <div class="stats">
      <div class="stat"><b>125+</b><span>Digital screens</span></div>
      <div class="stat"><b>44</b><span>Oxford host venues</span></div>
      <div class="stat"><b>1,500+</b><span>Plays per screen / mo</span></div>
      <div class="stat"><b>55+</b><span>Min average dwell</span></div>
    </div>
    <div class="kicker" style="margin-top:24px">Monthly network rates &nbsp;·&nbsp; 6-month minimum &nbsp;·&nbsp; volume pricing</div>
    <div class="options" style="margin-top:8px">{cards}</div>
    <div class="note"><b>Why we recommend 40 screens.</b> Oxford has 44 MCTV host venues. A 40-screen footprint saturates the market — HOTWORX shows up in nearly every waiting room, salon chair and bar stool in town — for $20 per screen, and every package includes a custom ad refreshed each quarter.</div>
    <div class="note" style="background:#fbf6e9;border-color:var(--gold-d)"><b>Pay in full &amp; save.</b> Prepay a 6-month contract and get your 7th month free. Prepay 12 months and get your 13th &amp; 14th months free.</div>
    <div class="incl"><span>Custom 15–30 sec ad production</span><span>Unlimited rotation</span><span>Proof-of-play reporting</span><span>Quarterly ad refresh</span><span>You own your ad forever</span></div>
  </div>
  {FOOT}
</section>'''

HOST_GROUPS = {g.replace("Fitness, Wellness & Medical","Fitness & Medical").replace("Retail, Auto & Everyday Stops","Retail & Everyday Stops"): v for g, v in OXFORD_HOSTS.items()}
groups = "".join(f'<div class="grp"><div class="gt">{g}<span>{len(v)}</span></div>' + "".join(f"<div>{h}</div>" for h in v) + "</div>"
                 for g, v in HOST_GROUPS.items())
bars = "".join(f'<div class="bar{" me" if n.startswith("MCTV") else ""}"><span>{n}</span><div class="tr"><div class="fl" style="width:{v/65*100:.0f}%"></div></div><span class="v">${v:g}</span></div>' for n, v in [(n.replace("MCTV Indoor Network","MCTV Network"), v) for n, v in CPM])
page2 = f'''
<section class="page">
  {brandbar(small=True)}
  <div class="content">
    <div class="kicker">Where your ad runs</div>
    <h2 style="font-size:18pt;margin-top:2px">Oxford host locations. <em>44 venues.</em></h2>
    <p class="lead" style="font-size:9pt;margin-bottom:10px">Every venue below carries MCTV screens today. Your package is concentrated on the Oxford screens that best match HOTWORX's members.</p>
    <div class="hosts">{groups}</div>
    <div class="two" style="margin-top:6px">
      <div>
        <div class="kicker">Cost per 1,000 impressions</div>
        <h2 style="font-size:14pt;margin-bottom:4px">Local CPM comparison.</h2>
        <div class="cpm">{bars}</div>
        <p class="fine" style="margin-top:6px">MCTV figure is the network blended average (as low as $1.64 CPM at scale). Comparison figures are typical U.S. local CPM ranges by channel.</p>
      </div>
      <div>
        <div class="kicker">How it works</div>
        <h2 style="font-size:14pt;margin-bottom:8px">Four steps to launch.</h2>
        <ol class="steps">
          <li><b>Pick your package.</b> Check a box on page 3 and sign.</li>
          <li><b>We build your ad.</b> Send your logo, photos and offer; we design a 15–30 second HD spot for approval.</li>
          <li><b>You go live.</b> HOTWORX enters the Oxford loop, 1,500+ plays per screen every month.</li>
          <li><b>We keep it fresh.</b> Proof-of-play reporting, plus a new ad build every quarter at no charge.</li>
        </ol>
      </div>
    </div>
  </div>
  {FOOT}
</section>'''

page3 = f'''
<section class="page page3">
  {brandbar(small=True)}
  <div class="content">
    <div class="kicker">Side by side</div>
    <h2 style="margin-bottom:6px">What each package includes.</h2>
    <table class="tbl">
      <tr><th></th><th class="c">20</th><th class="c" style="color:var(--navy)">40 ★</th><th class="c">80</th><th class="c">125+</th></tr>
      <tr><td>Monthly investment</td><td class="c" style="color:var(--navy)">$500</td><td class="c" style="color:var(--navy)">$800</td><td class="c" style="color:var(--navy)">$1,400</td><td class="c" style="color:var(--navy)">$2,000</td></tr>
      <tr><td>Ad plays per month</td><td class="c">30K</td><td class="c">60K</td><td class="c">120K</td><td class="c">187.5K</td></tr>
      <tr><td>Cost per screen</td><td class="c">$25</td><td class="c">$20</td><td class="c">$17.50</td><td class="c">$16</td></tr>
      <tr><td>Custom ad, quarterly refresh, unlimited rotation &amp; reporting</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td></tr>
      <tr><td>You own your ad forever</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td></tr>
      <tr><td>Prepay 6 months → 7th month free · 12 months → 13th &amp; 14th free</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td></tr>
    </table>

    <div class="accept">
      <div class="kicker">Agreement &amp; order form</div>
      <h2 style="margin-top:4px;margin-bottom:8px">Select your package.</h2>
      <div class="choose">
        <div class="choice"><div class="box"></div><div><b>20 Screens · $500/mo</b>Entry network reach.</div></div>
        <div class="choice rec"><div class="box"></div><div><b>40 Screens · $800/mo <em>Recommended</em></b>Oxford market saturation.</div></div>
        <div class="choice"><div class="box"></div><div><b>80 Screens · $1,400/mo</b>Deep saturation.</div></div>
        <div class="choice"><div class="box"></div><div><b>125+ Screens · $2,000/mo</b>Entire network.</div></div>
      </div>
      <div class="kicker" style="margin-top:4px">Billing</div>
      <div style="display:flex;gap:40px;font-size:8.8pt;color:var(--ink);margin-top:4px">
        <div class="choice"><div class="box"></div><div>Paid in full (prepay)</div></div>
        <div class="choice"><div class="box"></div><div>Monthly billing</div></div>
      </div>
      <div class="fields">
        <div class="f">HOTWORX Oxford, MS</div><div>&nbsp;</div><div>&nbsp;</div>
      </div>
      <div class="fields" style="margin-top:0">
        <div style="margin-top:2px;border:0">Business name</div><div style="margin-top:2px;border:0">Contact name &amp; title</div><div style="margin-top:2px;border:0">Phone &amp; email</div>
      </div>
      <div class="fields" style="margin-top:0">
        <div>&nbsp;</div><div>&nbsp;</div><div>&nbsp;</div>
      </div>
      <div class="fields" style="margin-top:0">
        <div style="margin-top:2px;border:0">Term (months) &amp; start date</div><div style="margin-top:2px;border:0">Monthly total</div><div style="margin-top:2px;border:0">Billing address</div>
      </div>
      <div class="sig">
        <div>HOTWORX Oxford · Signature / Date</div>
        <div>Swayze Hollingsworth · MCTV Digital / Date</div>
      </div>
      <p class="fine">Upon signing, the first month (or the full amount if prepaying) is billed immediately; monthly billing then begins 30 days after creative is approved and live. Minimum 90-day term, then month-to-month with 30-day written notice. Creative revisions beyond three rounds billed at $200/round. Prepay bonus: 6-month term → 7th month free; 12-month term → 13th &amp; 14th months free.</p>
    </div>
  </div>
  {FOOT}
</section>'''

html = f"<!doctype html><html><head><meta charset='utf-8'><title>HOTWORX Oxford × MCTV — Advertising Proposal</title><style>{FONTS}</style><style>{CSS}</style></head><body>{page1}{page2}{page3}</body></html>"
open(HTML_OUT, "w").write(html)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    kw = {"args": ["--no-sandbox"]}
    if os.path.exists(CHROME): kw["executable_path"] = CHROME
    b = p.chromium.launch(**kw)
    pg = b.new_page(viewport={"width": 816, "height": 1056})
    pg.goto("file://" + HTML_OUT); pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    pg.pdf(path=OUT, format="Letter", print_background=True, prefer_css_page_size=True)
    b.close()
print("saved", OUT, f"({os.path.getsize(OUT)/1e6:.1f} MB)")
