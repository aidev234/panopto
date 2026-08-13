#!/usr/bin/env python3
"""Expand the concise POC document into a full, screenshot-led specification."""
from pathlib import Path
import shutil, tempfile, zipfile, struct, re
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/Orion_POC_Functional_Specification.docx'
OUT=ROOT/'docs/Orion_Functional_Specification.docx'
SHOTS=sorted((ROOT/'docs/poc-platform-screenshots').glob('*.png'))[:10] + [
  ROOT/'docs/poc-platform-screenshots/11-case-notes-expanded.png',
  ROOT/'docs/poc-platform-screenshots/12-case-notes-collapsed.png',
  ROOT/'docs/poc-platform-screenshots/13-selector-corroboration.png',
]
assert len(SHOTS) == 13 and all(x.exists() for x in SHOTS), 'expected POC screenshots'

def r(s,b=False,c=None): return f'<w:r><w:rPr>{"<w:b/>" if b else ""}{f"<w:color w:val=\"{c}\"/>" if c else ""}</w:rPr><w:t xml:space="preserve">{escape(s)}</w:t></w:r>'
def p(s='',sty=None,b=False,c=None,after=120): return f'<w:p><w:pPr>{f"<w:pStyle w:val=\"{sty}\"/>" if sty else ""}<w:spacing w:after="{after}"/></w:pPr>{r(s,b,c)}</w:p>'
def cell(s,head=False): return f'<w:tc><w:tcPr>{"<w:shd w:fill=\"17324D\"/>" if head else ""}</w:tcPr>{p(str(s),b=head,c="FFFFFF" if head else None,after=55)}</w:tc>'
def tbl(head,rows,widths=(2400,6900)):
  top='<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="B8C7D9"/><w:left w:val="single" w:sz="4" w:color="B8C7D9"/><w:bottom w:val="single" w:sz="4" w:color="B8C7D9"/><w:right w:val="single" w:sz="4" w:color="B8C7D9"/><w:insideH w:val="single" w:sz="4" w:color="D9E2F3"/><w:insideV w:val="single" w:sz="4" w:color="D9E2F3"/></w:tblBorders></w:tblPr><w:tblGrid>'+''.join(f'<w:gridCol w:w="{x}"/>' for x in widths)+'</w:tblGrid>'
  return top+'<w:tr>'+''.join(cell(x,True) for x in head)+'</w:tr>'+''.join('<w:tr>'+''.join(cell(x) for x in row)+'</w:tr>' for row in rows)+'</w:tbl>'
def dimensions(path):
  with path.open('rb') as f:
    assert f.read(8) == b'\x89PNG\r\n\x1a\n'
    f.read(8); return struct.unpack('>II',f.read(8))
def extent(path):
  w,h=dimensions(path); scale=min(5943600/w, 6572250/h)
  return round(w*scale),round(h*scale)
def pic(rid,n,path):
  cx,cy=extent(path)
  return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{n}" name="Actual POC screen {n}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="poc-screen.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''

