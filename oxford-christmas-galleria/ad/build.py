"""Assemble ad/index.html from template.html + logo SVG + artists.json + logo_timeline.js"""
import json, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
fonts_dir = os.path.join(ROOT, 'assets', 'fonts')
fonts_css = open(os.path.join(fonts_dir, 'fonts.css')).read().replace("url('", "url('../assets/fonts/")
logo = open(os.path.join(ROOT, 'assets', 'logo', 'logo-inner.svg.fragment')).read()
artists = json.load(open(os.path.join(HERE, 'artists.json')))
timeline_path = os.path.join(HERE, 'logo_timeline.js')
timeline = open(timeline_path).read() if os.path.exists(timeline_path) else "  // stub\n  s1svg.style.opacity=1;"

def leaf_path(L, w):
    return (f"M0,0 C{L*0.25:.1f},{-w*0.55:.1f} {L*0.75:.1f},{-w*0.55:.1f} {L:.1f},0 "
            f"C{L*0.75:.1f},{w*0.55:.1f} {L*0.25:.1f},{w*0.55:.1f} 0,0 Z")

def sprig():
    """Corner ornament: a curved stem from bottom-right sweeping up-left, leaves + berries."""
    random.seed(7)
    els = ['<path d="M400,400 Q300,330 230,230 T60,60" fill="none" stroke="#4F7B5C" stroke-width="5" stroke-linecap="round"/>']
    pts = [(400,400),(355,370),(312,330),(270,282),(236,236),(200,195),(165,160),(128,125),(95,92),(62,62)]
    for i,(x,y) in enumerate(pts[1:]):
        side = 1 if i%2==0 else -1
        ang = -135 + side*55
        L = 70*(1-0.04*i); w = 24*(1-0.03*i)
        col = ['#A9B894','#5E8A6A','#C3CDAE','#5E8A6A'][i%4]
        els.append(f'<path transform="translate({x},{y}) rotate({ang})" d="{leaf_path(L,w)}" fill="{col}"/>')
    for (x,y,r,c) in [(300,300,11,'#E5705A'),(316,286,9,'#C8463E'),(292,318,8,'#C8463E'),(150,150,10,'#E5705A'),(165,138,8,'#C8463E')]:
        els.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
    return ''.join(els)

html = open(os.path.join(HERE, 'template.html')).read()
html = (html.replace('{{FONTS_CSS}}', fonts_css)
            .replace('{{LOGO_SVG}}', logo)
            .replace('{{ARTISTS_JSON}}', json.dumps(artists))
            .replace('{{SPRIG_JSON}}', json.dumps(sprig()))
            .replace('{{LOGO_TIMELINE}}', timeline))
open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('built index.html', len(html), 'bytes;', len(artists), 'artists')
