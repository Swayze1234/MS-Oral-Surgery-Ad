"""Adds fillable form fields to ach_form_flat.pdf using the boxes in ach_fields.json."""
import json, os, pymupdf
here = os.path.dirname(os.path.abspath(__file__))
fields = json.load(open(os.path.join(here, 'ach_fields.json')))
defaults = {'printed_name': 'Jason Brunner', 'title': 'Owner'}
doc = pymupdf.open(os.path.join(here, 'ach_form_flat.pdf'))
page = doc[0]
for f in fields:
    w = pymupdf.Widget()
    w.field_name = f['name']
    if f['type'] == 'check':
        w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
        w.rect = pymupdf.Rect(f['x0'], f['y0'], f['x1'], f['y1'])
        w.border_width = 0
    else:
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        w.rect = pymupdf.Rect(f['x0'] + 1, f['y0'] + 1, f['x1'] - 1, f['y1'] - 1.2)
        w.text_font = 'Helv'
        w.text_fontsize = 0 if f['name'] == 'signature' else 9.5
        w.text_color = (0, 0.21, 0.49)
        w.border_width = 0
        w.field_value = defaults.get(f['name'], '')
    w.fill_color = None
    page.add_widget(w)
out = os.path.join(here, 'MCTV_ACH_Authorization_Brunner_Air_Heat.pdf')
doc.save(out, garbage=3, deflate=True)
print('saved', out, 'with', len(fields), 'fields')
