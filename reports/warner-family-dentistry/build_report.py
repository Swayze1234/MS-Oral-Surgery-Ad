import json, html
from datetime import date
d=json.load(open('agg.json'))
hosts=d['hosts']; versions=d['versions']

SELECTED = {  # client's chosen screens -> matching host name in reports (None = not found)
 '39759 Nutrition': None,
 'Two Brothers': 'Two Brothers Smoked Meats',
 'William Wells': 'William Wells Tire & Auto',
 'Lucky Nails': 'Lucky Nails & Spa',
 'Starkville Veterinary Hospital': 'Starkville Veterinary Hospital',
 'Umi': 'Umi Japanese Steakhouse & Sushi Bar',
 'Legends': 'Legends Hair Salon',
 'MS Asthma': 'Mississippi Asthma & Allergy Clinic, PA - Starkville',
 'Skate Odyssey': 'Skate Odyssey Inc',
}
paid_names={v for v in SELECTED.values() if v}
DEMO='D.476 Dealer Demo'

def fmt_d(s):
    y,m,dd=s.split('-'); return f"{int(m)}/{int(dd)}/{y}"
def hrs(sec): return sec/3600
def n(x): return f"{x:,}"

rows=[]
for name,h in hosts.items():
    if name==DEMO: continue
    rows.append(dict(name=name,plays=h['plays'],secs=h['secs'],first=h['first'],last=h['last'],
        paid=name in paid_names,city=h['city'],versions=h['versions']))
rows.sort(key=lambda r:-r['plays'])
tot_plays=sum(r['plays'] for r in rows); tot_secs=sum(r['secs'] for r in rows)
paid_rows=[r for r in rows if r['paid']]; gift_rows=[r for r in rows if not r['paid']]
paid_plays=sum(r['plays'] for r in paid_rows); gift_plays=sum(r['plays'] for r in gift_rows)
first=min(r['first'] for r in rows); last=max(r['last'] for r in rows)
months=5; spend=350*months
cpp=spend/tot_plays*100  # cents per play
maxp=rows[0]['plays']

# ---- chart (SVG horizontal bars)
LW=250; BW=520; RH=24; PADT=6
H=PADT*2+RH*len(rows)
ticks=[0,5000,10000,15000,20000]
def x(v): return LW+ v/20000*BW
svg=[f'<svg class="bars" viewBox="0 0 {LW+BW+70} {H+28}" role="img" aria-label="Plays per screen, all four ad versions combined">']
for t in ticks:
    svg.append(f'<line class="grid" x1="{x(t):.1f}" y1="{PADT}" x2="{x(t):.1f}" y2="{H}"/>')
    svg.append(f'<text class="tick" x="{x(t):.1f}" y="{H+18}" text-anchor="middle">{n(t)}</text>')
for i,r in enumerate(rows):
    y=PADT+i*RH; bh=16; by=y+(RH-bh)/2
    w=max(2,(r['plays']/20000)*BW)
    cls='paid' if r['paid'] else 'gift'
    label=r['name'].replace(' - Starkville','').replace(', PA','')
    svg.append(f'<g class="row" data-name="{html.escape(r["name"])}" data-plays="{r["plays"]}" data-hours="{hrs(r["secs"]):.1f}" data-kind="{"Selected screen" if r["paid"] else "Gifted screen"}" data-range="{fmt_d(r["first"])} – {fmt_d(r["last"])}">')
    svg.append(f'<rect class="hit" x="0" y="{y}" width="{LW+BW+70}" height="{RH}"/>')
    svg.append(f'<text class="lbl" x="{LW-12}" y="{y+RH/2+4}" text-anchor="end">{html.escape(label)}</text>')
    svg.append(f'<path class="bar {cls}" d="M{LW},{by} h{w-4:.1f} a4,4 0 0 1 4,4 v{bh-8} a4,4 0 0 1 -4,4 h-{w-4:.1f} z"/>')
    svg.append(f'<text class="val" x="{LW+w+8:.1f}" y="{y+RH/2+4}">{n(r["plays"])}</text>')
    svg.append('</g>')
svg.append('</svg>')
svg='\n'.join(svg)

# ---- table
def trow(r):
    badge='<span class="badge gift">Gifted</span>' if not r['paid'] else '<span class="badge paid">Selected</span>'
    return f'<tr class="{"gift-row" if not r["paid"] else ""}"><td>{html.escape(r["name"])}<span class="city">{r["city"]}</span></td><td>{badge}</td><td class="num">{n(r["plays"])}</td><td class="num">{hrs(r["secs"]):.1f}</td><td class="dates">{fmt_d(r["first"])} – {fmt_d(r["last"])}</td></tr>'
