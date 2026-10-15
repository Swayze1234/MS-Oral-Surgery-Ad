"""Assemble one-pager/index.html and print it to output/OCG_MCTV_One_Pager.pdf (Letter, one page)."""
import os, sys, datetime
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
fonts_css = open(os.path.join(ROOT,'assets','fonts','fonts.css')).read().replace("url('","url('../assets/fonts/")
logo = open(os.path.join(ROOT,'assets','logo','logo-inner.svg.fragment')).read()
# small thumbnails for the storyboard row (keeps the PDF light)
from PIL import Image
th = os.path.join(HERE,'thumbs'); os.makedirs(th, exist_ok=True)
for f in os.listdir(os.path.join(ROOT,'output','stills')):
    if f.endswith('.jpg'):
        im = Image.open(os.path.join(ROOT,'output','stills',f)); im.thumbnail((720,405)); im.save(os.path.join(th,f), quality=86)
today = datetime.date(2026,10,15).strftime('%B %-d, %Y')
artist_note = os.environ.get('ARTIST_NOTE', 'Featured-artist slots shown with placeholder photos until artist photos are supplied.')
html = (open(os.path.join(HERE,'template.html')).read()
        .replace('{{FONTS_CSS}}',fonts_css).replace('{{LOGO_SVG}}',logo)
        .replace('../output/stills/','thumbs/').replace('{{TODAY}}',today).replace('{{ARTIST_NOTE}}',artist_note))
open(os.path.join(HERE,'index.html'),'w').write(html)
out = os.path.join(ROOT,'output','OCG_MCTV_One_Pager.pdf')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto('file://'+os.path.join(HERE,'index.html')); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    pg.pdf(path=out, format='Letter', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'}, prefer_css_page_size=True)
    pg.set_viewport_size({'width':816,'height':1056}); pg.screenshot(path=os.path.join(ROOT,'output','OCG_MCTV_One_Pager_preview.png'), full_page=False)
    b.close()
import fitz
print('pdf pages:', len(fitz.open(out)), '->', out)
