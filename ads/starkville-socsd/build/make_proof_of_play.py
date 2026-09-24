#!/usr/bin/env python3
"""Build the Project CARE proof-of-play PDF from the MCTV traction report (.xlsx)."""
import openpyxl, re, sys, os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER

XLSX = sys.argv[1] if len(sys.argv) > 1 else "src/NTV18_SOCSD_OUT1_traction_2026-09-22_to_09-24.xlsx"
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
OUT = "../ProjectCARE_ProofOfPlay_2026-09-22_to_09-24.pdf"

wb = openpyxl.load_workbook(XLSX, data_only=True); ws = wb.worksheets[0]
rows = list(ws.iter_rows(values_only=True))
filename = rows[0][1]; total_count, total_dur = rows[2][2], rows[2][3]
hosts = sorted([r for r in rows[5:] if r[0]], key=lambda r: -r[6])
def secs(s):
    h, m, sec = re.match(r"(\d+)h (\d+)m (\d+)s", s).groups(); return int(h)*3600 + int(m)*60 + int(sec)
assert sum(r[6] for r in hosts) == total_count and sum(secs(r[7]) for r in hosts) == secs(total_dur)

TEAL = colors.HexColor("#29A59E"); LIME = colors.HexColor("#8DB237"); YELLOW = colors.HexColor("#F7C948"); INK = colors.HexColor("#282828")
ss = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=22, textColor=INK, spaceAfter=4, alignment=0)
SUB = ParagraphStyle("sub", parent=ss["Normal"], fontSize=11, textColor=colors.HexColor("#555555"), spaceAfter=14)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=13, textColor=TEAL, spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("body", parent=ss["Normal"], fontSize=10, leading=14)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=11, textColor=colors.HexColor("#666666"))
CELL = ParagraphStyle("cell", parent=BODY, fontSize=9.5, leading=12)
STAT_N = ParagraphStyle("statn", parent=BODY, fontName="Helvetica-Bold", fontSize=20, textColor=INK, alignment=TA_CENTER, leading=24)
STAT_M = ParagraphStyle("statm", parent=STAT_N, fontSize=16)
STAT_L = ParagraphStyle("statl", parent=BODY, fontSize=8.5, textColor=colors.HexColor("#555555"), alignment=TA_CENTER)

def footer(c, doc):
    c.saveState(); w, h = letter
    c.setFillColor(LIME); c.rect(0, 0, w, 0.28*inch, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, h-0.32*inch, w, 0.32*inch, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 10); c.drawString(0.75*inch, h-0.21*inch, "MCTV DIGITAL  ·  Proof of Play Report")
    c.setFont("Helvetica", 9); c.drawRightString(w-0.75*inch, h-0.21*inch, f"Page {doc.page}")
    c.setFillColor(INK); c.setFont("Helvetica", 8)
    c.drawCentredString(w/2, 0.09*inch, "Swayze Hollingsworth · MCTV Digital · swayze@mctvofms.com · 662-907-0404")
    c.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.7*inch, bottomMargin=0.6*inch,
                        title="Project CARE Proof of Play Report", author="MCTV Digital")
S = [Paragraph("Proof of Play Report", H1),
     Paragraph("Project CARE / SOSD Discovery Center · 30-second ad · September 22 – 24, 2026", SUB)]
meta = [["Prepared for", "Roy Ann Bell, Project Manager – Project CARE, SOSD Discovery Center"],
        ["Prepared by", "Swayze Hollingsworth, MCTV Digital"],
        ["Campaign", "Project CARE – Active Parenting & Family Resource Library (30-second spot)"],
        ["Media file", filename],
        ["Playlist", "D.476 1-Mainshow Starkville (plus Oxford network)"],
        ["Report period", "Tuesday, September 22, 2026 through Thursday, September 24, 2026"]]
t = Table([[Paragraph(f"<b>{a}</b>", CELL), Paragraph(b, CELL)] for a, b in meta], colWidths=[1.3*inch, 5.7*inch])
t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),0.4,colors.HexColor("#DDDDDD")),
                       ("BOTTOMPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5)]))
S += [t, Paragraph("Campaign Summary", H2)]
stats = [[Paragraph(str(len(hosts)), STAT_N), Paragraph(f"{total_count:,}", STAT_N), Paragraph(total_dur, STAT_M), Paragraph("30 sec", STAT_N)],
         [Paragraph("Host screens", STAT_L), Paragraph("Total plays", STAT_L), Paragraph("Total on-screen time", STAT_L), Paragraph("Spot length", STAT_L)]]
st = Table(stats, colWidths=[1.75*inch]*4, rowHeights=[0.45*inch, 0.3*inch])
st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F2F7F6")),("BOX",(0,0),(-1,-1),0.8,TEAL),
                        ("LINEAFTER",(0,0),(-2,-1),0.5,colors.HexColor("#CCE3E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
S += [st, Spacer(1, 8),
      Paragraph(f"The Project CARE ad played <b>{total_count:,} times</b> across <b>{len(hosts)} host locations</b> between September 22 and September 24, 2026, "
                f"for a combined <b>{total_dur}</b> of on-screen time. Every play is the full 30-second spot. "
                "Play counts and durations below come directly from the MCTV network playback log for this media file.", BODY),
      Paragraph("Screen Locations & Play Counts", H2)]
hdr = ["#", "Host location", "City", "Plays", "On-screen time", "First play", "Last play"]
data = [hdr] + [[str(i+1), Paragraph(r[0], CELL), f"{r[1]}, {r[2]}", f"{r[6]:,}", r[7], r[8], r[9]] for i, r in enumerate(hosts)]
data.append(["", Paragraph("<b>Total</b>", CELL), "", f"{total_count:,}", total_dur, "09/22/2026", "09/24/2026"])
ht = Table(data, colWidths=[0.3*inch, 2.55*inch, 1.05*inch, 0.6*inch, 1.05*inch, 0.75*inch, 0.75*inch], repeatRows=1)
ht.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),TEAL),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
       ("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(3,0),(3,-1),"RIGHT"),("ALIGN",(0,0),(0,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
       ("ROWBACKGROUNDS",(0,1),(-1,-2),[colors.white, colors.HexColor("#F4F8F1")]),("LINEBELOW",(0,0),(-1,-1),0.3,colors.HexColor("#DDDDDD")),
       ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#FFF3CF")),("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),("LINEABOVE",(0,-1),(-1,-1),1,YELLOW),
       ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
S += [ht, Spacer(1, 6),
      Paragraph("Locations are listed from most to fewest plays. Seventeen screens are in Starkville; Elm Lake Golf Course (Columbus) and Bep Haus (Oxford) "
                "are on the same regional network and also carried the spot. Play counts vary by location because each screen's loop length and "
                "hours of operation differ.", SMALL),
      Paragraph("What Aired", H2),
      Paragraph("Stills from the 30-second Project CARE spot as it appeared on screen (1920x1080):", BODY), Spacer(1, 4)]
from PIL import Image as PILImage
_w, _h = PILImage.open("stills_grid.png").size
g = Image("stills_grid.png", width=7*inch, height=7*inch*_h/_w)
S += [g, Spacer(1, 10),
      Paragraph("Source: MCTV network playback report for NTV18_SOCSD_OUT1.webm, exported September 24, 2026. Original spreadsheet available on request.", SMALL)]
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
