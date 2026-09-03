import json, html, os, base64
from datetime import date

d = json.load(open('agg.json'))
hosts = d['hosts']; versions = d['versions']

SELECTED = {  # client's chosen screens -> matching host name in reports (None = not in the exports)
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
OFFLINE_NAME = '39759 Nutrition'   # played but disconnected from Wi-Fi, so no counts reported

def fmt_d(s):
    y, m, dd = s.split('-'); return f"{int(m)}/{int(dd)}/{y}"
def hrs(sec): return sec / 3600
def n(x): return f"{x:,}"

rows = []
for name, h in hosts.items():
    if name == DEMO: continue
    rows.append(dict(name=name, plays=h['plays'], secs=h['secs'], first=h['first'], last=h['last'],
                     paid=name in paid_names, city=h['city']))
rows.sort(key=lambda r: -r['plays'])
n_screens = len(rows) + 1
tot_plays = sum(r['plays'] for r in rows); tot_secs = sum(r['secs'] for r in rows)
paid_rows = [r for r in rows if r['paid']]; gift_rows = [r for r in rows if not r['paid']]
paid_plays = sum(r['plays'] for r in paid_rows); gift_plays = sum(r['plays'] for r in gift_rows)
first = min(r['first'] for r in rows); last = max(r['last'] for r in rows)
months = 5; spend = 350 * months
cpp = spend / tot_plays * 100
demo = hosts[DEMO]

# ---------------------------------------------------------------- chart: plays by screen
LW, BW, RH, PADT = 250, 520, 24, 6
H = PADT * 2 + RH * (len(rows) + 1)
def x(v): return LW + v / 20000 * BW
svg = [f'<svg class="bars" viewBox="0 0 {LW+BW+70} {H+28}" role="img" aria-label="Plays per screen, all four ad versions combined">']
for t in (0, 5000, 10000, 15000, 20000):
    svg.append(f'<line class="grid" x1="{x(t):.1f}" y1="{PADT}" x2="{x(t):.1f}" y2="{H}"/>')
    svg.append(f'<text class="tick" x="{x(t):.1f}" y="{H+18}" text-anchor="middle">{n(t)}</text>')
for i, r in enumerate(rows):
    y = PADT + i * RH; bh = 16; by = y + (RH - bh) / 2
    w = max(2, (r['plays'] / 20000) * BW)
    cls = 'paid' if r['paid'] else 'gift'
    label = r['name'].replace(' - Starkville', '').replace(', PA', '')
    svg.append(f'<g class="row" data-name="{html.escape(r["name"])}" data-plays="{r["plays"]}" data-hours="{hrs(r["secs"]):.1f}" '
               f'data-kind="{"Selected screen" if r["paid"] else "Gifted screen"}" data-range="{fmt_d(r["first"])} &ndash; {fmt_d(r["last"])}">')
    svg.append(f'<rect class="hit" x="0" y="{y}" width="{LW+BW+70}" height="{RH}"/>')
    svg.append(f'<text class="lbl" x="{LW-12}" y="{y+RH/2+4}" text-anchor="end">{html.escape(label)}</text>')
    svg.append(f'<path class="bar {cls}" d="M{LW},{by} h{w-4:.1f} a4,4 0 0 1 4,4 v{bh-8} a4,4 0 0 1 -4,4 h-{w-4:.1f} z"/>')
    svg.append(f'<text class="val" x="{LW+w+8:.1f}" y="{y+RH/2+4}">{n(r["plays"])}</text>')
    svg.append('</g>')
y = PADT + len(rows) * RH
svg.append(f'<g class="row" data-name="{OFFLINE_NAME}" data-plays="0" data-hours="0" data-kind="Selected screen" data-range="Played, not reported (screen offline from Wi-Fi)">'
           f'<rect class="hit" x="0" y="{y}" width="{LW+BW+70}" height="{RH}"/>')
svg.append(f'<text class="lbl" x="{LW-12}" y="{y+RH/2+4}" text-anchor="end">{OFFLINE_NAME}</text>')
svg.append(f'<rect class="bar paid nodata" x="{LW}" y="{y+(RH-16)/2}" width="4" height="16"/>')
svg.append(f'<text class="val muted" x="{LW+12}" y="{y+RH/2+4}">played, not reported*</text></g>')
svg.append('</svg>')
svg = '\n'.join(svg)

# ---------------------------------------------------------------- table
def trow(r):
    badge = '<span class="badge paid">Selected</span>' if r['paid'] else '<span class="badge gift">Gifted</span>'
    return (f'<tr class="{"" if r["paid"] else "gift-row"}"><td>{html.escape(r["name"])}<span class="city">{r["city"]}</span></td>'
            f'<td>{badge}</td><td class="num">{n(r["plays"])}</td><td class="num">{hrs(r["secs"]):.1f}</td>'
            f'<td class="dates">{fmt_d(r["first"])} &ndash; {fmt_d(r["last"])}</td></tr>')
table_rows = '\n'.join(trow(r) for r in rows)
table_rows += (f'<tr><td>{OFFLINE_NAME}<span class="city">Starkville</span></td><td><span class="badge paid">Selected</span></td>'
               f'<td class="num muted">not reported*</td><td class="num muted">&mdash;</td><td class="dates muted">Played, no play data*</td></tr>')

# ---------------------------------------------------------------- versions
vlabels = {1: 'Original spot', 2: 'Revision 2', 3: 'Revision 3', 4: 'Final spot'}
vrows = ''
for v in versions:
    p = v['plays'] - v['demo_plays']
    vrows += (f'<div class="ver"><div class="ver-dot"></div><div class="ver-n">v{v["version"]}</div>'
              f'<div class="ver-title">{vlabels[v["version"]]}</div><div class="ver-meta">{fmt_d(v["first"])} &ndash; {fmt_d(v["last"])}</div>'
              f'<div class="ver-plays">{n(p)}<span>plays</span></div></div>')

# ---------------------------------------------------------------- logos
FONTS = open('fonts_inline.css').read() + open('logofonts_inline.css').read()
def img_or(path, fallback, cls):
    if os.path.exists(path):
        b = base64.b64encode(open(path, 'rb').read()).decode()
        return f'<img class="{cls} real" src="data:image/png;base64,{b}" alt="">'
    return fallback
TOOTH = '''<svg class="tooth" viewBox="0 0 104 128" aria-hidden="true">
  <g transform="translate(3.5,3.5)" fill="none" stroke="#111" stroke-width="9" stroke-linejoin="round" stroke-linecap="round">
   <path d="M50,14 C33,4 13,12 11,34 C10,50 21,58 24,76 C27,96 31,116 40,118 C48,119 48,98 50,88 C52,98 52,119 60,118 C69,116 73,96 76,76 C79,58 90,50 89,34 C87,12 67,4 50,14 Z"/>
   <path d="M14,30 C6,22 8,6 22,6 C31,6 33,15 27,18" stroke-width="6"/>
  </g>
  <g fill="none" stroke="#149BD1" stroke-width="9" stroke-linejoin="round" stroke-linecap="round">
   <path d="M50,14 C33,4 13,12 11,34 C10,50 21,58 24,76 C27,96 31,116 40,118 C48,119 48,98 50,88 C52,98 52,119 60,118 C69,116 73,96 76,76 C79,58 90,50 89,34 C87,12 67,4 50,14 Z"/>
   <path d="M14,30 C6,22 8,6 22,6 C31,6 33,15 27,18" stroke-width="6"/>
  </g>
 </svg>'''
WARNER_SVG = f'''<div class="warner-logo">{TOOTH}
 <div class="warner-text"><div class="warner-name">ARNER</div><div class="warner-sub">FAMILY DENTISTRY</div><div class="warner-spa">&amp; Med Spa</div></div>
</div>'''
MCTV_SVG = '<div class="mctv-logo"><div class="mctv-name">MCTV</div><div class="mctv-sub">ELITE ADVERTISING</div></div>'
WARNER_LOGO = img_or('logos/warner.png', WARNER_SVG, 'warner-logo')
MCTV_LOGO = img_or('logos/mctv.png', MCTV_SVG, 'mctv-logo')

# ---------------------------------------------------------------- page
page = f'''<title>Warner Family Dentistry Traction</title>
<style>
{FONTS}
:root{{
  --ground:#F4F8FB; --paper:#FFFFFF; --ink:#111417; --ink-2:#4A5560; --ink-3:#7C8994;
  --rule:#D9E3EA; --rule-soft:#EAF1F5;
  --blue:#149BD1; --blue-deep:#0B6C99; --blue-wash:#E3F3FB; --blue-tint:#F1F9FD;
  --black:#111417;
  --amber:#CC7A0E; --amber-ink:#8F5407; --amber-wash:#FBF0DF;
  --grid:#E1EAF0;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{
  --ground:#0E1419; --paper:#161D24; --ink:#EEF3F6; --ink-2:#B5C1CB; --ink-3:#8494A1;
  --rule:#2A3640; --rule-soft:#202A33;
  --blue:#1C9DD0; --blue-deep:#7CCBEF; --blue-wash:#143446; --blue-tint:#122733;
  --black:#0A0D10;
  --amber:#CF7F12; --amber-ink:#F0B461; --amber-wash:#3D2C14;
  --grid:#25313B;
}}}}
:root[data-theme="dark"]{{
  --ground:#0E1419; --paper:#161D24; --ink:#EEF3F6; --ink-2:#B5C1CB; --ink-3:#8494A1;
  --rule:#2A3640; --rule-soft:#202A33;
  --blue:#1C9DD0; --blue-deep:#7CCBEF; --blue-wash:#143446; --blue-tint:#122733;
  --black:#0A0D10;
  --amber:#CF7F12; --amber-ink:#F0B461; --amber-wash:#3D2C14;
  --grid:#25313B;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}}
h1,h2,.stat b,.hero-num,.ver-plays,.ver-n,.gifted .big{{font-family:"Bricolage Grotesque","IBM Plex Sans",system-ui,sans-serif}}
.eyebrow{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue-deep);font-weight:600}}

/* running header / footer: repeat on every printed page via table thead/tfoot */
.sheet{{width:100%;border-collapse:collapse}}
.sheet>thead>tr>td,.sheet>tbody>tr>td,.sheet>tfoot>tr>td{{padding:0}}
.runhead{{display:flex;justify-content:space-between;align-items:center;padding:14px 0 10px;border-bottom:3px solid var(--blue);max-width:860px;margin:0 auto;width:100%}}
.runhead .rh-l{{display:flex;align-items:center;gap:10px;font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:15px;letter-spacing:.05em;color:var(--ink)}}
.runhead .rh-l .tooth{{height:26px;width:auto}}
.runhead .rh-l small{{font-family:"Josefin Sans",sans-serif;font-weight:400;font-size:9.5px;letter-spacing:.2em;color:var(--ink-2);display:block;margin-top:2px}}
.runhead .rh-r{{font-family:"Bodoni Moda",Georgia,serif;font-size:17px;letter-spacing:.3em;color:var(--ink);text-align:right}}
.runhead .rh-r small{{display:block;font-family:"Josefin Sans",sans-serif;font-size:8.5px;letter-spacing:.28em;color:var(--ink-3);margin-top:3px}}
.runfoot{{display:flex;justify-content:space-between;gap:16px;font-size:11px;color:var(--ink-3);padding:10px 0 0;border-top:1px solid var(--rule);max-width:860px;margin:0 auto;width:100%}}
.runfoot b{{color:var(--ink-2);font-weight:600}}
.runfoot i{{display:inline-block;width:8px;height:8px;border-radius:2px;background:var(--blue);vertical-align:-1px;margin-right:6px}}

.page{{max-width:860px;margin:0 auto;padding:0 0 28px}}
.wrap{{padding:0 28px}}

/* cover */
.brandbar{{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:28px 0 20px}}
.brandbar img.real{{height:68px;width:auto;max-width:300px;object-fit:contain}}
.warner-logo{{display:flex;align-items:center;gap:2px}}
.warner-logo .tooth{{height:70px;width:auto;margin-right:-6px}}
.warner-text{{line-height:1}}
.warner-name{{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:38px;letter-spacing:.06em;color:#149BD1;text-shadow:2px 2px 0 #111;line-height:.9}}
.warner-sub{{font-family:"Josefin Sans","IBM Plex Sans",sans-serif;font-size:12px;letter-spacing:.2em;color:var(--ink);margin:5px 0 0 2px}}
.warner-spa{{font-family:"Great Vibes",cursive;font-size:21px;color:#149BD1;text-shadow:1.5px 1.5px 0 #111;text-align:right;margin-top:-1px;line-height:1}}
.mctv-logo{{text-align:center;line-height:1}}
.mctv-name{{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;font-size:38px;letter-spacing:.34em;color:var(--ink);padding-left:.34em}}
.mctv-sub{{font-family:"Josefin Sans","IBM Plex Sans",sans-serif;font-size:10.5px;letter-spacing:.32em;color:var(--ink-2);padding-left:.32em;margin-top:6px}}

.titleblock{{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end;padding:6px 0 22px}}
h1{{font-size:42px;line-height:1;margin:6px 0 0;font-weight:800;letter-spacing:-.02em;text-wrap:balance}}
h1 small{{display:block;font-size:16px;font-weight:500;letter-spacing:0;color:var(--ink-2);margin-top:10px}}
.meta{{text-align:right;font-size:12.5px;color:var(--ink-2);line-height:1.7;border-right:3px solid var(--blue);padding-right:14px}}
.meta b{{color:var(--ink);font-weight:600}}

.hero{{display:grid;grid-template-columns:1.25fr 1fr 1fr 1fr;background:linear-gradient(135deg,var(--blue-deep) 0%,var(--blue) 70%,#3DB3E3 100%);color:#fff;border-radius:10px;overflow:hidden;box-shadow:0 10px 30px -14px rgba(11,108,153,.55)}}
.hero>div{{padding:22px 22px 20px;border-right:1px solid rgba(255,255,255,.22)}}
.hero>div:last-child{{border-right:0}}
.hero .eyebrow{{color:rgba(255,255,255,.82)}}
.hero .hero-num{{display:block;font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1;margin:8px 0 6px;font-variant-numeric:tabular-nums}}
.hero b{{display:block;font-size:30px;font-weight:700;letter-spacing:-.02em;line-height:1.05;margin:10px 0 6px;font-variant-numeric:tabular-nums}}
.hero span{{font-size:12.5px;color:rgba(255,255,255,.85)}}

.lede{{font-size:15.5px;max-width:66ch;color:var(--ink-2);margin:22px 0 0}}
.lede strong{{color:var(--ink);font-weight:600}}

.gifted{{margin:20px 0 0;display:grid;grid-template-columns:auto 1fr;gap:0;border-radius:10px;overflow:hidden;border:1px solid color-mix(in srgb,var(--amber) 35%,transparent);background:var(--paper)}}
.gifted .big{{background:var(--amber);color:#fff;font-size:40px;font-weight:800;letter-spacing:-.02em;line-height:1;padding:18px 22px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px}}
.gifted .big small{{font-family:"IBM Plex Sans",sans-serif;font-size:10px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;opacity:.9}}
.gifted p{{margin:0;padding:16px 20px;font-size:14px;color:var(--ink);align-self:center}}
.gifted p b{{font-weight:600}}
.gifted .amt{{color:var(--amber-ink);font-weight:700}}

.split{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px}}
.card{{background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:16px 18px}}
.card .eyebrow{{margin-bottom:8px}}
.share{{height:14px;border-radius:7px;overflow:hidden;display:flex;background:var(--rule-soft);margin:8px 0 8px}}
.share i{{display:block;height:100%}}
.share .p{{background:var(--blue)}} .share .g{{background:var(--amber);margin-left:2px}}
.share-key{{display:flex;justify-content:space-between;font-size:12.5px;color:var(--ink-2)}}
.share-key b{{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}}
.share-key i{{display:inline-block;width:10px;height:10px;border-radius:3px;vertical-align:-1px;margin-right:6px}}
.share-note{{margin:12px 0 0;font-size:13px;color:var(--ink-2);line-height:1.55}} .share-note b{{color:var(--ink);font-weight:600}}
.kv{{display:grid;grid-template-columns:1fr auto;gap:4px 14px;font-size:13px;color:var(--ink-2)}}
.kv b{{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums;text-align:right}}
.kv div{{padding:5px 0;border-bottom:1px solid var(--rule-soft)}}
.kv div:nth-last-child(-n+2){{border-bottom:0}}

/* sections */
section{{margin-top:34px}}
.sec-head{{display:flex;align-items:baseline;gap:14px;margin:0 0 6px}}
.sec-num{{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:13px;color:#fff;background:var(--blue);border-radius:6px;padding:3px 8px;letter-spacing:.04em}}
h2{{font-size:24px;font-weight:800;letter-spacing:-.015em;margin:0}}
.sub{{color:var(--ink-2);margin:0 0 14px;font-size:13.5px;max-width:74ch}}
.legend{{display:flex;gap:18px;font-size:12.5px;color:var(--ink-2);margin:0 0 8px}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:6px}}
.legend .p i{{background:var(--blue)}} .legend .g i{{background:var(--amber)}}
.chart{{background:var(--paper);border:1px solid var(--rule);border-top:4px solid var(--blue);border-radius:10px;padding:14px 10px 6px;position:relative;overflow-x:auto}}
svg.bars{{width:100%;height:auto;display:block;font-family:"IBM Plex Sans",sans-serif}}
.bars .grid{{stroke:var(--grid);stroke-width:1}}
.bars .tick{{font-size:11px;fill:var(--ink-3);font-variant-numeric:tabular-nums}}
.bars .lbl{{font-size:12px;fill:var(--ink)}}
.bars .val{{font-size:11.5px;fill:var(--ink-2);font-variant-numeric:tabular-nums}}
.bars .val.muted{{fill:var(--ink-3);font-style:italic}}
.bars .bar.paid{{fill:var(--blue)}} .bars .bar.gift{{fill:var(--amber)}} .bars .bar.nodata{{opacity:.35}}
.bars .hit{{fill:transparent}}
.bars .row:hover .hit{{fill:var(--blue-tint)}}
.tip{{position:absolute;pointer-events:none;background:var(--black);color:#fff;font-size:12px;padding:8px 10px;border-radius:6px;line-height:1.4;box-shadow:0 4px 14px rgba(0,0,0,.18);max-width:240px;z-index:2}}
.tip b{{display:block;font-weight:600;margin-bottom:2px}}
.fn{{font-size:11.5px;color:var(--ink-3);margin:10px 0 0;max-width:80ch}}

table.data{{width:100%;border-collapse:separate;border-spacing:0;background:var(--paper);border:1px solid var(--rule);border-radius:10px;overflow:hidden;font-size:13px}}
table.data thead th{{text-align:left;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#fff;font-weight:600;padding:11px 12px;background:var(--black)}}
table.data thead th.num{{text-align:right}}
table.data td{{padding:8px 12px;border-bottom:1px solid var(--rule-soft);vertical-align:middle}}
table.data tbody tr:last-child td{{border-bottom:0}}
td .city{{display:block;font-size:11.5px;color:var(--ink-3)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
td.muted,.dates.muted{{color:var(--ink-3);font-style:italic}}
.dates{{white-space:nowrap;color:var(--ink-2);font-variant-numeric:tabular-nums}}
tr.gift-row td{{background:color-mix(in srgb,var(--amber-wash) 45%,var(--paper))}}
.badge{{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.04em;padding:2px 9px;border-radius:999px;white-space:nowrap}}
.badge.gift{{background:var(--amber-wash);color:var(--amber-ink)}}
.badge.paid{{background:var(--blue);color:#fff}}
table.data tfoot td{{font-weight:600;border-top:2px solid var(--blue);background:var(--blue-tint)}}
.tablewrap{{overflow-x:auto}}

.vers{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;position:relative;padding-top:14px}}
.vers:before{{content:"";position:absolute;left:4%;right:4%;top:19px;height:3px;background:var(--blue);border-radius:2px}}
.ver{{background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:22px 14px 14px;position:relative;text-align:center}}
.ver-dot{{position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:14px;height:14px;border-radius:50%;background:var(--blue);border:3px solid var(--ground)}}
.ver-n{{display:inline-block;font-size:12px;font-weight:800;color:var(--blue-deep);background:var(--blue-wash);border-radius:4px;padding:2px 8px}}
.ver-title{{font-weight:600;font-size:13.5px;margin-top:8px}}
.ver-meta{{font-size:11.5px;color:var(--ink-3);font-variant-numeric:tabular-nums;margin-top:2px}}
.ver-plays{{font-size:26px;font-weight:800;letter-spacing:-.02em;font-variant-numeric:tabular-nums;margin-top:8px;line-height:1}}
.ver-plays span{{font-family:"IBM Plex Sans",sans-serif;font-size:11px;font-weight:400;color:var(--ink-3);margin-left:5px;letter-spacing:0}}

.closing{{margin-top:26px;background:var(--black);color:#fff;border-radius:10px;padding:20px 24px;display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center}}
.closing h3{{margin:0 0 4px;font-family:"Bricolage Grotesque",sans-serif;font-size:19px;font-weight:800;letter-spacing:-.01em}}
.closing p{{margin:0;font-size:13px;color:rgba(255,255,255,.78);max-width:56ch}}
.closing .who{{text-align:right;font-size:13px;line-height:1.6;border-left:3px solid var(--blue);padding-left:16px}}
.closing .who b{{display:block;font-size:14.5px}}

@media (max-width:640px){{ .hero,.vers{{grid-template-columns:repeat(2,1fr)}} .hero>div{{border-bottom:1px solid rgba(255,255,255,.22)}} .split{{grid-template-columns:1fr}} .titleblock{{grid-template-columns:1fr}} .meta{{text-align:left;border-right:0;border-left:3px solid var(--blue);padding:0 0 0 14px}} .closing{{grid-template-columns:1fr}} .closing .who{{text-align:left}} .vers:before{{display:none}} .brandbar{{flex-wrap:wrap}} }}

@media print{{
  @page{{size:letter;margin:.4in .5in .45in}}
  :root{{--ground:#fff}}
  body{{font-size:12.5px}}
  .sheet>thead{{display:table-header-group}} .sheet>tfoot{{display:table-footer-group}}
  .runhead{{padding:6px 0 8px;max-width:none}} .runfoot{{max-width:none;padding-top:8px}}
  .page{{max-width:none;padding:0}} .wrap{{padding:0}}
  .brandbar{{padding:18px 0 14px}}
  section{{margin-top:22px}}
  .chart,.hero,.gifted,.card,.ver,.closing,table.data{{break-inside:avoid;box-shadow:none}}
  section.chart-sec,section.tbl{{break-before:page}}
  h2,.sub,.legend,.sec-head{{break-after:avoid}}
  .hero-num{{font-size:44px}} .hero b{{font-size:26px}} h1{{font-size:36px}}
  .bars .lbl{{font-size:11.5px}}
  table.data{{border-radius:0}}
  table.data thead{{display:table-header-group}} table.data tfoot{{display:table-row-group}}
  table.data td{{padding:6px 12px}}
  tr,td,th{{break-inside:avoid}}
  .ver{{padding:18px 10px 12px}} .ver-plays{{font-size:22px}}
  .tip{{display:none}}
}}
</style>
<table class="sheet"><thead><tr><td>
<div class="runhead">
  <div class="rh-l">{TOOTH}<div>ARNER <small>FAMILY DENTISTRY &middot; SCREEN TRACTION REPORT</small></div></div>
  <div class="rh-r">MCTV<small>ELITE ADVERTISING</small></div>
</div>
</td></tr></thead>
<tbody><tr><td>
<div class="page"><div class="wrap">

<div class="brandbar">
  {WARNER_LOGO}
  {MCTV_LOGO}
</div>

<div class="titleblock">
  <div>
    <div class="eyebrow">Screen Traction Report</div>
    <h1>Warner Family Dentistry<small>Starkville network &middot; {fmt_d(first)} &ndash; {fmt_d(last)}</small></h1>
  </div>
  <div class="meta">
    <div><b>Prepared for:</b> Dr. Lindsey Warner</div>
    <div><b>Plan:</b> 10 screens &middot; $350 / month</div>
    <div><b>Spot length:</b> 30 seconds</div>
    <div><b>Prepared:</b> {date.today().strftime("%B %-d, %Y")}</div>
  </div>
</div>

<div class="hero">
  <div><div class="eyebrow">Total plays</div><div class="hero-num">{n(tot_plays)}</div><span>every airing of the Warner spot</span></div>
  <div><div class="eyebrow">Hours on screen</div><b>{hrs(tot_secs):,.0f}</b><span>{hrs(tot_secs)/24:.0f} full days of airtime</span></div>
  <div><div class="eyebrow">Screens reached</div><b>{n_screens}</b><span>{len(paid_rows)+1} selected + {len(gift_rows)} gifted</span></div>
  <div><div class="eyebrow">Cost per play</div><b>{cpp:.1f}&cent;</b><span>at $350 a month</span></div>
</div>

<p class="lede">Over five months the Warner Family Dentistry spot aired <strong>{n(tot_plays)} times</strong> across the Starkville MCTV network. The spot went through four versions while the creative was refined; every version is counted here.</p>

<div class="gifted">
  <div class="big">+{len(gift_rows)}<small>gifted screens</small></div>
  <p><b>Warner Family Dentistry paid for 10 screens.</b> MCTV also ran the spot at no charge on {len(gift_rows)} additional locations, including high-traffic hosts like Uno Mas Tacos y Tequila, Skate Zone, Starkville Parks and Recreation, and Elm Lake Golf Course. Those bonus screens delivered <span class="amt">{n(gift_plays)} plays</span>, shown in amber throughout this report.</p>
</div>

<div class="split">
  <div class="card">
    <div class="eyebrow">Where the plays came from</div>
    <div class="share"><i class="p" style="width:{paid_plays/tot_plays*100:.1f}%"></i><i class="g" style="width:{gift_plays/tot_plays*100:.1f}%"></i></div>
    <div class="share-key"><span><i style="background:var(--blue)"></i>Selected screens <b>{n(paid_plays)}</b></span><span><i style="background:var(--amber)"></i>Gifted screens <b>{n(gift_plays)}</b></span></div>
    <p class="share-note"><b>{gift_plays/tot_plays*100:.0f}%</b> of all plays came from screens Warner Family Dentistry did not pay for. The 10 selected screens averaged <b>{paid_plays/len(paid_rows):,.0f}</b> plays each.</p>
  </div>
  <div class="card">
    <div class="eyebrow">Campaign at a glance</div>
    <div class="kv">
      <div>Campaign window</div><div><b>{fmt_d(first)} &ndash; {fmt_d(last)}</b></div>
      <div>Days on air</div><div><b>{(date.fromisoformat(last)-date.fromisoformat(first)).days+1}</b></div>
      <div>Busiest screen</div><div><b>{html.escape(rows[0]['name'])}</b></div>
      <div>Plays per screen per day</div><div><b>{tot_plays/len(rows)/((date.fromisoformat(last)-date.fromisoformat(first)).days+1):.0f}</b></div>
    </div>
  </div>
</div>

<section class="chart-sec">
  <div class="sec-head"><span class="sec-num">01</span><h2>Plays by screen</h2></div>
  <p class="sub">All four spot versions combined, {fmt_d(first)} through {fmt_d(last)}. Hover a bar for details.</p>
  <div class="legend"><span class="p"><i></i>Selected screen (paid)</span><span class="g"><i></i>Gifted screen (no charge)</span></div>
  <div class="chart" id="chart">
  {svg}
  </div>
  <p class="fn">* {OFFLINE_NAME} ran the Warner spot but was disconnected from Wi-Fi during this period, so its player could not send play counts. Its plays are real but are not included in any total.</p>
</section>

<section class="tbl">
  <div class="sec-head"><span class="sec-num">02</span><h2>Every screen</h2></div>
  <p class="sub">Play count and airtime per host location. Gifted screens are shaded amber.</p>
  <div class="tablewrap">
  <table class="data">
    <thead><tr><th>Host location</th><th>Status</th><th class="num">Plays</th><th class="num">Hours</th><th>Active dates</th></tr></thead>
    <tbody>
    {table_rows}
    </tbody>
    <tfoot><tr><td>Total &middot; {len(rows)} reporting screens</td><td></td><td class="num">{n(tot_plays)}</td><td class="num">{hrs(tot_secs):,.1f}</td><td></td></tr></tfoot>
  </table>
  </div>
  <p class="fn">* {OFFLINE_NAME} played the spot but was offline from Wi-Fi, so no counts were reported. {n(demo['plays'])} plays on MCTV's internal demo player are excluded from every figure in this report.</p>
</section>

<section>
  <div class="sec-head"><span class="sec-num">03</span><h2>Four versions of the spot</h2></div>
  <p class="sub">The creative was refined three times before settling on the final cut.</p>
  <div class="vers">{vrows}</div>
</section>

<div class="closing">
  <div>
    <h3>Thank you for advertising with MCTV.</h3>
    <p>Questions about this report, or ready to plan the next flight? Reach out any time.</p>
  </div>
  <div class="who"><b>Swayze Hollingsworth</b>MCTV Digital<br>swayze@mctvofms.com &middot; 662-907-0404</div>
</div>

</div></div>
</td></tr></tbody>
<tfoot><tr><td>
<div class="runfoot"><div><i></i><b>Warner Family Dentistry</b> &middot; Screen Traction Report &middot; {fmt_d(first)} &ndash; {fmt_d(last)}</div><div>Source: MCTV player reports FS_1 &ndash; FS_4, exported {fmt_d(last)}</div></div>
</td></tr></tfoot></table>
<script>
(function(){{
  var chart=document.getElementById('chart'); if(!chart) return;
  var tip=document.createElement('div'); tip.className='tip'; tip.hidden=true; chart.appendChild(tip);
  chart.querySelectorAll('.row').forEach(function(g){{
    g.addEventListener('mousemove',function(e){{
      var d=g.dataset; var r=chart.getBoundingClientRect();
      tip.innerHTML='<b>'+d.name+'</b>'+d.kind+'<br>'+(d.plays>0?Number(d.plays).toLocaleString()+' plays &middot; '+d.hours+' hrs<br>':'')+d.range;
      tip.hidden=false;
      var x=e.clientX-r.left+12, y=e.clientY-r.top+12;
      if(x+250>r.width) x=e.clientX-r.left-250;
      tip.style.left=x+'px'; tip.style.top=y+'px';
    }});
    g.addEventListener('mouseleave',function(){{tip.hidden=true;}});
  }});
}})();
</script>
'''
out = 'Warner_Family_Dentistry_Traction_Report.html'
open(out, 'w').write(page.encode('ascii', 'xmlcharrefreplace').decode('ascii'))
print('wrote', out, dict(tot_plays=tot_plays, screens=n_screens, paid=len(paid_rows) + 1, gift=len(gift_rows), gift_plays=gift_plays))
