#!/usr/bin/env python3
"""Generate a concise, POC-only editable Word specification using real POC captures."""
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'Orion_POC_Functional_Specification.docx'
SHOTS = [
    ('Case management', ROOT / 'docs/actual-poc-screenshots/01-case-management.png', 'Figure 1. Actual Orion POC: case list and case-management controls.'),
    ('Active case workspace', ROOT / 'docs/actual-poc-screenshots/02-case-dashboard.png', 'Figure 2. Actual Orion POC: an opened demonstration case and its workspace navigation.'),
    ('Recon setup', ROOT / 'docs/actual-poc-screenshots/03-recon-setup.png', 'Figure 3. Actual Orion POC: Recon setup using the supplied demonstration username, lnmangione.'),
]

def run(text, bold=False, color=None, size=None):
    props = ('<w:b/>' if bold else '') + (f'<w:color w:val="{color}"/>' if color else '') + (f'<w:sz w:val="{size}"/>' if size else '')
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
def para(text='', style=None, bold=False, color=None, size=None, after=140):
    sty = f'<w:pStyle w:val="{style}"/>' if style else ''
    return f'<w:p><w:pPr>{sty}<w:spacing w:after="{after}"/></w:pPr>{run(text,bold,color,size)}</w:p>'
def cell(text, head=False):
    shade = '<w:shd w:fill="17324D"/>' if head else ''
    return f'<w:tc><w:tcPr>{shade}</w:tcPr>{para(str(text), bold=head, color="FFFFFF" if head else None, after=60)}</w:tc>'
def table(headers, rows, widths):
    out=['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="B8C7D9"/><w:left w:val="single" w:sz="4" w:color="B8C7D9"/><w:bottom w:val="single" w:sz="4" w:color="B8C7D9"/><w:right w:val="single" w:sz="4" w:color="B8C7D9"/><w:insideH w:val="single" w:sz="4" w:color="D9E2F3"/><w:insideV w:val="single" w:sz="4" w:color="D9E2F3"/></w:tblBorders></w:tblPr><w:tblGrid>'+''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)+'</w:tblGrid>']
    out.append('<w:tr>'+''.join(cell(h,True) for h in headers)+'</w:tr>')
    out += ['<w:tr>'+''.join(cell(c) for c in row)+'</w:tr>' for row in rows]
    return ''.join(out)+'</w:tbl>'
def picture(rid, num):
    cx,cy=5943600,3714750
    return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{num}" name="POC screenshot {num}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="screenshot.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''

