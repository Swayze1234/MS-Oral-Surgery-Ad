# Project CARE / SOSD Discovery Center — 30-second ad (1920x1080)

`ProjectCARE_30s_1920x1080.mp4` — 30 s, 1920x1080, 30 fps, H.264 + AAC (silent track), ready for MCTV screens.
`ProjectCARE_keyframes.png` — one still from each scene for quick review.

## Scenes
1. Project CARE — Healthy Families, Happy Families (family photo)
2. Active Parenting — Wed & Thu, 11:00–12:00, free diapers & wipes after two classes
3. Family Resource Library — Mon–Fri 8:00–4:30, what you can check out
4. More ways we help — Imagination Library, teen parent classes, family events, free adult therapy
5. Call today — Roy Ann Bell, 662-615-0033 / 662-320-4607, 1504 Louisville Street
6. End card — Discovery Center + Project CARE logos, StarkvilleSD.com/DiscoveryCenter, Facebook, funding line

## Re-rendering
Source art (flyer, brochure pages, logo from CARE_Logo.docx) is in `build/src/`.
Drop a `music.mp3` or `music.wav` into `build/src/` to add a soundtrack (auto-trimmed to 30 s with fades).

```bash
pip install pillow numpy imageio-ffmpeg
cd ads/starkville-socsd/build
python3 render.py
```

All on-screen copy is in the `SCENES` list and `end_card()` in `build/render.py`.