table_rows='\n'.join(trow(r) for r in rows)

# ---- versions
vlabels={1:'Original spot',2:'Revision 2',3:'Revision 3',4:'Final spot'}
vrows=''
for v in versions:
    p=v['plays']-v['demo_plays']
    vrows+=f'<div class="ver"><div class="ver-n">v{v["version"]}</div><div class="ver-body"><div class="ver-title">{vlabels[v["version"]]}</div><div class="ver-meta">{fmt_d(v["first"])} – {fmt_d(v["last"])}</div></div><div class="ver-plays">{n(p)}<span> plays</span></div></div>'

legends=hosts['Legends Hair Salon']; ww=hosts['William Wells Tire & Auto']
demo=hosts[DEMO]

FONTS=open('fonts_inline.css').read()+open('logofonts_inline.css').read()
import os,base64
def img_or(path,fallback,cls):
    if os.path.exists(path):
        b=base64.b64encode(open(path,'rb').read()).decode()
        return f'<img class="{cls} real" src="data:image/png;base64,{b}" alt="">'
    return fallback
WARNER_SVG='''<div class="warner-logo">
 <svg class="tooth" viewBox="0 0 100 124" aria-hidden="true">
  <path d="M50,14 C33,4 13,12 11,34 C10,50 21,58 24,76 C27,96 31,116 40,118 C48,119 48,98 50,88 C52,98 52,119 60,118 C69,116 73,96 76,76 C79,58 90,50 89,34 C87,12 67,4 50,14 Z" fill="none" stroke="#149BD1" stroke-width="9" stroke-linejoin="round"/>
  <path d="M14,30 C6,22 8,6 22,6 C31,6 33,15 27,18" fill="none" stroke="#149BD1" stroke-width="6" stroke-linecap="round"/>
 </svg>
 <div class="warner-text">
  <div class="warner-name">ARNER</div>
  <div class="warner-sub">FAMILY DENTISTRY</div>
  <div class="warner-spa">&amp; Med Spa</div>
 </div>
</div>'''
MCTV_SVG='''<div class="mctv-logo"><div class="mctv-name">MCTV</div><div class="mctv-sub">ELITE ADVERTISING</div></div>'''
WARNER_LOGO=img_or('logos/warner.png',WARNER_SVG,'warner-logo')
MCTV_LOGO=img_or('logos/mctv.png',MCTV_SVG,'mctv-logo')
page=f'''<title>Warner Family Dentistry Traction</title>
<style>
{FONTS}
:root{{
  --ground:#F6F8FA; --paper:#FFFFFF; --ink:#15191E; --ink-2:#4E5964; --ink-3:#7F8B96;
  --rule:#DCE3E8; --rule-soft:#EBF0F3;
  --teal:#149BD1; --teal-ink:#0B6C99; --teal-wash:#E3F3FB;
  --amber:#CC7A0E; --amber-ink:#8F5407; --amber-wash:#FBF0DF;
  --grid:#E3EAEE;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{
  --ground:#101418; --paper:#181E25; --ink:#EEF2F5; --ink-2:#B7C1CB; --ink-3:#8492A0;
  --rule:#2C3640; --rule-soft:#222B34;
  --teal:#1C9DD0; --teal-ink:#7CCBEF; --teal-wash:#143446;
  --amber:#CF7F12; --amber-ink:#F0B461; --amber-wash:#3D2C14;
  --grid:#26313B;
}}}}
:root[data-theme="dark"]{{
  --ground:#101418; --paper:#181E25; --ink:#EEF2F5; --ink-2:#B7C1CB; --ink-3:#8492A0;
  --rule:#2C3640; --rule-soft:#222B34;
  --teal:#1C9DD0; --teal-ink:#7CCBEF; --teal-wash:#143446;
  --amber:#CF7F12; --amber-ink:#F0B461; --amber-wash:#3D2C14;
  --grid:#26313B;
}}
*{{box-sizing:border-box}}
.brandbar{{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:0 0 22px}}
.brandbar img.real{{height:64px;width:auto;max-width:300px;object-fit:contain}}
.warner-logo{{display:flex;align-items:center;gap:2px}}
.warner-logo .tooth{{height:66px;width:auto;margin-right:-6px}}
.warner-text{{line-height:1}}
.warner-name{{font-family:"Playfair Display",Georgia,serif;font-weight:900;font-size:36px;letter-spacing:.06em;color:#15191E;line-height:.9}}
.warner-sub{{font-family:"Josefin Sans","IBM Plex Sans",sans-serif;font-size:11.5px;letter-spacing:.2em;color:#15191E;margin:5px 0 0 2px}}
.warner-spa{{font-family:"Great Vibes",cursive;font-size:19px;color:#149BD1;text-align:right;margin-top:-1px;line-height:1}}
.mctv-logo{{text-align:center;line-height:1}}
.mctv-name{{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;font-size:38px;letter-spacing:.34em;color:#1C1F2B;padding-left:.34em}}
.mctv-sub{{font-family:"Josefin Sans","IBM Plex Sans",sans-serif;font-size:10.5px;letter-spacing:.32em;color:#5A6B7D;padding-left:.32em;margin-top:6px}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]) .warner-name, :root:not([data-theme="light"]) .warner-sub, :root:not([data-theme="light"]) .mctv-name{{color:#EEF2F5}} :root:not([data-theme="light"]) .mctv-sub{{color:#B7C1CB}} }}
:root[data-theme="dark"] .warner-name, :root[data-theme="dark"] .warner-sub, :root[data-theme="dark"] .mctv-name{{color:#EEF2F5}}
:root[data-theme="dark"] .mctv-sub{{color:#B7C1CB}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}}
.page{{max-width:860px;margin:0 auto;padding:34px 28px 48px}}
h1,h2,.stat b,.ver-plays,.ver-n{{font-family:"Bricolage Grotesque","IBM Plex Sans",system-ui,sans-serif}}
.eyebrow{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);font-weight:600}}
header{{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end;padding-bottom:22px;border-bottom:2px solid var(--ink)}}
h1{{font-size:40px;line-height:1.02;margin:6px 0 0;font-weight:800;letter-spacing:-.02em;text-wrap:balance}}
h1 small{{display:block;font-size:17px;font-weight:500;letter-spacing:0;color:var(--ink-2);margin-top:8px}}
.meta{{text-align:right;font-size:13px;color:var(--ink-2);line-height:1.6}}
.meta b{{color:var(--ink);font-weight:600}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:26px 0 8px;border:1px solid var(--rule);border-radius:6px;background:var(--paper);overflow:hidden}}
.stat{{padding:16px 18px;border-right:1px solid var(--rule)}}
.stat:last-child{{border-right:0}}
.stat b{{display:block;font-size:30px;font-weight:700;letter-spacing:-.02em;line-height:1.05;font-variant-numeric:tabular-nums;margin:4px 0 4px}}
.stat span{{font-size:12.5px;color:var(--ink-2)}}
.stat.gift{{background:var(--amber-wash)}}
.stat.gift b{{color:var(--amber-ink)}}
.stat.gift .eyebrow{{color:var(--amber-ink)}}
.lede{{font-size:15.5px;max-width:64ch;color:var(--ink-2);margin:18px 0 0}}
.lede strong{{color:var(--ink);font-weight:600}}
.gifted{{background:var(--amber-wash);border-left:4px solid var(--amber);padding:14px 18px;border-radius:0 6px 6px 0;margin:22px 0 0;display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center}}
.gifted .big{{font-family:"Bricolage Grotesque",sans-serif;font-size:34px;font-weight:800;color:var(--amber-ink);letter-spacing:-.02em;line-height:1}}
.gifted p{{margin:0;font-size:14px;color:var(--ink)}}
.gifted p b{{font-weight:600}}
section{{margin-top:40px}}
h2{{font-size:21px;font-weight:700;letter-spacing:-.01em;margin:0 0 4px}}
.sub{{color:var(--ink-2);margin:0 0 16px;font-size:13.5px;max-width:70ch}}
.legend{{display:flex;gap:18px;font-size:12.5px;color:var(--ink-2);margin:0 0 6px}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:6px}}
.legend .p i{{background:var(--teal)}} .legend .g i{{background:var(--amber)}}
.chart{{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:14px 10px 6px;position:relative;overflow-x:auto}}
svg.bars{{width:100%;height:auto;display:block;font-family:"IBM Plex Sans",sans-serif}}
.bars .grid{{stroke:var(--grid);stroke-width:1}}
.bars .tick{{font-size:11px;fill:var(--ink-3);font-variant-numeric:tabular-nums}}
.bars .lbl{{font-size:12px;fill:var(--ink)}}
.bars .val{{font-size:11.5px;fill:var(--ink-2);font-variant-numeric:tabular-nums}}
.bars .bar.paid{{fill:var(--teal)}} .bars .bar.gift{{fill:var(--amber)}}
.bars .hit{{fill:transparent}}
.bars .row:hover .hit{{fill:var(--rule-soft)}}
.tip{{position:absolute;pointer-events:none;background:var(--ink);color:var(--ground);font-size:12px;padding:8px 10px;border-radius:5px;line-height:1.4;box-shadow:0 4px 14px rgba(0,0,0,.18);max-width:240px;z-index:2}}
.tip b{{display:block;font-weight:600;margin-bottom:2px}}
table{{width:100%;border-collapse:collapse;background:var(--paper);border:1px solid var(--rule);border-radius:6px;overflow:hidden;font-size:13px}}
thead th{{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:600;padding:10px 12px;border-bottom:1px solid var(--rule);background:var(--paper)}}
td{{padding:8px 12px;border-bottom:1px solid var(--rule-soft);vertical-align:middle}}
tbody tr:last-child td{{border-bottom:0}}
td .city{{display:block;font-size:11.5px;color:var(--ink-3)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
th.num{{text-align:right}}
.dates{{white-space:nowrap;color:var(--ink-2);font-variant-numeric:tabular-nums}}
tr.gift-row td{{background:color-mix(in srgb,var(--amber-wash) 45%,var(--paper))}}
.badge{{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.04em;padding:2px 8px;border-radius:999px;white-space:nowrap}}
.badge.gift{{background:var(--amber-wash);color:var(--amber-ink);border:1px solid color-mix(in srgb,var(--amber) 40%,transparent)}}
.badge.paid{{background:var(--teal-wash);color:var(--teal-ink);border:1px solid color-mix(in srgb,var(--teal) 40%,transparent)}}
tfoot td{{font-weight:600;border-top:2px solid var(--rule);background:var(--paper)}}
.tablewrap{{overflow-x:auto}}
.vers{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
.ver{{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:14px 14px 12px;display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;gap:4px 10px}}
.ver-n{{font-size:13px;font-weight:700;color:var(--teal-ink);background:var(--teal-wash);border-radius:4px;padding:2px 7px;align-self:start}}
.ver-title{{font-weight:600;font-size:13.5px}}
.ver-meta{{font-size:12px;color:var(--ink-3);font-variant-numeric:tabular-nums}}
.ver-plays{{grid-column:1/-1;font-size:24px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums;margin-top:4px}}
.ver-plays span{{font-family:"IBM Plex Sans",sans-serif;font-size:12px;font-weight:400;color:var(--ink-3);margin-left:4px;letter-spacing:0}}
.notes{{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:6px 20px}}
.notes dl{{margin:0}}
.notes .n{{display:grid;grid-template-columns:200px 1fr;gap:14px;padding:12px 0;border-bottom:1px solid var(--rule-soft)}}
.notes .n:last-child{{border-bottom:0}}
.notes dt{{font-weight:600;font-size:13.5px}}
.notes dd{{margin:0;color:var(--ink-2);font-size:13.5px}}
footer{{margin-top:44px;padding-top:16px;border-top:1px solid var(--rule);display:flex;justify-content:space-between;gap:16px;font-size:12.5px;color:var(--ink-2);flex-wrap:wrap}}
footer b{{color:var(--ink);font-weight:600}}
@media (max-width:640px){{ .stats,.vers{{grid-template-columns:repeat(2,1fr)}} .stat:nth-child(2){{border-right:0}} .stat{{border-bottom:1px solid var(--rule)}} .stat:nth-child(n+3){{border-bottom:0}} header{{grid-template-columns:1fr}} .meta{{text-align:left}} .notes .n{{grid-template-columns:1fr}} }}
@media print{{
  @page{{size:letter;margin:.55in .5in}}
  :root{{--ground:#fff}}
  body{{font-size:12.5px}}
  .page{{max-width:none;padding:0}}
  section{{margin-top:26px}}
  .chart,.stats,table,.ver,.notes,.gifted{{break-inside:avoid;box-shadow:none}}
  .stat b{{font-size:26px}}
  h1{{font-size:34px}}
  .bars .lbl{{font-size:11.5px}}
  .tip{{display:none}}
  tr,td,th{{break-inside:avoid}}
  section.chart-sec{{break-before:page}}
  h2,.sub,.legend{{break-after:avoid}}
  thead{{display:table-header-group}}
  tfoot{{display:table-row-group}}
  .stats{{margin-top:18px}}
  footer{{margin-top:28px}}
}}
</style>
<div class="page">
<div class="brandbar">
  {WARNER_LOGO}
  {MCTV_LOGO}
</div>
<header>
  <div>
    <div class="eyebrow">Screen Traction Report</div>
    <h1>Warner Family Dentistry<small>Starkville network &middot; {fmt_d(first)} &ndash; {fmt_d(last)}</small></h1>
  </div>
  <div class="meta">
    <div><b>Plan:</b> 10 screens &middot; $350 / month</div>
    <div><b>Spot length:</b> 30 seconds</div>
    <div><b>Prepared:</b> {date.today().strftime("%B %-d, %Y")}</div>
  </div>
</header>

<div class="stats">
  <div class="stat"><div class="eyebrow">Total plays</div><b>{n(tot_plays)}</b><span>every airing of the Warner spot</span></div>
  <div class="stat"><div class="eyebrow">Hours on screen</div><b>{hrs(tot_secs):,.0f}</b><span>{hrs(tot_secs)/24:.0f} full days of airtime</span></div>
  <div class="stat"><div class="eyebrow">Screens reached</div><b>{len(rows)}</b><span>{len(paid_rows)} selected + {len(gift_rows)} gifted</span></div>
  <div class="stat gift"><div class="eyebrow">Plays on gifted screens</div><b>{n(gift_plays)}</b><span>{gift_plays/tot_plays*100:.0f}% of all plays, at no charge</span></div>
</div>

<p class="lede">Over five months the Warner Family Dentistry spot aired <strong>{n(tot_plays)} times</strong> across the Starkville MCTV network. At $350 a month that works out to roughly <strong>{cpp:.1f}¢ per play</strong>. The spot went through four versions while the creative was refined; every version is counted here.</p>

<div class="gifted">
  <div class="big">+{len(gift_rows)}</div>
  <p><b>Gifted screens.</b> Warner Family Dentistry paid for 10 screens. MCTV also ran the spot at no charge on {len(gift_rows)} additional locations, including high-traffic hosts like Uno Mas Tacos y Tequila, Skate Zone, BJ's Family Pharmacy, and Starkville Parks and Recreation. Those bonus screens delivered <b>{n(gift_plays)} plays</b>, shown in amber throughout this report.</p>
</div>

<section class="chart-sec">
  <h2>Plays by screen</h2>
  <p class="sub">All four spot versions combined, {fmt_d(first)} through {fmt_d(last)}. Hover a bar for details.</p>
  <div class="legend"><span class="p"><i></i>Selected screen (paid)</span><span class="g"><i></i>Gifted screen (no charge)</span></div>
  <div class="chart" id="chart">
  {svg}
  </div>
</section>

<section class="tbl">
  <h2>Every screen</h2>
  <p class="sub">Play count and airtime per host location. Gifted screens are shaded amber.</p>
  <div class="tablewrap">
  <table>
    <thead><tr><th>Host location</th><th>Status</th><th class="num">Plays</th><th class="num">Hours</th><th>Active dates</th></tr></thead>
    <tbody>
    {table_rows}
    </tbody>
    <tfoot><tr><td>Total · {len(rows)} screens</td><td></td><td class="num">{n(tot_plays)}</td><td class="num">{hrs(tot_secs):,.1f}</td><td></td></tr></tfoot>
  </table>
  </div>
</section>

<section>
  <h2>Four versions of the spot</h2>
  <p class="sub">The creative was refined three times before settling on the final cut. Plays below exclude MCTV's internal demo player.</p>
  <div class="vers">{vrows}</div>
</section>

<footer>
  <div><b>Swayze Hollingsworth</b> · MCTV Digital · swayze@mctvofms.com · 662-907-0404</div>
  <div>Source: MCTV player reports, files FS_1 through FS_4, exported {fmt_d(last)}</div>
</footer>
</div>
<script>
(function(){{
  var chart=document.getElementById('chart'); if(!chart) return;
  var tip=document.createElement('div'); tip.className='tip'; tip.hidden=true; chart.appendChild(tip);
  chart.querySelectorAll('.row').forEach(function(g){{
    g.addEventListener('mousemove',function(e){{
      var d=g.dataset; var r=chart.getBoundingClientRect();
      tip.innerHTML='<b>'+d.name+'</b>'+d.kind+'<br>'+Number(d.plays).toLocaleString()+' plays · '+d.hours+' hrs<br>'+d.range;
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
out='Warner_Family_Dentistry_Traction_Report.html'
open(out,'w').write(page.encode('ascii','xmlcharrefreplace').decode('ascii'))
print('wrote',out)
print(dict(tot_plays=tot_plays,tot_hours=round(hrs(tot_secs),1),paid=len(paid_rows),gift=len(gift_rows),paid_plays=paid_plays,gift_plays=gift_plays,cpp=round(cpp,2),first=first,last=last))
