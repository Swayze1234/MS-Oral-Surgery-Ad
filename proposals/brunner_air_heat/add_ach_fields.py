"""Adds fillable form fields to ach_form_flat.pdf using the boxes in ach_fields.json."""
import json, os, re, pymupdf
here = os.path.dirname(os.path.abspath(__file__))
fields = json.load(open(os.path.join(here, 'ach_fields.json')))
defaults = {'printed_name': 'Jason Brunner', 'title': 'Owner'}
NAVY = (0, 0.21, 0.49)

doc = pymupdf.open(os.path.join(here, 'ach_form_flat.pdf'))
page = doc[0]
radios = []
for f in fields:
    w = pymupdf.Widget()
    w.field_name = f['name']
    if f.get('label'):
        w.field_label = f['label']
    if f['type'] == 'radio':
        w.field_type = pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON
        w.rect = pymupdf.Rect(f['x0'] + 0.5, f['y0'] + 0.5, f['x1'] - 0.5, f['y1'] - 0.5)
        w.border_width = 0
        w.text_color = NAVY
        radios.append(f)
    else:
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        # sits the typed baseline on the printed label baseline
        w.rect = pymupdf.Rect(f['x0'] + 1, f['y0'] + 4.5, f['x1'] - 1, f['y1'] + 0.3)
        w.text_font = 'Helv'
        w.text_fontsize = 9.5
        w.text_color = NAVY
        w.border_width = 0
        if f.get('max'):
            w.text_maxlen = f['max']
        w.field_value = defaults.get(f['name'], '')
    w.fill_color = None
    page.add_widget(w)

# PyMuPDF names every radio's on-state the same; give each button its own value
# so a group behaves as pick-one, and start every group unselected.
by_rect = {(round(r['x0'] + 0.5, 1), round(r['y0'] + 0.5, 1)): r for r in radios}
parents = set()
for w in page.widgets():
    if w.field_type != pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON:
        continue
    src = by_rect[(round(w.rect.x0, 1), round(w.rect.y0, 1))]
    ap = doc.xref_get_key(w.xref, 'AP/N')[1]
    states = dict(re.findall(r'/([^\s/<>]+)\s*(\d+ 0 R)', ap))
    on_ref = next(v for k, v in states.items() if k != 'Off')
    doc.xref_set_key(w.xref, 'AP/N', '<</Off %s/%s %s>>' % (states['Off'], src['value'], on_ref))
    doc.xref_set_key(w.xref, 'AS', '/Off')
    parents.add(int(doc.xref_get_key(w.xref, 'Parent')[1].split()[0]))
for px in parents:
    doc.xref_set_key(px, 'V', '/Off')
    doc.xref_set_key(px, 'Ff', '49152')  # radio + no toggle to off

# Default resources so viewers can rebuild field appearances with the right fonts.
helv = doc.get_new_xref()
doc.update_object(helv, '<</Type/Font/Subtype/Type1/BaseFont/Helvetica/Encoding/WinAnsiEncoding>>')
zadb = doc.get_new_xref()
doc.update_object(zadb, '<</Type/Font/Subtype/Type1/BaseFont/ZapfDingbats>>')
cat = doc.pdf_catalog()
doc.xref_set_key(cat, 'AcroForm/DR', '<</Font<</Helv %d 0 R/ZaDb %d 0 R>>>>' % (helv, zadb))
doc.xref_set_key(cat, 'AcroForm/DA', '(/Helv 0 Tf 0 g)')

out = os.path.join(here, 'MCTV_ACH_Authorization_Brunner_Air_Heat.pdf')
doc.save(out, garbage=3, deflate=True)
print('saved', out, 'with', len(fields), 'widgets')