sections=[
('8. Detailed functional specification', 'The following sections describe current POC behaviour. They are implementation notes, not proposed enhancements.'),
('8.1 Case-management landing screen', None),
('Case list and controls', [('Open Cases / Watchlist metrics','Show totals derived from the current case set.'),('New Case','Opens the Save Case Details form. A saved case becomes available as a tile.'),('Case search','Filters by title, case number, location, and case tags.'),('Status and threat filters','Can be combined with search. Options shown in the POC must be retained.'),('Sort','Supports last edited, opened date, threat level, and case name.'),('Case tile','Shows case number, title, status, threat level, location, image, plus settings and delete actions.'),('Empty state','When no cases match, show the explicit “No matching cases yet” state.')]),
('8.2 Case settings and save/quit', None),
('Case forms', [('Identity','Title, known location, and optional case image URL are editable.'),('Status and risk','Status and threat level are separate fields. Watchlist reveals a monitoring-refresh cadence.'),('Retention','The user selects one of the displayed retention periods.'),('Save / cancel','Save Changes persists edits; Cancel/Close returns without applying edits.'),('Save & Quit Case','Opens a final save form with the same status/risk/retention controls before leaving the active case.')]),
('8.3 Workspace shell and navigation', None),
('Workspace navigation', [('Header','Shows the active case name and case number. Cases returns to the landing screen; Save & Quit Case opens case save; New Search / Collection opens the operation modal; Exit Session opens exit choices.'),('Overview group','Overview shows collection activity; Guide shows the investigation guide.'),('Collection group','Posts and Media switch the result presentation.'),('Digital Footprint group','Profiles, Pattern of Life, Timeline, and Entity Graph each activate their respective view.'),('Reporting group','Case Notes opens the Case File modal.'),('Active state','Only the selected workspace view is displayed; selected tab is visibly active.')]),
('8.4 Posts, media, search, and filtering', None),
('Review controls', [('Search','Searches the active case’s posts by text, username, or platform. The clear button resets the field.'),('Sort','Orders posts newest first or oldest first.'),('Sources','Check boxes: Twitter, Reddit, TikTok, Bluesky, Instagram, YouTube.'),('Post types','Check boxes: Posts, Reposts, Replies, Quotes, Comments.'),('Signals','Check boxes: Selectors, Ideological Indicators, Threat Keyword Parse, LLM Primary, LLM Secondary.'),('Facial Recognition','Run button, minimum-confidence range, status, and recurring-face filters are displayed in the filter panel.'),('Post detail / evidence','A result opens Post Details. Capture Evidence associates the selected post and analyst note with Cited Posts in the case file.')]),
('8.5 Insights and assessment', None),
('Insight panels', [('Geo / Entities','Displays Location Map, Entity Mentions, Selector Parse, and Custom Keyword Parse for current results.'),('Threat Assessment','Displays assessment coverage, manual Run AI Threat Assessment action, behaviour visualisations, themes, ideological indicators, and threat-keyword parse.'),('Sandbox','The LLM Sandbox accepts text plus optional username, platform, and source URL, then shows a simulated-post analysis result.'),('No-data states','The POC explicitly states when information has not been run or is unavailable; implement equivalent explanatory states.')]),
('8.6 Overview and guide', None),
('Overview and guide functions', [('Case Overview','Shows collection overview and available collection streams; refresh and rerun-failed actions are icon controls.'),('Investigation Guide','Lists a staged workflow and displays completion progress. Each stage is a guide to the existing workspace actions, not a separate case status.')]),
('8.7 Digital Footprint', None),
('Digital Footprint views', [('Profiles','Shows discovered profiles and a ranked Discovered Selectors panel. Selector panel supports information help and collapse.'),('Pattern of Life','Shows platform controls, Refresh Estimate, location map, timezone/location indications, hourly rhythm, and source mix.'),('Timeline','Shows timeline summary, earliest-event grid, and event list. Its empty state directs the user to run recon.'),('Entity Graph','Shows summary, Find entity search, Reset View, graph canvas, and selected-entity details. Its empty state directs the user to run recon.')]),
('8.8 Case File, evidence, and export', None),
('Case File controls', [('Subject details','POI name, known location, age, aliases, selected image, and image upload.'),('Narrative sections','Context, Threat / Risk Assessment, and Personal Details are editable. Each has an x control that removes the section from the report.'),('Selectors','Email, phone, and username inputs support multiple comma-separated entries plus corroboration display.'),('Evidence Capture','Cited Posts list is available from the evidence section and its popout icon.'),('Profiles','Profiles are listed in the file. Add Profile adds one; section can be excluded from report.'),('Actions','Save Notes persists the file; Export PDF creates the current case report; Cancel and close leave the modal.')]),
('8.9 Operations: Recon and collection', None),
('Operation modal', [('Chooser','New Search / Collection presents Recon and Collection options.'),('Recon','Selector rows include selector type, value, add (+), remove (×), and Run Recon. After results, Use Active Profiles for Collection and Go to Assessment can become available.'),('Collection','Target rows can be loaded from collection-ready profiles, added manually, or autofilled. Start Date and End Date are required before Collect and Open.'),('Progress','Recon and collection areas provide status/progress surfaces; the workflow overview records resulting streams.')]),
('8.10 Manual content, settings, and session exit', None),
('Supporting functions', [('Manual Content Insert','Allows freeform text and a PDF/TXT upload, plus optional author name, platform, source URL, and date. Save as Post adds it to the active case.'),('Settings','Includes configured service-key/token fields, default data-retention selection, custom-keyword entry, removable keyword pills, Save, Cancel, and Close.'),('Exit Session','Offers Exit Only, Exit and Save, Exit and Wipe, and Cancel. Exit and Wipe is presented as the destructive option.')]),
('8.11 Case Notes evidence and selector corroboration states', None),
('Focused Case Notes behaviour', [('Evidence sidebar expanded','Cited Posts is visible beside the editable Case File. Each displayed item has a figure number and the available Cite/delete controls.'),('Evidence sidebar collapsed','The sidebar can be collapsed to restore editing space; the evidence control restores it.'),('Selector corroboration','Email, phone, and username selectors are editable in the Case Notes selector section, which also displays corroboration information.'),('Report export','Export PDF is available from Case Notes and uses the current case file and cited evidence.')]),
]

