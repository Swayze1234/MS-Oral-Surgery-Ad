"""Assemble one-pager/index.html and print it to output/OCG_MCTV_One_Pager.pdf (Letter, one page)."""
import os, sys, datetime
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
fonts_css = open(os.path.join(ROOT,'assets','fonts','fonts.css')).read().replace("url('","url('../assets/fonts/")
logo = ''
# small thumbnails for the storyboard row (keeps the PDF light)
from PIL import Image
th = os.path.join(HERE,'thumbs'); os.makedirs(th, exist_ok=True)
for f in os.listdir(os.path.join(ROOT,'output','stills')):
    if f.endswith('.jpg'):
        im = Image.open(os.path.join(ROOT,'output','stills',f)); im.thumbnail((720,405)); im.save(os.path.join(th,f), quality=86)
today = datetime.date.today().strftime('%B %-d, %Y')
artist_note = os.environ.get('ARTIST_NOTE', 'More photos and video footage can be dropped into the 14–23 s slots.')
import json as _json, html as _html
venues = _json.load(open(os.path.join(HERE,'host-locations.json')))
def loc_section(title, markets, cols, show_town, note=''):
    vs = [v for v in venues if v['market'] in markets]
    vs.sort(key=lambda v: (v['town'] if show_town else '', v['name'].lower()))
    from collections import Counter
    towns = Counter(v['town'] for v in vs); major = towns.most_common(1)[0][0] if vs else ''
    tag_all = show_town and towns[major] < 0.6 * len(vs)      # no clear home town: tag every entry
    items = []
    for v in vs:
        extra = []
        if show_town and (tag_all or v['town'] != major) and v['town'].lower() not in v['name'].lower(): extra.append(v['town'])
        if v['status'] and v['status'].lower() != 'ready': extra.append(v['status'].lower())
        items.append(f"<li>{_html.escape(v['name'])}" + (f" <span>· {_html.escape(' · '.join(extra))}</span>" if extra else '') + "</li>")
    return (f'<section class="loc {cols}"><h2>{title}<small>{len(vs)} screen{"s" if len(vs)!=1 else ""}{(" · " + note) if note else ""}</small></h2>'
            f'<ul>{"".join(items)}</ul></section>')
page2 = (loc_section('Oxford / Lafayette County', ['Oxford'], 'c3', False)
         + loc_section('Tupelo / Lee County', ['Tupelo'], 'c3', False)
         + loc_section('Golden Triangle', ['Starkville','Columbus'], 'c3', True, 'Starkville unless noted'))
page3 = (loc_section('Jackson metro', ['Jackson metro'], 'c5', True)
         + loc_section('Natchez', ['Natchez'], 'c5', False)
         + loc_section('Hattiesburg / Laurel', ['Hattiesburg / Laurel'], 'c5', True)
         + loc_section('Gulf Coast', ['Gulf Coast'], 'c5', True))
html = (open(os.path.join(HERE,'template.html')).read()
        .replace('{{LOC_PAGE2}}', page2).replace('{{LOC_PAGE3}}', page3)
        .replace('{{FONTS_CSS}}',fonts_css).replace('{{LOGO_SVG}}',logo)
        .replace('../output/stills/','thumbs/').replace('{{TODAY}}',today).replace('{{ARTIST_NOTE}}',artist_note))
open(os.path.join(HERE,'index.html'),'w').write(html)
out = os.path.join(ROOT,'output','OCG_MCTV_One_Pager.pdf')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto('file://'+os.path.join(HERE,'index.html')); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    pg.pdf(path=out, format='Letter', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'}, prefer_css_page_size=True)
    b.close()
import pymupdf
doc = pymupdf.open(out)
for i, page in enumerate(doc):
    page.get_pixmap(dpi=96).save(os.path.join(ROOT,'output', 'OCG_MCTV_One_Pager_preview.png' if i == 0 else f'OCG_MCTV_One_Pager_preview_p{i+1}.png'))
print('pdf pages:', len(doc), '->', out)
