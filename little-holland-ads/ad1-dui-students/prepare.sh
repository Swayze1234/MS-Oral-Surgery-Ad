#!/usr/bin/env bash
# Turns the police-light footage into stills the page steps through frame by frame
# (the headless browser used for rendering can't decode H.264 video itself).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="$here/../assets/police_lights_intro.mp4"
out="$here/../.work/footage"
if [ ! -f "$out/intro_0001.jpg" ] || [ "$src" -nt "$out/intro_0001.jpg" ]; then
  rm -rf "$out" && mkdir -p "$out"
  # BT.709 video -> full-range JPEG (BT.601, as browsers decode it)
  ffmpeg -y -loglevel error -i "$src" \
    -vf "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt601:out_range=pc,format=yuvj444p" \
    -q:v 1 "$out/intro_%04d.jpg"
  echo "extracted $(ls "$out" | wc -l) footage frames"
fi
