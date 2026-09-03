"""Render partnership.html to PDF (Letter) and PNG previews using the pre-installed Chromium."""
import os, pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).parent.resolve()
proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                          proxy={"server": proxy} if proxy else None)
    pg = b.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2)
    import re
    html = (here / "partnership.html").read_text()
    svg = (here / "parlor1858_logo.svg").read_text()
    def inline(m):
        style = m.group(1) or ""
        return svg.replace('<svg ', f'<svg class="parlor"{style} ', 1)
    html = re.sub(r'<img class="parlor" src="parlor1858_logo.svg"[^>]*?( style="[^"]*")?>', inline, html)
    import base64
    logo = "data:image/png;base64," + base64.b64encode((here / "mctv_logo.png").read_bytes()).decode()
    html = html.replace('src="mctv_logo.png"', f'src="{logo}"')
    html = html.replace("<!-- FONTS -->", "<style>" + (here / "fonts" / "embedded.css").read_text() + "</style>")
    (here / "partnership_standalone.html").write_text(html)
    pg.set_content(html, wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    pg.pdf(path=str(here / "Parlor1858_MCTV_Host_Partnership.pdf"), format="Letter",
           print_background=True, prefer_css_page_size=True)
    pg.emulate_media(media="print")
    for i, sec in enumerate(pg.query_selector_all("section.page"), 1):
        sec.screenshot(path=str(here / f"preview_p{i}.png"))
    b.close()
print("done")
