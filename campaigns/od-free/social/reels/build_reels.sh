#!/usr/bin/env bash
# Builds vertical (1080x1920) reels from the six OD Free screen spots.
# Needs ffmpeg. Run from anywhere: ./build_reels.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPOTS="${SPOTS:-$HERE/../../assets/spots}"
OUT="${OUT:-$HERE/out}"

# ---- things you may want to change ---------------------------------------
TOP_TEXT="MCTV × MSDH"
TOP_SUB="On every MCTV screen in North Mississippi"
BOTTOM_TEXT="Free naloxone for every Mississippian"
BOTTOM_SUB="Scan the screen  ·  odfree.org"
BG="0x0A2342"            # canvas color behind the spot (navy)
FONT="${FONT:-/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf}"
# ---------------------------------------------------------------------------

S15_1="MCTV_OXF_ODFreeCommonAndDeadly_Paid_15s_v2.mp4"
S15_2="MCTV_OXF_ODFreeFentanylAnywhere_Paid_15s_v2.mp4"
S15_3="MCTV_OXF_ODFreeSaveALife_Paid_15s_v2.mp4"
S10_1="MCTV_OXF_ODFreeRequestNaloxone_Paid_10s_v2.mp4"
S10_2="MCTV_OXF_ODFreePreventDeaths_Paid_10s_v2.mp4"
S10_3="MCTV_OXF_ODFreeCommonAndDeadly_Paid_10s_v2.mp4"

command -v ffmpeg >/dev/null || { echo "ffmpeg not found"; exit 1; }
[ -f "$FONT" ] || { echo "font not found: $FONT (set FONT=/path/to/font.ttf)"; exit 1; }
mkdir -p "$OUT"

# Text is written to files so quotes and symbols never break the ffmpeg filter.
TXT="$(mktemp -d)"
printf '%s' "$TOP_TEXT"    > "$TXT/top"
printf '%s' "$TOP_SUB"     > "$TXT/topsub"
printf '%s' "$BOTTOM_TEXT" > "$TXT/bottom"
printf '%s' "$BOTTOM_SUB"  > "$TXT/bottomsub"
trap 'rm -rf "$TXT"' EXIT

# 16:9 spot scaled to 1080 wide (608 tall), centered on a 1080x1920 canvas,
# with two text bands. Safe zones: nothing important above y=220 or below y=1500.
FILTER="scale=1080:-2:flags=lanczos,setsar=1,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=$BG,\
drawtext=fontfile=$FONT:textfile=$TXT/top:fontcolor=white:fontsize=84:x=(w-text_w)/2:y=330,\
drawtext=fontfile=$FONT:textfile=$TXT/topsub:fontcolor=0xF2C14E:fontsize=36:x=(w-text_w)/2:y=450,\
drawtext=fontfile=$FONT:textfile=$TXT/bottom:fontcolor=white:fontsize=46:x=(w-text_w)/2:y=1330,\
drawtext=fontfile=$FONT:textfile=$TXT/bottomsub:fontcolor=0xF2C14E:fontsize=42:x=(w-text_w)/2:y=1410,\
format=yuv420p"

# Encode with a silent audio track so every platform accepts the upload.
encode() {  # encode <input> <output>
  ffmpeg -y -hide_banner -loglevel error \
    -i "$1" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -filter_complex "[0:v]$FILTER[v]" -map "[v]" -map 1:a -shortest \
    -c:v libx264 -preset medium -crf 20 -r 30 -c:a aac -b:a 96k -movflags +faststart \
    "$2"
  echo "  wrote $(basename "$2")"
}

have() { [ -f "$SPOTS/$1" ]; }

echo "Spots folder: $SPOTS"
missing=0
for f in "$S15_1" "$S15_2" "$S15_3" "$S10_1" "$S10_2" "$S10_3"; do
  have "$f" || { echo "  missing: $f"; missing=1; }
done

# One vertical version of each spot (for stories and single-spot reels).
echo "Building vertical versions of each spot..."
for f in "$S15_1" "$S15_2" "$S15_3" "$S10_1" "$S10_2" "$S10_3"; do
  have "$f" || continue
  name="${f#MCTV_OXF_ODFree}"; name="${name%_v2.mp4}"; name="${name/_Paid_/_}"
  encode "$SPOTS/$f" "$OUT/spot_${name}.mp4"
done

# Reel 4: the Fentanyl :15 spot on its own.
if have "$S15_2"; then
  cp "$OUT/spot_FentanylAnywhere_15s.mp4" "$OUT/reel_4_fentanyl-anywhere.mp4"
  echo "  wrote reel_4_fentanyl-anywhere.mp4"
fi

# Reel 1: Common and deadly, Fentanyl, Save a life, back to back.
# Uses the :15 cut of Common and deadly when present, otherwise the :10 cut.
cad=""
if have "$S15_1"; then cad="CommonAndDeadly_15s"; elif have "$S10_3"; then cad="CommonAndDeadly_10s"; fi
if [ -n "$cad" ] && have "$S15_2" && have "$S15_3"; then
  echo "Building Reel 1 ($cad + Fentanyl + Save a life)..."
  list="$TXT/list.txt"
  for s in "$cad" FentanylAnywhere_15s SaveALife_15s; do
    echo "file '$OUT/spot_${s}.mp4'" >> "$list"
  done
  ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "$list" -c copy \
    "$OUT/reel_1_three-spots.mp4"
  echo "  wrote reel_1_three-spots.mp4"
fi

if [ "$missing" = 1 ]; then
  echo "Some spots were missing; see assets/spots/README.md for the file names."
fi
echo "Done. Output in $OUT"
