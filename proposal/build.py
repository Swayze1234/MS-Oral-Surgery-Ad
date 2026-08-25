#!/usr/bin/env python3
"""Build Financial_Concepts_Proposal.pdf from the page templates.

Any images dropped into the asset folders are picked up automatically:
  assets/cover/       -> full-bleed cover background (first image, sorted by name)
  assets/screens/     -> page 6 photo grid, slots 1-6 (sorted by name)
  assets/billboards/  -> page 7 screen mockups, slots 1-2 (sorted by name)

Usage:  python3 build.py
"""
import base64
import mimetypes
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent
CHROMIUM = "/opt/pw-browsers/chromium"
OUT_PDF = ROOT.parent / "Financial_Concepts_Proposal.pdf"
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def asset_images(subdir: str) -> list[Path]:
    d = ROOT / "assets" / subdir
    return sorted(p for p in d.iterdir() if p.suffix.lower() in IMG_EXTS) if d.is_dir() else []


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def fill_slots(html: str) -> str:
    """Replace placeholder markup inside data-fill="dir/N" elements with real images."""
    def repl(m: re.Match) -> str:
        head, subdir, idx, body = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        imgs = asset_images(subdir)
        if idx <= len(imgs):
            return f'{head}<img src="{data_uri(imgs[idx - 1])}" alt="">'
        return m.group(0)

    return re.sub(
        r'(<div class="[^"]*" data-fill="(\w+)/(\d+)">)(<div class="ph">.*?</div>)',
        repl, html, flags=re.S,
    )


def set_cover_photo(html: str) -> str:
    imgs = asset_images("cover")
    if imgs:
        html = html.replace(
            'class="cover-photo"',
            f'class="cover-photo" style="background-image: url({data_uri(imgs[0])})"',
        )
        print(f"  cover photo: {imgs[0].name}")
    else:
        print("  cover photo: none found in assets/cover/ — using black fallback")
    return html


def print_page(html_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [
            CHROMIUM, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--force-device-scale-factor=1", "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000", "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}", html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )


def main() -> None:
    pages = sorted((ROOT / "pages").glob("p*.html"))
    if len(pages) != 10:
        sys.exit(f"expected 10 page templates, found {len(pages)}")

    merged = pymupdf.open()
    with tempfile.TemporaryDirectory() as td:
        staged = Path(td)
        for page in pages:
            print(f"building {page.name}")
            html = page.read_text()
            if "cover" in page.name:
                html = set_cover_photo(html)
            html = fill_slots(html)
            # stage next to the originals so relative asset/css paths keep working
            stage = page.parent / f"_build_{page.name}"
            stage.write_text(html)
            pdf = staged / f"{page.stem}.pdf"
            try:
                print_page(stage, pdf)
            finally:
                stage.unlink()
            with pymupdf.open(pdf) as part:
                merged.insert_pdf(part, from_page=0, to_page=0)

    merged.set_metadata({
        "title": "Financial Concepts — Advertiser Partnership Proposal",
        "author": "MCTV Digital",
        "subject": "MCTV indoor billboard network proposal for Financial Concepts, Columbus MS",
    })
    merged.save(OUT_PDF, garbage=4, deflate=True)
    w, h = merged[0].rect.width, merged[0].rect.height
    print(f"\nwrote {OUT_PDF} — {len(merged)} pages @ {w:.0f}x{h:.0f}pt")


if __name__ == "__main__":
    main()
