"""Builds the Warner Family Dentistry Ad Traction Report as a 16:9 slide deck (HTML + print CSS).

Inputs : agg.json (from agg.py), fonts_inline.css, logofonts_inline.css, deckfonts_inline.css
Optional: photos/cover.jpg  (cover + screen-time photo; a branded gradient is used if missing)
          logos/warner.png, logos/mctv.png (real logo artwork; vector look-alikes are used if missing)
Output : Warner_Family_Dentistry_Traction_Report.html  (render to PDF with headless Chromium)
"""
import json, html, os, base64, mimetypes
from datetime import date

d = json.load(open('agg.json'))
hosts = d['hosts']; versions = d['versions']

SELECTED = {  # client's chosen screens -> host name in the player exports (None = not in the exports)
    '39759 Nutrition': None,
    'Two Brothers': 'Two Brothers Smoked Meats',
    'William Wells': 'William Wells Tire & Auto',
    'Lucky Nails': 'Lucky Nails & Spa',
    'Starkville Veterinary Hospital': 'Starkville Veterinary Hospital',
    'Umi': 'Umi Japanese Steakhouse & Sushi Bar',
    'Legends': 'Legends Hair Salon',
    'MS Asthma': 'Mississippi Asthma & Allergy Clinic, PA - Starkville',
    'Skate Odyssey': 'Skate Odyssey Inc',
    "BJ's Family Pharmacy": "BJ's Family Pharmacy",
}
paid_names = {v for v in SELECTED.values() if v}
DEMO = 'D.476 Dealer Demo'
OFFLINE_NAME = '39759 Nutrition'   # played, but the screen was off Wi-Fi so its player could not report
HEALTHCARE = {"BJ's Family Pharmacy", 'Mississippi Asthma & Allergy Clinic, PA - Starkville',
              'Revive Wellness Clinic - Starkville', 'Right Track Medical Group - Starkville',
              'Starkville Veterinary Hospital'}
CATEGORY = {
    'Two Brothers Smoked Meats': 'Restaurant', 'Uno Mas Tacos y Tequila Starkville': 'Restaurant',
    'Skate Zone': 'Entertainment', "BJ's Family Pharmacy": 'Medical', 'Starkville Parks and Recreation': 'Community',
    'Elm Lake Golf Course': 'Recreation', 'Hobie’s Tiki Dawgs & Daqs': 'Restaurant',
    'Umi Japanese Steakhouse & Sushi Bar': 'Restaurant', 'Mississippi Ice Daiquiri Shop': 'Restaurant',
    'Right Track Medical Group - Starkville': 'Medical', 'Lucky Nails & Spa': 'Salon',
    'Oktibbeha County Co-op': 'Retail', 'Cellars Wine & Spirits': 'Retail', 'Bennett Home Furniture & More': 'Retail',
    'Little Magnolia Gifts & Apparel - Starkville': 'Retail', 'Copy Cow': 'Services', 'starkvegas pawnshop': 'Retail',
    'Mississippi Asthma & Allergy Clinic, PA - Starkville': 'Medical', 'Starkville Veterinary Hospital': 'Medical',
    "Montgomery's Jewelry": 'Retail', 'Skate Odyssey Inc': 'Entertainment', 'William Wells Tire & Auto': 'Auto',
    'Revive Wellness Clinic - Starkville': 'Medical', 'The Breakfast Club': 'Restaurant', 'Legends Hair Salon': 'Salon',
}

def fmt_d(s):
    y, m, dd = s.split('-'); return f"{int(m)}/{int(dd)}/{y}"
def mon(s):
    return date.fromisoformat(s).strftime('%b %Y')
def hrs(sec): return sec / 3600
def n(x): return f"{x:,}"
def short(name): return name.replace(' - Starkville', '').replace(', PA', '').replace(' Starkville', '').replace('starkvegas', 'Starkvegas')

rows = []
for name, h in hosts.items():
    if name == DEMO: continue
    rows.append(dict(name=name, plays=h['plays'], secs=h['secs'], first=h['first'], last=h['last'],
                     paid=name in paid_names, city=h['city'], cat=CATEGORY.get(name, 'General')))
