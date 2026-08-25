#!/usr/bin/env python3
"""Assemble preview.html — a single self-contained web proof of all 10 booklet
pages, published as a Claude Artifact so edits can be reviewed without
downloading the PDF. Rerun after any page edit, then republish.

Usage:  python3 make_preview.py
"""
import base64
import datetime
import mimetypes
import re
from pathlib import Path

from build import ROOT, asset_images, fill_slots, set_cover_assets  # noqa: F401

OUT = ROOT / "preview.html"
PAGE_W, PAGE_H = 1056, 816  # 11in x 8.5in at 96dpi

GOOGLE_FONTS = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
    "?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500"
    "&family=Barlow:wght@400;500;600;700"
    '&family=Montserrat:wght@700;800&display=swap">'
)

TITLES = [
    "Cover", "Where MCTV Fits", "The Network", "Three Markets", "How Your Spot Runs",
    "Real Screens", "Your Creative", "CPM Comparison", "Pricing", "Next Steps",
]


def inline_images(html: str) -> str:
    def repl(m: re.Match) -> str:
        p = (ROOT / "pages" / m.group(1)).resolve()
        mime = mimetypes.guess_type(p.name)[0] or "image/png"
        return f'src="data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"'
    return re.sub(r'src="(\.\./assets/[^"]+)"', repl, html)


def prefix_css(css: str, pid: str) -> str:
    """Scope a page's own rules under its wrapper id so pages can't collide."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for rule in re.findall(r"([^{}]+)\{([^}]*)\}", css):
        sels = ",".join(f"#{pid} {s.strip()}" for s in rule[0].split(",") if s.strip())
        out.append(f"{sels}{{{rule[1]}}}")
    return "\n".join(out)


def main() -> None:
    pages = sorted((ROOT / "pages").glob("p[0-9]*.html"))
    shared = (ROOT / "style.css").read_text()
    # the proof scales pages itself and paints its own ground; drop the print-only
    # page sizing and white document background from the shared css
    shared = shared.replace("@page { size: 11in 8.5in; margin: 0; }", "")
    shared = shared.replace("html, body { background: #fff; }", "")

    scoped_css, sheets = [], []
    for i, page in enumerate(pages):
        pid = f"pg{i + 1}"
        html = page.read_text()
        if "cover" in page.name:
            html = set_cover_assets(html)
        html = fill_slots(html)
        html = inline_images(html)
        style = re.search(r"<style>(.*?)</style>", html, re.S)
        body = re.search(r"<body>\s*(.*?)\s*</body>", html, re.S).group(1)
        if style:
            scoped_css.append(prefix_css(style.group(1), pid))
        sheets.append(
            f'<section class="proof">'
            f'<div class="plabel"><span class="pnum">{i + 1:02d}</span> {TITLES[i]}</div>'
            f'<div class="sheet" id="{pid}"><div class="zoom">{body}</div></div>'
            f"</section>"
        )

    stamp = datetime.datetime.now().strftime("%b %d, %Y · %H:%M")
    doc = f"""<title>Financial Concepts Proposal</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
{GOOGLE_FONTS}
<style>
/* ---- proof-room chrome (single committed look; pages carry their own brand) ---- */
html, body {{ margin: 0; background: #171E2B; }}
body {{ font-family: 'Barlow', 'Liberation Sans', Arial, sans-serif; color: #93A2B8; }}
.bar {{
  position: sticky; top: 0; z-index: 5; display: flex; justify-content: space-between;
  align-items: baseline; gap: 16px; padding: 14px 22px; background: rgba(23,30,43,0.94);
  border-bottom: 1px solid #2A3548; backdrop-filter: blur(4px);
}}
.bar .t {{ font-family: 'Playfair Display', Georgia, serif; font-size: 17px; color: #F4F1EA; }}
.bar .t em {{ font-style: italic; color: #E8C87A; }}
.bar .s {{ font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; white-space: nowrap; }}
main {{ max-width: 1120px; margin: 0 auto; padding: 26px 20px 60px; }}
.note {{
  font-size: 13px; line-height: 1.5; background: #202A3D; border: 1px solid #2A3548;
  border-radius: 6px; padding: 10px 14px; margin-bottom: 26px;
}}
.note b {{ color: #E8C87A; font-weight: 600; }}
.proof {{ margin-bottom: 34px; }}
.plabel {{ font-size: 11px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; margin-bottom: 8px; }}
.plabel .pnum {{ color: #E8C87A; margin-right: 6px; }}
.sheet {{ overflow: hidden; border-radius: 3px; box-shadow: 0 10px 34px rgba(0,0,0,0.45); }}
.zoom {{ width: {PAGE_W}px; transform-origin: top left; }}
/* ---- shared booklet styles ---- */
{shared}
.page {{ page-break-after: auto; }}
/* ---- per-page styles, scoped ---- */
{chr(10).join(scoped_css)}
</style>
<div class="bar">
  <div class="t">Financial Concepts &middot; <em>Advertiser Partnership Proposal</em></div>
  <div class="s">Print proof &middot; 11&times;8.5&Prime; &middot; built {stamp}</div>
</div>
<main>
  <div class="note">Live proof of the spiral booklet — refresh this page after each edit.
  <b>Dashed frames are photo slots</b> (cover band, screen photos, billboard creative) that fill
  automatically once the image files are attached.</div>
  {chr(10).join(sheets)}
</main>
<script>
function fit() {{
  document.querySelectorAll('.sheet').forEach(function (sheet) {{
    var s = sheet.clientWidth / {PAGE_W};
    sheet.querySelector('.zoom').style.transform = 'scale(' + s + ')';
    sheet.style.height = ({PAGE_H} * s) + 'px';
  }});
}}
addEventListener('resize', fit);
addEventListener('load', fit);
fit();
</script>
"""
    OUT.write_text(doc)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
