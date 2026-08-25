"""Pull reusable brand assets out of the MCTV North MS media kit PDF."""
import sys, pymupdf

KIT = sys.argv[1] if len(sys.argv) > 1 else \
    '/root/.claude/uploads/af2e75a0-3ea3-578a-92c3-dacafb941b39/dfe01939-MCTV_North_MS_Media_Kit.pdf'

doc = pymupdf.open(KIT)
# White "MCTV / ELITE ADVERTISING" wordmark, top-left of the cover page.
logo = doc.extract_image(11)
open('assets/mctv_logo_white.png', 'wb').write(logo['image'])
print('logo:', logo['width'], 'x', logo['height'], logo['ext'])