rows.sort(key=lambda r: -r['plays'])
n_screens = len(rows) + 1
tot_plays = sum(r['plays'] for r in rows); tot_secs = sum(r['secs'] for r in rows)
paid_rows = [r for r in rows if r['paid']]; gift_rows = [r for r in rows if not r['paid']]
paid_plays = sum(r['plays'] for r in paid_rows); gift_plays = sum(r['plays'] for r in gift_rows)
first = min(r['first'] for r in rows); last = max(r['last'] for r in rows)
days_on_air = (date.fromisoformat(last) - date.fromisoformat(first)).days + 1
months = 5; spend = 350 * months
cpp = spend / tot_plays * 100
demo = hosts[DEMO]
top = rows[0]
hc_rows = [r for r in rows if r['name'] in HEALTHCARE]; hc_plays = sum(r['plays'] for r in hc_rows)
period = f"{mon(first)} &ndash; {mon(last)}"
period_caps = f"{date.fromisoformat(first).strftime('%b').upper()} &ndash; {date.fromisoformat(last).strftime('%b %Y').upper()}"

# ---------------------------------------------------------------- assets
def data_uri(path):
    mt = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return f"data:{mt};base64,{base64.b64encode(open(path, 'rb').read()).decode()}"
COVER = None
for cand in ('photos/cover.jpg', 'photos/cover.jpeg', 'photos/cover.png', 'photos/cover.webp'):
    if os.path.exists(cand): COVER = data_uri(cand); break
FONTS = open('fonts_inline.css').read() + open('logofonts_inline.css').read() + open('deckfonts_inline.css').read()

TOOTH = '''<svg class="tooth" viewBox="0 0 104 128" aria-hidden="true">
  <g transform="translate(3.5,3.5)" fill="none" stroke="#000" stroke-width="9" stroke-linejoin="round" stroke-linecap="round">
   <path d="M50,14 C33,4 13,12 11,34 C10,50 21,58 24,76 C27,96 31,116 40,118 C48,119 48,98 50,88 C52,98 52,119 60,118 C69,116 73,96 76,76 C79,58 90,50 89,34 C87,12 67,4 50,14 Z"/>
   <path d="M14,30 C6,22 8,6 22,6 C31,6 33,15 27,18" stroke-width="6"/>
  </g>
  <g fill="none" stroke="#2FB4E8" stroke-width="9" stroke-linejoin="round" stroke-linecap="round">
   <path d="M50,14 C33,4 13,12 11,34 C10,50 21,58 24,76 C27,96 31,116 40,118 C48,119 48,98 50,88 C52,98 52,119 60,118 C69,116 73,96 76,76 C79,58 90,50 89,34 C87,12 67,4 50,14 Z"/>
   <path d="M14,30 C6,22 8,6 22,6 C31,6 33,15 27,18" stroke-width="6"/>
  </g>
 </svg>'''
WARNER_SVG = f'''<div class="warner-logo">{TOOTH}
 <div class="warner-text"><div class="warner-name">ARNER</div><div class="warner-sub">FAMILY DENTISTRY</div><div class="warner-spa">&amp; Med Spa</div></div>
</div>'''
def img_or(path, fallback, cls):
    return f'<img class="{cls} real" src="{data_uri(path)}" alt="">' if os.path.exists(path) else fallback
WARNER_LOGO = img_or('logos/warner.png', WARNER_SVG, 'warner-logo')
MCTV_SVG = '<div class="mctv-logo"><div class="mctv-name">MCTV</div><div class="mctv-sub">ELITE ADVERTISING</div></div>'
MCTV_LOGO = img_or('logos/mctv.png', MCTV_SVG, 'mctv-logo')

# ---------------------------------------------------------------- pieces
def chrome(label, right):
    return f'<div class="chrome"><span class="lab">{label}</span><span class="lab muted">{right}</span></div>'

def rank_list(items, maxv):
    out = []
    for i, r in enumerate(items, 1):
        cls = 'sel' if r['paid'] else 'gift'
        meta = f"{r['city']} &middot; {r['cat']}" + ('' if r['paid'] else ' &middot; <em>Gifted</em>')
        out.append(f'<div class="rk"><span class="rk-n">{i:02d}</span><span class="rk-name {cls}">{html.escape(short(r["name"]))}</span>'
                   f'<span class="rk-meta">{meta}</span><span class="rk-bar"><i class="{cls}" style="width:{r["plays"]/maxv*100:.1f}%"></i></span>'
                   f'<span class="rk-val">{n(r["plays"])}</span></div>')
    return '\n'.join(out)

