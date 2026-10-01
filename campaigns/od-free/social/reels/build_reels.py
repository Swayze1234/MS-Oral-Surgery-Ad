#!/usr/bin/env python3
"""Restack the 16:9 OD Free screen spots into 9:16 reels and stories.

The spots are two panels: the message (left, 1300 px, animated) and the
MSDH / QR panel (right, 614 px, static) split by a gold rule. This script
puts the message panel on top and re-lays the MSDH logo, OD Free wordmark,
QR code and labels below it, cut straight from the spot at full quality.
Nothing is redrawn and no text is added.

Needs: ffmpeg, ffprobe, Pillow (pip install pillow).
Run:   python3 build_reels.py            (from anywhere)
Output: out/spot_*.mp4 (one vertical reel per spot), out/reel_1_three-spots.mp4,
        out/reel_4_fentanyl-anywhere.mp4, out/stills/*.png (9:16 stills).
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SPOTS = Path(os.environ.get("SPOTS", HERE / "../../assets/spots")).resolve()
OUT = Path(os.environ.get("OUT", HERE / "out")).resolve()

W, H = 1080, 1920
TOP_H = 898                 # message panel 1300x1080 scaled to 1080 wide
RULE_H = 8                  # gold rule between the panels
GOLD = (233, 170, 30)       # sampled from the spot
WHITE = (255, 255, 255)

# Source geometry (1920x1080 frame)
MSG_W = 1300                                # message panel, x 0..1299
RIGHT = dict(                               # static panel elements, (x0, y0, x1, y1)
    msdh=(1378, 56, 1848, 218),             # MSDH logo, tight
    kit=(1440, 254, 1784, 298),             # FREE NALOXONE KIT
    qr=(1366, 312, 1860, 806),              # QR with its navy border
    scan=(1396, 808, 1843, 889),            # phone icon + SCAN TO REQUEST
    odfree=(1424, 903, 1806, 1015),         # MAKE MISSISSIPPI / ODFREE.org
)

FILES = {
    "CommonAndDeadly_15s": "MCTV_OXF_ODFreeCommonAndDeadly_Paid_15s_v2.mp4",
    "FentanylAnywhere_15s": "MCTV_OXF_ODFreeFentanylAnywhere_Paid_15s_v2.mp4",
    "SaveALife_15s": "MCTV_OXF_ODFreeSaveALife_Paid_15s_v2.mp4",
    "RequestNaloxone_10s": "MCTV_OXF_ODFreeRequestNaloxone_Paid_10s_v2.mp4",
    "PreventDeaths_10s": "MCTV_OXF_ODFreePreventDeaths_Paid_10s_v2.mp4",
    "CommonAndDeadly_10s": "MCTV_OXF_ODFreeCommonAndDeadly_Paid_10s_v2.mp4",
}


def run(cmd):
    subprocess.run(cmd, check=True)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def frame(video, t, dest):
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}",
         "-i", str(video), "-frames:v", "1", str(dest)])


def fit(img, w=None, h=None):
    """Scale to a width or height, keeping aspect, Lanczos."""
    if w:
        h = round(img.height * w / img.width)
    else:
        w = round(img.width * h / img.height)
    return img.resize((w, h), Image.LANCZOS)


def bottom_panel(src_frame):
    """Build the white panel (with the gold rule on top) from one spot frame."""
    f = Image.open(src_frame).convert("RGB")
    el = {k: f.crop(box) for k, box in RIGHT.items()}
    # The MSDH mark sits on a faint grey box in the spot; lift it onto pure white.
    el["msdh"] = el["msdh"].point(lambda v: 255 if v >= 236 else v)

    panel_h = H - TOP_H                      # 1022 incl. rule
    p = Image.new("RGB", (W, panel_h), WHITE)
    p.paste(Image.new("RGB", (W, RULE_H), GOLD), (0, 0))

    margin = 64
    # Label, QR, label: the call to action sits right under the message and
    # inside Instagram's safe zone (clear of the caption overlay).
    y = RULE_H + 40
    kit = fit(el["kit"], h=50)
    p.paste(kit, ((W - kit.width) // 2, y)); y += kit.height + 14
    qr = fit(el["qr"], w=560)
    p.paste(qr, ((W - qr.width) // 2, y)); y += qr.height + 14
    scan = fit(el["scan"], h=78)
    p.paste(scan, ((W - scan.width) // 2, y)); y += scan.height + 44

    # Footer: the two partner marks side by side
    msdh = fit(el["msdh"], h=136)
    odfree = fit(el["odfree"], h=124)
    p.paste(msdh, (margin, y))
    p.paste(odfree, (W - margin - odfree.width, y + (msdh.height - odfree.height) // 2))
    y += msdh.height
    assert y <= panel_h - 24, f"bottom panel overflow: {y} > {panel_h}"
    return p


def build_spot(name, video, tmp):
    bottom_png = tmp / f"{name}_bottom.png"
    frame(video, 1.0, tmp / f"{name}_f.png")
    bottom_panel(tmp / f"{name}_f.png").save(bottom_png)

    out = OUT / f"spot_{name}.mp4"
    vf = (f"[0:v]crop={MSG_W}:1080:0:0,scale={W}:{TOP_H}:flags=lanczos,"
          f"pad={W}:{H}:0:0:color=white[v0];"
          f"[v0][1:v]overlay=0:{TOP_H}:shortest=1,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(video), "-loop", "1", "-i", str(bottom_png),
         "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-filter_complex", vf, "-map", "[v]", "-map", "2:a", "-shortest",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30",
         "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)])
    print(f"  wrote {out.name}")

    # 9:16 still from the closing frame, for stories and the carousel
    (OUT / "stills").mkdir(exist_ok=True)
    frame(video, max(0.0, duration(video) - 0.3), tmp / f"{name}_last.png")
    last = Image.open(tmp / f"{name}_last.png").convert("RGB")
    still = Image.new("RGB", (W, H), WHITE)
    still.paste(fit(last.crop((0, 0, MSG_W, 1080)), w=W).crop((0, 0, W, TOP_H)), (0, 0))
    still.paste(Image.open(bottom_png), (0, TOP_H))
    still.save(OUT / "stills" / f"still_{name}.png", optimize=True)
    return out


def main():
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found")
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Spots folder: {SPOTS}")
    present = {k: SPOTS / v for k, v in FILES.items() if (SPOTS / v).is_file()}
    for k, v in FILES.items():
        if k not in present:
            print(f"  missing: {v}")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        print("Building vertical versions of each spot...")
        built = {k: build_spot(k, v, tmp) for k, v in present.items()}

        if "FentanylAnywhere_15s" in built:
            shutil.copy(built["FentanylAnywhere_15s"], OUT / "reel_4_fentanyl-anywhere.mp4")
            print("  wrote reel_4_fentanyl-anywhere.mp4")

        cad = next((k for k in ("CommonAndDeadly_15s", "CommonAndDeadly_10s") if k in built), None)
        if cad and "FentanylAnywhere_15s" in built and "SaveALife_15s" in built:
            print(f"Building Reel 1 ({cad} + Fentanyl + Save a life)...")
            lst = tmp / "list.txt"
            lst.write_text("".join(f"file '{built[k]}'\n" for k in (cad, "FentanylAnywhere_15s", "SaveALife_15s")))
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
                 "-i", str(lst), "-c", "copy", str(OUT / "reel_1_three-spots.mp4")])
            print("  wrote reel_1_three-spots.mp4")

    if len(present) < len(FILES):
        print("Some spots were missing; see assets/spots/README.md for the file names.")
    print(f"Done. Output in {OUT}")


if __name__ == "__main__":
    main()