extra=[]
for a,b in sections:
  if isinstance(b,list): extra.append(tbl(['Control / area','Required POC behaviour'],b))
  else: extra.extend([p(a,'Heading1' if a.startswith('8.') and a.count('.')==1 else 'Heading2'), p(b) if b else ''])
extra.append(p('9. Full POC screen catalogue','Heading1'))
extra.append(p('Each figure below is a browser capture from the running POC. Captions serve as implementation callouts.'))
labels=[
'Case management: metrics, search, filters, sorting, New Case, Settings, and case tiles.',
'Posts dashboard: case header, grouped navigation, post results, and insight rail.',
'Post filters: sources, post types, signals, and facial-recognition controls.',
'Threat Assessment: assessment coverage, manual assessment action, and signal visualisations.',
'Case Overview: collection streams and refresh / rerun-failed actions.',
'Investigation Guide: staged guidance and progress indicator.',
'Profiles: prioritised digital-footprint results and discovered-selector grouping.',
'Pattern of Life: location/rhythm display and refresh control.',
'Timeline: date-stamped footprint activity and empty-state guidance.',
'Entity Graph: graph canvas, entity find field, reset, and detail panel.',
'Case Notes with Cited Posts evidence sidebar expanded beside the editable case file.',
'Case Notes with the evidence sidebar collapsed, returning space to the editor.',
'Selector inputs and corroboration display inside Case Notes.',
]
for i,(shot,label) in enumerate(zip(SHOTS,labels),1):
  extra += [p(f'Figure {i}. {shot.stem.replace("-"," ").title()}','Heading2'),pic(f'rId{i+5}',i+20,shot),p(label,'Caption',c='666666',after=220)]

with tempfile.TemporaryDirectory() as tmp:
  tmp=Path(tmp); shutil.unpack_archive(SOURCE,tmp,'zip')
  docpath=tmp/'word/document.xml'; xml=docpath.read_text()
  xml=xml.replace('<w:sectPr>', ''.join(extra)+'<w:sectPr>',1)
  # The source document has three existing screen blocks. Match their dimensions to
  # their real PNG aspect ratio too, rather than forcing every image into one box.
  source_extents=[extent(x) for x in SHOTS[:3]]
  iterator=iter(source_extents)
  def replace_extent(match):
    try: cx,cy=next(iterator)
    except StopIteration: return match.group(0)
    return f'<wp:extent cx="{cx}" cy="{cy}"/>'
  xml=re.sub(r'<wp:extent cx="\d+" cy="\d+"/>',replace_extent,xml)
  iterator=iter(source_extents)
  def replace_a_extent(match):
    try: cx,cy=next(iterator)
    except StopIteration: return match.group(0)
    return f'<a:ext cx="{cx}" cy="{cy}"/>'
  xml=re.sub(r'<a:ext cx="\d+" cy="\d+"/>',replace_a_extent,xml)
  docpath.write_text(xml)
  relpath=tmp/'word/_rels/document.xml.rels'; rel=relpath.read_text().replace('</Relationships>','')
  for i,shot in enumerate(SHOTS,1):
    # overwrite the original three concise-capture images, then append the remaining full catalogue.
    image_no=i
    (tmp/'word/media'/f'image{image_no}.png').write_bytes(shot.read_bytes())
    rel += f'<Relationship Id="rId{i+5}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{image_no}.png"/>'
  rel += '</Relationships>'; relpath.write_text(rel)
  if OUT.exists(): OUT.unlink()
  shutil.make_archive(str(OUT.with_suffix('')),'zip',tmp)
  OUT.with_suffix('.zip').replace(OUT)
print(OUT)