def dir_list(items):
    return '\n'.join(f'<div class="dr"><span>{html.escape(short(r["name"]))}<small>{r["city"]} &middot; {r["cat"]}</small></span><b>{n(r["plays"])}</b></div>' for r in items)

vlabels = {1: 'Original spot', 2: 'Revision 2', 3: 'Revision 3', 4: 'Final spot'}
ver_cards = ''.join(
    f'<div class="vc"><span class="lab">V{v["version"]} &middot; {vlabels[v["version"]].upper()}</span>'
    f'<b>{n(v["plays"]-v["demo_plays"])}</b><span class="sub">{fmt_d(v["first"])} &ndash; {fmt_d(v["last"])}</span></div>'
    for v in versions)

cover_media = (f'<div class="cover-photo" style="background-image:url({COVER})"></div>' if COVER else
               f'<div class="cover-photo placeholder"><div class="ph-mark">{TOOTH}</div></div>')
band_media = (f'<div class="band-photo" style="background-image:url({COVER})"></div>' if COVER else
              '<div class="band-photo placeholder"></div>')

page = f'''<title>Warner Family Dentistry Traction</title>
<style>
{FONTS}
:root{{ --bg:#0b1216; --bg-2:#0f1a20; --fg:#f0f4f6; --fg-2:#b7c4cc; --mute:#7e8f99; --line:rgba(240,244,246,.13); --line-2:rgba(240,244,246,.07);
  --accent:#2FB4E8; --accent-deep:#149BD1; --bar:#1C9DD0; --bar-gift:#CF7F12; --gift:#E8A24A; --track:rgba(240,244,246,.10); }}
*{{box-sizing:border-box}}
body{{margin:0;background:#06090b;color:var(--fg);font-family:"Inter Tight","IBM Plex Sans",system-ui,sans-serif;font-size:14px;line-height:1.45;-webkit-font-smoothing:antialiased}}
.deck{{display:flex;flex-direction:column;align-items:center;gap:22px;padding:22px 12px}}
.slide{{width:960px;height:540px;background:var(--bg);position:relative;overflow:hidden;padding:30px 48px 32px;flex:none;border-radius:4px}}
.lab{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10px;letter-spacing:.26em;text-transform:uppercase;color:var(--accent);font-weight:500}}
.lab.muted{{color:var(--mute)}}
.chrome{{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid var(--line);margin-bottom:22px}}
h1{{font-size:64px;font-weight:600;letter-spacing:-.035em;line-height:1;margin:14px 0 16px}}
h2{{font-size:30px;font-weight:600;letter-spacing:-.025em;line-height:1.1;margin:0 0 6px}}
h3{{font-size:17px;font-weight:600;letter-spacing:-.01em;margin:6px 0 4px}}
p{{margin:0;color:var(--fg-2);font-size:13.5px;line-height:1.5}}
.slide .big{{color:var(--fg);font-size:108px;font-weight:600;letter-spacing:-.045em;line-height:.95;font-variant-numeric:tabular-nums;margin:0}}
.slide .big.md{{font-size:84px}}
.mono{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}}
.foot{{position:absolute;left:48px;right:48px;bottom:22px;display:flex;justify-content:space-between;align-items:center}}
.foot .lab{{color:var(--mute)}}
.hl{{color:var(--accent)}} .gl{{color:var(--gift)}}
em{{font-style:normal;color:var(--gift)}}

/* logos */
.warner-logo{{display:flex;align-items:center;gap:2px}} .warner-logo .tooth{{height:54px;width:auto;margin-right:-5px}}
.warner-text{{line-height:1}}
.warner-name{{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:29px;letter-spacing:.06em;color:#2FB4E8;text-shadow:1.5px 1.5px 0 #000;line-height:.9}}
.warner-sub{{font-family:"Josefin Sans",sans-serif;font-size:9.5px;letter-spacing:.2em;color:var(--fg);margin:4px 0 0 2px}}
.warner-spa{{font-family:"Great Vibes",cursive;font-size:16px;color:#2FB4E8;text-shadow:1px 1px 0 #000;text-align:right;line-height:1}}
img.warner-logo.real{{height:56px;width:auto;max-width:240px;object-fit:contain}}
.mctv-logo{{text-align:center;line-height:1}} .mctv-name{{font-family:"Bodoni Moda",Georgia,serif;font-size:26px;letter-spacing:.34em;color:var(--fg);padding-left:.34em}}
.mctv-sub{{font-family:"Josefin Sans",sans-serif;font-size:7.5px;letter-spacing:.32em;color:var(--fg-2);padding-left:.32em;margin-top:4px}}
img.mctv-logo.real{{height:40px;width:auto;object-fit:contain;filter:invert(1) brightness(1.4)}}
.small-logo .warner-logo .tooth{{height:38px}} .small-logo .warner-name{{font-size:20px}} .small-logo .warner-sub{{font-size:7px}} .small-logo .warner-spa{{font-size:12px}} .small-logo img.warner-logo.real{{height:40px}}

/* cover */
.cover{{padding:0;display:grid;grid-template-columns:1.05fr 1fr}}
.cover-l{{padding:34px 40px 34px 48px;display:flex;flex-direction:column}}
.cover-l .title{{margin-top:auto}}
.cover-l h1{{font-size:56px}}
.cover-l p{{font-size:15px;max-width:38ch}}
.cover-meta{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;border-top:1px solid var(--line);padding-top:16px;margin-top:38px}}
.cover-meta b{{display:block;font-weight:500;font-size:13px;margin-top:6px;color:var(--fg)}}
.cover-photo{{background-size:cover;background-position:center;position:relative}}
.cover-photo:after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--bg) 0%,rgba(11,18,22,0) 22%)}}
.cover-photo.placeholder{{background:radial-gradient(120% 90% at 80% 20%,#1a6f92 0%,#0f3a4d 45%,#0b1216 100%);display:flex;align-items:center;justify-content:center}}
.cover-photo.placeholder .tooth{{height:260px;opacity:.9}}

/* glance */
.glance{{display:grid;grid-template-columns:1.6fr 1fr;gap:40px;align-items:end;margin-bottom:26px}}
.glance p{{font-size:14px;max-width:34ch}}
.tiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:0 28px}}
.tile{{border-top:1px solid var(--line);padding:16px 0 18px}}
.tile b{{display:block;font-size:30px;font-weight:600;letter-spacing:-.03em;line-height:1;margin-bottom:8px;font-variant-numeric:tabular-nums}}
.tile b.gl{{color:var(--gift)}}
.tile .lab{{color:var(--mute);letter-spacing:.2em}}

/* gifted */
.gift-grid{{display:grid;grid-template-columns:1fr 1.15fr;gap:44px;align-items:start}}
.split{{display:flex;height:18px;border-radius:3px;overflow:hidden;margin:20px 0 10px;gap:2px}}
.split i{{display:block;height:100%}} .split .s{{background:var(--bar)}} .split .g{{background:var(--bar-gift)}}
.key{{display:flex;justify-content:space-between;font-size:12.5px;color:var(--fg-2)}} .key b{{color:var(--fg);font-weight:500}}
.key i{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:7px;vertical-align:-1px}}
.gift-cols{{display:grid;grid-template-columns:1fr 1fr;gap:0 28px;margin-top:6px}}
.dr{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:6px 0;border-bottom:1px solid var(--line-2);font-size:12.5px}}
.dr span{{color:var(--fg)}} .dr small{{display:block;color:var(--mute);font-size:10.5px}} .dr b{{font-family:"IBM Plex Mono",monospace;font-weight:400;color:var(--fg-2);font-variant-numeric:tabular-nums;font-size:12px}}
.dr.off b{{font-size:10.5px;color:var(--mute)}}

/* band */
.band{{padding:0}}
.band-top{{padding:44px 48px 36px;display:grid;grid-template-columns:1.4fr 1fr;gap:40px;align-items:end;height:300px}}
.band-top p{{font-size:13.5px;max-width:34ch}}
.band-photo{{height:240px;background-size:cover;background-position:center 60%;position:relative}}
.band-photo:before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,var(--bg) 0%,rgba(11,18,22,0) 60%)}}
.band-photo.placeholder{{background:linear-gradient(180deg,#0b1216 0%,#0f3a4d 60%,#1a6f92 100%)}}

/* rank */
.rk{{display:grid;grid-template-columns:26px 236px 176px 1fr 74px;align-items:center;gap:14px;padding:6px 0;border-bottom:1px solid var(--line-2);font-size:13px}}
.rk-n{{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--mute)}}
.rk-name{{font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}} .rk-name.sel{{color:var(--accent)}}
.rk-meta{{font-size:11px;color:var(--mute);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.rk-bar{{height:7px;background:var(--track);border-radius:2px;overflow:hidden}} .rk-bar i{{display:block;height:100%;background:var(--bar);border-radius:2px}} .rk-bar i.gift{{background:var(--bar-gift)}}
.rk-val{{font-family:"IBM Plex Mono",monospace;font-size:12px;text-align:right;color:var(--fg);font-variant-numeric:tabular-nums}}
.legend{{display:flex;gap:18px;font-size:11px;color:var(--mute);margin-top:10px}} .legend i{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px;vertical-align:-1px}}

/* directory */
.dir{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0 30px}}
.dir .span2{{grid-column:2/4}}
.dir .dr{{padding:3px 0;font-size:11.5px;line-height:1.3}} .dir .dr small{{font-size:9.5px}}
.dir-head h2{{margin-bottom:0}} .dir .lab{{margin-bottom:4px!important}}
.dir-head{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}}
.dir-head h2{{font-size:24px}} .dir-head .lab{{color:var(--mute)}}

/* versions */
.vcs{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:10px}}
.vc{{border-top:2px solid var(--accent-deep);padding-top:14px}}
.vc b{{display:block;font-size:40px;font-weight:600;letter-spacing:-.035em;line-height:1;margin:14px 0 8px;font-variant-numeric:tabular-nums}}
.vc .sub{{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--mute)}}
.vline{{position:relative;height:2px;background:var(--line);margin:26px 0 22px}}
.vline i{{position:absolute;top:-4px;width:10px;height:10px;border-radius:50%;background:var(--accent)}}

/* observations */
.obs{{display:grid;grid-template-columns:1fr 1fr;gap:26px 44px}}
.ob{{border-top:1px solid var(--line);padding-top:14px}}
.ob .lab{{letter-spacing:.22em}}
.obs-foot{{border-top:1px solid var(--line);margin-top:26px;padding-top:14px}}

/* contact */
.team{{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:26px}}
.tm{{border-top:1px solid var(--line);padding-top:14px}}
.tm h3{{margin:0 0 6px;font-size:18px}} .tm .lab{{letter-spacing:.2em}} .tm p{{margin-top:12px;font-size:13px;color:var(--fg)}}

@media print{{
  @page{{size:10in 5.625in;margin:0}}
  body{{background:var(--bg)}}
  .deck{{display:block;padding:0;gap:0}}
  .slide{{width:10in;height:5.625in;border-radius:0;break-after:page;page-break-after:always}}
  .slide:last-child{{break-after:auto;page-break-after:auto}}
}}
</style>
<div class="deck">

<!-- 1 · cover -->
<section class="slide cover">
  <div class="cover-l">
    {WARNER_LOGO}
    <div class="title">
      <span class="lab">Prepared for Warner Family Dentistry &amp; Med Spa</span>
      <h1>Ad Traction Report</h1>
      <p>Indoor digital billboard performance across the Starkville MCTV network, {fmt_d(first)} through {fmt_d(last)}.</p>
    </div>
    <div class="cover-meta">
      <div><span class="lab muted">Period</span><b>{period}</b></div>
      <div><span class="lab muted">Network</span><b>{n_screens} screens</b></div>
      <div><span class="lab muted">Prepared by</span><b>MCTV Elite Advertising</b></div>
    </div>
  </div>
  {cover_media}
</section>

<!-- 2 · glance -->
<section class="slide">
  {chrome('Campaign at a glance', period_caps)}
  <div class="glance">
    <div><p class="big">{n(tot_plays)}</p><span class="lab" style="display:block;margin-top:10px">Total ad plays</span></div>
    <p>Warner Family Dentistry ran on {n_screens} screens across Starkville for five consecutive months, on a plan that paid for 10.</p>
  </div>
  <div class="tiles">
    <div class="tile"><b>{n_screens}</b><span class="lab">Screens reached</span></div>
    <div class="tile"><b>{hrs(tot_secs):,.0f}</b><span class="lab">Hours of screen time</span></div>
    <div class="tile"><b>{days_on_air}</b><span class="lab">Days on air</span></div>
    <div class="tile"><b>{cpp:.1f}&cent;</b><span class="lab">Cost per play</span></div>
    <div class="tile"><b>10</b><span class="lab">Selected screens</span></div>
    <div class="tile"><b class="gl">{len(gift_rows)}</b><span class="lab">Gifted screens</span></div>
    <div class="tile"><b>{n(round(tot_plays/len(rows)))}</b><span class="lab">Avg. plays per screen</span></div>
    <div class="tile"><b>{len(versions)}</b><span class="lab">Versions of the spot</span></div>
  </div>
</section>

<!-- 3 · gifted -->
<section class="slide">
  {chrome('Gifted screens', 'No charge to Warner')}
  <div class="gift-grid">
    <div>
      <h2><span class="gl">{len(gift_rows)} extra screens</span><br>at no charge</h2>
      <p>Warner Family Dentistry paid for 10 screens at $350 a month. MCTV also ran the spot on {len(gift_rows)} additional Starkville-area locations for free.</p>
      <div class="split"><i class="s" style="width:{paid_plays/tot_plays*100:.1f}%"></i><i class="g" style="width:{gift_plays/tot_plays*100:.1f}%"></i></div>
      <div class="key"><span><i style="background:var(--bar)"></i>Selected screens <b>{n(paid_plays)}</b></span><span><i style="background:var(--bar-gift)"></i>Gifted screens <b>{n(gift_plays)}</b></span></div>
      <p style="margin-top:22px"><b class="gl">{gift_plays/tot_plays*100:.0f}%</b> of every play Warner received came from screens they did not pay for, including {short(gift_rows[0]['name'])}, the busiest gifted screen at {n(gift_rows[0]['plays'])} plays.</p>
    </div>
    <div>
      <span class="lab muted" style="display:block;margin-bottom:6px">Gifted screens &middot; sorted by plays</span>
      <div class="gift-cols"><div>{dir_list(gift_rows[:8])}</div><div>{dir_list(gift_rows[8:])}</div></div>
    </div>
  </div>
</section>

<!-- 4 · screen time band -->
<section class="slide band">
  <div class="band-top">
    <div><span class="lab">Total screen time</span><p class="big md" style="margin-top:12px">{hrs(tot_secs):,.0f} hours</p></div>
    <p>The equivalent of {hrs(tot_secs)/24:.0f} continuous days on screen, in the dining rooms, waiting rooms, salons and shops of Starkville, where nobody is scrolling past.</p>
  </div>
  {band_media}
</section>

<!-- 5 · top screens -->
<section class="slide">
  {chrome('Top screens', 'Ranked by ad plays')}
  <h2>Ten highest-volume screens</h2>
  <div style="margin-top:14px">{rank_list(rows[:10], rows[0]['plays'])}</div>
  <div class="legend"><span><i style="background:var(--bar)"></i>Selected screen (paid)</span><span><i style="background:var(--bar-gift)"></i>Gifted screen (no charge)</span></div>
</section>

<!-- 6 · directory -->
<section class="slide">
  {chrome('Screen directory', f'{n_screens} screens &middot; sorted by plays')}
  <div class="dir">
    <div>
      <div class="dir-head"><h2>Selected screens</h2></div>
      <span class="lab" style="display:block;margin-bottom:6px">10 screens &middot; {n(paid_plays)} plays</span>
      {dir_list(paid_rows)}
      <div class="dr off"><span>{OFFLINE_NAME}<small>Starkville &middot; Played, screen offline from Wi-Fi so no counts reported</small></span><b>not reported</b></div>
    </div>
    <div class="span2">
      <div class="dir-head"><h2>Gifted screens</h2></div>
      <span class="lab" style="display:block;margin-bottom:6px;color:var(--gift)">{len(gift_rows)} screens &middot; {n(gift_plays)} plays &middot; no charge</span>
      <div class="dir" style="grid-template-columns:1fr 1fr">
        <div>{dir_list(gift_rows[:8])}</div><div>{dir_list(gift_rows[8:])}</div>
      </div>
    </div>
  </div>
</section>

<!-- 7 · versions -->
<section class="slide">
  {chrome('The creative', period_caps)}
  <h2>Four versions of the spot</h2>
  <p style="max-width:60ch">The 30-second spot was refined three times before settling on the final cut. Every version is counted in this report.</p>
  <div class="vline"><i style="left:0%"></i><i style="left:33%"></i><i style="left:66%"></i><i style="left:calc(100% - 10px)"></i></div>
  <div class="vcs">{ver_cards}</div>
  <div class="foot"><span class="lab">Plays exclude {n(demo['plays'])} airings on MCTV's internal demo player</span><span class="lab">Source: MCTV player reports FS_1 &ndash; FS_4</span></div>
</section>

<!-- 8 · observations -->
<section class="slide">
  {chrome('Observations', period_caps)}
  <h2>What this means for Warner</h2>
  <div class="obs" style="margin-top:18px">
    <div class="ob"><span class="lab">Gifted reach</span><h3>{gift_plays/tot_plays*100:.0f}% of plays came free</h3><p>{n(gift_plays)} plays across {len(gift_rows)} screens MCTV added at no charge, more than doubling the footprint of the 10-screen plan.</p></div>
    <div class="ob"><span class="lab">Top screen</span><h3>{short(top['name'])} carried {top['plays']/tot_plays*100:.0f}% alone</h3><p>{n(top['plays'])} plays and {hrs(top['secs']):,.0f} hours of screen time in one of Starkville's busiest dining rooms.</p></div>
    <div class="ob"><span class="lab">Healthcare placement</span><h3>{n(hc_plays)} plays in clinical settings</h3><p>{len(hc_rows)} pharmacy, clinic and veterinary waiting rooms, including BJ's Family Pharmacy and Mississippi Asthma &amp; Allergy, where health is already the subject.</p></div>
    <div class="ob"><span class="lab">Value</span><h3>About {cpp:.1f}&cent; per play</h3><p>${spend:,} over five months bought {n(tot_plays)} plays and {hrs(tot_secs):,.0f} hours on screen, roughly {n(round(tot_plays/len(rows)))} plays per reporting screen.</p></div>
  </div>
  <div class="obs-foot"><p>{OFFLINE_NAME}, a selected screen, ran the spot but was disconnected from Wi-Fi during the period, so its player could not report play counts. Its plays are real and are not included in any figure above.</p></div>
</section>

<!-- 9 · contact -->
<section class="slide">
  {chrome('Contact', 'mctvofms.com')}
  <h2>Your MCTV team</h2>
  <p style="max-width:62ch">Granular per-location data, including air time and play counts by screen, is available on request.</p>
  <div class="team">
    <div class="tm"><h3>T. Creed Cannon</h3><span class="lab">Owner / Managing Partner</span><p>(601) 201-8202<br>creed@mctvofms.com</p></div>
    <div class="tm"><h3>Mary Michael Cannon</h3><span class="lab">Owner / Managing Partner</span><p>(662) 801-5677<br>mmc@mctvofms.com</p></div>
    <div class="tm"><h3>Swayze Hollingsworth</h3><span class="lab">Director of Sales</span><p>(662) 907-0404<br>swayze@mctvofms.com</p></div>
  </div>
  <div class="foot small-logo">{WARNER_LOGO}<span class="lab">MCTV Elite Advertising &middot; North Mississippi</span></div>
</section>

</div>
'''
out = 'Warner_Family_Dentistry_Traction_Report.html'
open(out, 'w').write(page.encode('ascii', 'xmlcharrefreplace').decode('ascii'))
print('wrote', out, dict(tot_plays=tot_plays, screens=n_screens, gift=len(gift_rows), gift_plays=gift_plays, hc_plays=hc_plays, cover='photo' if COVER else 'placeholder'))
