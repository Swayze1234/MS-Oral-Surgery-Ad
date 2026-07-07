"""
Rebuilds MCTV_Media_Kit_Tupelo.pdf from the original Oxford media kit.

Customizations applied:
  1. Cover photo (p1)  : Oxford stadium  -> Tupelo City Hall (+ legibility scrim)
  2. Back photo  (p11) : Oxford water tower -> downtown Tupelo street scene
  3. Contact block (p11): Creed Cannon -> Swayze Hollingsworth
  4. Footer (p11)      : Mary Michael Cannon removed; Swayze centered as sole contact
  5. Signature (p12)   : CREED CANNON -> SWAYZE HOLLINGSWORTH

Run from the build/ directory:  python3 make_cover.py && python3 build.py
Output is written one level up (repo root).
"""
import fitz, os

BASE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(BASE,"source","MCTV_Media_Kit_Oxford_original.pdf")
OUT=os.path.join(os.path.dirname(BASE),"MCTV_Media_Kit_Tupelo.pdf")
COVER=os.path.join(BASE,"cover.jpg")
BACK=os.path.join(BASE,"back.jpg")
BLOCK=os.path.join(BASE,"swayze_block.png")
LIB="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
LIBB="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def rgb(hexv): return ((hexv>>16&255)/255,(hexv>>8&255)/255,(hexv&255)/255)
NAVY_PANEL=(0/255,45/255,104/255)
NAVY_BAND=(1/255,19/255,47/255)
CREAM=(246/255,242/255,233/255)
GOLD=rgb(0xe8b84b); LT=rgb(0xe3eef9); GREY=rgb(0x6a7891)

FONT_LIB=fitz.Font(fontfile=LIB)
FONT_LIBB=fitz.Font(fontfile=LIBB)

doc=fitz.open(SRC)

# ---------- 1. Cover photo (page 1, xref 83) ----------
doc[0].replace_image(83, filename=COVER)

# ---------- 2. Back photo (page 11, xref 414) ----------
p11=doc[10]
p11.replace_image(414, filename=BACK)

# ---------- 3. Relocate footer: render original Swayze block, center it ----------
orig=fitz.open(SRC)          # untouched copy for the crop
crop_pdf=fitz.Rect(490,468,707,513)               # Swayze block in pts (incl. ring)
swz=orig[10].get_pixmap(matrix=fitz.Matrix(4,4), clip=crop_pdf)
swz.save(BLOCK)

# truly remove both original footer contacts (text + headshot images), keep the band
p11.add_redact_annot(fitz.Rect(46,466,262,514), fill=NAVY_BAND)   # Mary Michael block
p11.add_redact_annot(fitz.Rect(484,466,712,514), fill=NAVY_BAND)  # original Swayze block
p11.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE,
                     graphics=fitz.PDF_REDACT_LINE_ART_NONE)

# paste Swayze block centred on the page
bw=crop_pdf.width
newx0=480-bw/2
dest=fitz.Rect(newx0,crop_pdf.y0,newx0+bw,crop_pdf.y1)
p11.insert_image(dest, filename=BLOCK, keep_proportion=True)

# ---------- 4. Main contact block (page 11): Creed -> Swayze ----------
# remove old line1 (name + · MCTV Digital) and email line
for r in [fitz.Rect(452,169.5,608,183), fitz.Rect(452,192,653,205.2)]:
    p11.add_redact_annot(r, fill=NAVY_PANEL)
p11.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                     graphics=fitz.PDF_REDACT_LINE_ART_NONE)
# redraw line1
name="Swayze Hollingsworth"
p11.insert_text((453.59,178.72), name, fontfile=LIBB, fontname="libb",
                fontsize=11.25, color=GOLD)
nw=FONT_LIBB.text_length(name, fontsize=11.25)
p11.insert_text((453.59+nw,178.72), " · MCTV Digital", fontfile=LIB, fontname="lib",
                fontsize=11.25, color=LT)
# redraw email/phone
p11.insert_text((453.59,201.22), "swayze@mctvofms.com  ·  662-907-0404",
                fontfile=LIB, fontname="lib", fontsize=11.25, color=LT)

# ---------- 5. Page 12 signature: CREED -> SWAYZE ----------
p12=doc[11]
p12.add_redact_annot(fitz.Rect(714,454,905,464), fill=CREAM)
p12.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                     graphics=fitz.PDF_REDACT_LINE_ART_NONE)
sig="SWAYZE HOLLINGSWORTH · MCTV DIGITAL / DATE"
size=7.88; avail=911-716.16
while FONT_LIB.text_length(sig, fontsize=size)>avail and size>6.4:
    size-=0.05
p12.insert_text((716.16,461.01), sig, fontfile=LIB, fontname="lib",
                fontsize=size, color=GREY)
print(f"signature size={size:.2f} width={FONT_LIB.text_length(sig,fontsize=size):.1f} avail={avail:.1f}")

doc.save(OUT, garbage=4, deflate=True)
print("saved", OUT)