body=[]
body += [para('ORION', 'Title', color='17324D', size=42, after=80), para('POC Functional Specification', 'Subtitle', color='3F6788', size=28, after=240), para('Purpose', 'Heading1'), para('A concise description of the functionality currently present in the locally run Orion proof of concept. It is written to support user-story refinement. It does not propose roles, permissions, workflows, or features that are not shown in the POC.'), para('Demonstration data', 'Heading2'), para('Screens use a locally created demonstration case named “Demo case — Pep Mangione” and the supplied username “lnmangione”. These are display examples only; this document makes no claims about people or accounts.'), para(f'Prepared {date.today().isoformat()}', color='666666', after=240)]
body += [para('1. What the POC does', 'Heading1'), para('Orion is organised around investigation cases. From a case, the user can run Recon, set collection targets and dates, review returned posts, switch between analysis views, maintain a case file, capture evidence, export a PDF report, and adjust local settings.'), table(['Area','Current POC function'],[
 ('Case management','Create, search, filter, sort, open, edit, and delete cases. Case tiles show status, threat level, location, and case number.'),
 ('Recon','Enter one or more typed selectors, run Recon, review resulting profiles/selectors, and use active profiles for collection when available.'),
 ('Collection','Add targets, load collection-ready profiles, choose a date range, and start collection. The overview tracks collection streams and retry/refresh actions.'),
 ('Review','Search, sort, and filter posts by source, post type, and signals. Open post details, add manual content, and capture cited evidence.'),
 ('Analysis','View profiles, pattern of life, timeline, entity graph, geo/entities, and threat-assessment panels.'),
 ('Case file','Record subject/context/risk notes, selectors, profiles, and cited posts; save notes or export PDF.'),
 ('Settings/session','Set local defaults/custom keywords and use the Exit Session choices.'),
], [2700,7400])]
body += [para('2. Case management', 'Heading1'), para('The Case Management screen is the entry point.'), table(['Control','Function'],[
 ('New Case','Creates a new case and opens the case-details form.'),('Search','Searches case name, case number, or location.'),('Status filter','Shows All status, Open, Under Investigation, Closed, or Watchlist.'),('Threat filter','Shows All threat levels or a selected named threat level.'),('Sort','Orders by last edited, opened date, threat, or case name.'),('Case tile','Opens the selected case. The settings icon edits it; the delete icon removes it.'),('Settings','Opens the POC settings modal.'),
], [2600,7500]), para('Case details', 'Heading2'), para('The create/edit forms expose case title, known location, case image URL, status, threat level, data-retention period, and—when Watchlist is selected—monitoring refresh cadence. Save Changes persists edits; Cancel/Close exits the form.')]
body += [para('3. Open-case workspace', 'Heading1'), para('The case header provides Cases, Save & Quit Case, New Search / Collection, and Exit Session. The toolbar groups the available views:'), table(['Group','Views / actions'],[
 ('Overview','Overview and Guide.'),('Collection','Posts and Media.'),('Digital Footprint','Profiles, Pattern of Life, Timeline, and Entity Graph.'),('Reporting','Case Notes.'),
], [2700,7400]), para('The Posts view includes a text search, newest/oldest sort, source filters (Twitter, Reddit, TikTok, Bluesky, Instagram, YouTube), post-type filters, and signal filters. The same filter panel includes the action and confidence control for facial recognition.')]
body += [para('4. Recon and collection', 'Heading1'), para('New Search / Collection opens a choice between Recon and Collection.'), table(['Workflow','Current POC behaviour'],[
 ('Recon','Selector rows support a selector type and value; + adds a row; × removes a row; Run Recon starts the operation. Results can expose Use Active Profiles for Collection and Go to Assessment.'),
 ('Collection','The user can Load Collection-Ready Profiles, Add Target, Autofill Usernames, choose Start Date and End Date, then select Collect and Open.'),
 ('Overview','Collection Overview shows stream status and includes refresh-streams and rerun-failed actions.'),
], [2600,7500])]
body += [para('5. Review, analysis, and reporting', 'Heading1'), table(['Feature','Current POC function'],[
 ('Manual Content Insert','Saves freeform text or a supported file as a post with optional author, platform, source URL, and date details.'),
 ('Post / evidence','Post Details opens an item. Capture Evidence adds it to the Cited Posts area with an analyst note.'),
 ('Geo / Entities','Shows Location Map, Entity Mentions, Selector Parse, and Custom Keyword Parse.'),
 ('Threat Assessment','Shows assessment coverage, the Run AI Threat Assessment action, warning-behaviour visualisations, themes, ideological indicators, and threat-keyword parse.'),
 ('Digital Footprint','Profiles provides discovered selectors; Pattern of Life offers location/rhythm views; Timeline shows events; Entity Graph supports entity search and Reset View.'),
 ('Case Notes','Contains identity, context, threat/risk assessment, personal details, selectors, cited posts, and profiles. It provides Save Notes and Export PDF.'),
], [2600,7500]), para('6. Settings and session controls', 'Heading1'), para('Settings exposes fields for configured service keys/tokens, default data-retention period, and custom keywords. Exit Session offers Exit Only, Exit and Save, and Exit and Wipe. The POC also exposes optional demo-case and LLM sandbox controls when enabled.')]
body += [para('7. Real POC screenshots', 'Heading1'), para('The following captures were taken from a temporary local POC run for this document—not generated images.' )]
for i,(title,path,caption) in enumerate(SHOTS,1): body += [para(title,'Heading2'),picture(f'rId{i+2}',i),para(caption,'Caption',color='666666',after=240)]
body.append('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080"/></w:sectPr>')
doc='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><w:body>'+''.join(body)+'</w:body></w:document>'
styles='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:lang w:val="en-US"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:sz w:val="20"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:b/><w:color w:val="17324D"/><w:sz w:val="30"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:rPr><w:b/><w:color w:val="3F6788"/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/></w:style></w:styles>'
types='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'
rels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
docrels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'+''.join(f'<Relationship Id="rId{i+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i}.png"/>' for i in range(1,4))+'</Relationships>'
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml',types); z.writestr('_rels/.rels',rels); z.writestr('word/document.xml',doc); z.writestr('word/styles.xml',styles); z.writestr('word/_rels/document.xml.rels',docrels)
 for i,(_,path,_) in enumerate(SHOTS,1): z.write(path,f'word/media/image{i}.png')
print(OUT)
