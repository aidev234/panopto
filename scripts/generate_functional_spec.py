#!/usr/bin/env python3
"""Create the editable Orion functional specification (.docx) with only stdlib."""
from __future__ import annotations

import os
import shutil
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Orion_Functional_Specification.docx"
ASSETS = [
    ("Case management", ROOT / "frontend/static/concepts/screenshots/mantine-case-workspace.png",
     "Figure 1. Case-management landing view: summary metrics, search/filter controls, and case records."),
    ("Active case dashboard", ROOT / "frontend/static/concepts/screenshots/mantine-active-case-dashboard.png",
     "Figure 2. Active-case workspace: navigation, post review, and analytical insights."),
    ("Case notes and settings", ROOT / "frontend/static/concepts/screenshots/mantine-case-notes-settings.png",
     "Figure 3. Form-led case file and settings surfaces used for documentation and configuration."),
]

def t(text, bold=False, italic=False, color=None, size=None):
    props = ""
    if bold: props += "<w:b/>"
    if italic: props += "<w:i/>"
    if color: props += f'<w:color w:val="{color}"/>'
    if size: props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f"<w:r><w:rPr>{props}</w:rPr><w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>"

def p(text="", style=None, bold=False, italic=False, color=None, size=None, before=0, after=120):
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ""
    spacing = f'<w:spacing w:before="{before}" w:after="{after}"/>'
    return f"<w:p><w:pPr>{style_xml}{spacing}</w:pPr>{t(text, bold, italic, color, size)}</w:p>"

def bullet(text):
    return f'<w:p><w:pPr><w:pStyle w:val="ListBullet"/><w:spacing w:after="60"/></w:pPr>{t(text)}</w:p>'

def cell(text, header=False, width=None):
    width_xml = f'<w:tcW w:w="{width}" w:type="dxa"/>' if width else ""
    shade = '<w:shd w:fill="17324D"/>' if header else ""
    return f'<w:tc><w:tcPr>{width_xml}{shade}</w:tcPr>{p(text, bold=header, color="FFFFFF" if header else None, after=60)}</w:tc>'

def table(headers, rows, widths=None):
    cols = ''.join(f'<w:gridCol w:w="{w}"/>' for w in (widths or [2400] * len(headers)))
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="B8C7D9"/><w:left w:val="single" w:sz="4" w:color="B8C7D9"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="B8C7D9"/><w:right w:val="single" w:sz="4" w:color="B8C7D9"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="D9E2F3"/><w:insideV w:val="single" w:sz="4" w:color="D9E2F3"/>'
           f'</w:tblBorders></w:tblPr><w:tblGrid>{cols}</w:tblGrid>']
    out.append('<w:tr>' + ''.join(cell(x, True, (widths or [None]*len(headers))[i]) for i,x in enumerate(headers)) + '</w:tr>')
    for row in rows:
        out.append('<w:tr>' + ''.join(cell(str(x), False, (widths or [None]*len(headers))[i]) for i,x in enumerate(row)) + '</w:tr>')
    out.append('</w:tbl>')
    return ''.join(out)

def image_paragraph(rid, name, cx, cy):
    return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"
xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{name}" name="{name}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="{name}.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''

def main():
    body = []
    body += [p("ORION", "Title", color="17324D", size=42, after=100), p("Functional Specification and User-Story Foundation", "Subtitle", color="3F6788", size=28, after=300)]
    body += [p("Purpose", "Heading1"), p("This document describes the user-facing behaviour of the Orion proof of concept. It is intended to support product refinement, user-story writing, acceptance criteria, and design discussion. It deliberately avoids implementation choices and technical architecture."),
             p("Demo-data note", "Heading2"), p("The examples ‘lnmangione’ and ‘Pep Mangione’ are user-supplied demonstration values only. They are used below to make workflows concrete; this specification makes no assertion about any real person or account."),
             p(f"Prepared: {date.today().isoformat()} | Status: POC functional baseline", italic=True, color="666666", after=300),
             p("Document guide", "Heading1")]
    body += [table(["Section", "What it contains"], [
        ("1. Product scope", "Actors, goals, operating principles, and shared vocabulary."),
        ("2. End-to-end workflow", "The recommended analyst journey using the supplied demo values."),
        ("3. Functional specification", "Menus, screens, rules, user stories, and acceptance criteria."),
        ("4. Cross-cutting requirements", "Permissions, states, validation, auditability, and usability."),
        ("5. Story backlog", "A delivery-oriented slice of the POC capability."),
    ], [2400, 6500]), p("Contents", "Heading1")]
    for entry in ["1. Product scope and roles", "2. End-to-end demo workflow", "3. Case management", "4. Case workspace and navigation", "5. Recon and digital footprint", "6. Collection and content review", "7. Insights and assessment", "8. Case file, evidence, and reporting", "9. Configuration and session controls", "10. Cross-cutting functional rules", "11. Initial user-story backlog", "Appendix A. Screen reference images"]:
        body.append(bullet(entry))

    body += [p("1. Product scope and roles", "Heading1"), p("Orion is a case-first investigation workspace. An analyst begins with a case, adds known subject context and selectors, develops leads through recon, reviews collected content and signals, records evidence, and closes, monitors, or exports the case."),
             p("Primary users", "Heading2"), table(["Role", "Primary goals", "Expected actions"], [
                 ("Analyst", "Develop and document a case", "Create/open cases; run recon and collection; review content; capture evidence; author case notes."),
                 ("Supervisor / reviewer", "Prioritise and quality-check work", "Filter cases by status/risk; review case file, evidence, assessment coverage, and exports."),
                 ("Administrator", "Set operating defaults", "Maintain integration credentials, retention defaults, and custom keyword vocabulary."),
             ], [1800, 3100, 4000]),
             p("Key business objects", "Heading2"), table(["Object", "Functional meaning", "Core attributes shown to users"], [
                 ("Case", "The container for an investigation.", "Title, case number, location, status, threat level, retention, image, monitoring cadence."),
                 ("Selector", "A known search input used to find and link activity.", "Username, email, phone; source/corroboration where available."),
                 ("Profile / lead", "A discovered account or identity clue.", "Platform, handle, URL, linkage context, priority."),
                 ("Collected post", "A content item reviewed inside a case.", "Author, source, date/time, text/media, post type, signals, cited status."),
                 ("Evidence capture", "A preserved item cited in the case file/report.", "Post reference, analyst note, capture date, case association."),
             ], [1800, 3600, 3500])]

    body += [p("2. End-to-end demo workflow", "Heading1"), p("This workflow is a functional walkthrough, not a finding about the example values."),
             table(["Step", "Analyst action", "Expected product behaviour"], [
                 ("1", "Create a case for ‘Pep Mangione’. Add known location if available; leave unknown information blank.", "A new case record is saved with Open status and Unassessed threat level unless the analyst selects alternatives."),
                 ("2", "Open Case File and add ‘lnmangione’ as a username selector and ‘Pep Mangione’ as context.", "The case file saves the values, keeps them case-scoped, and makes the selector available to recon/collection workflows."),
                 ("3", "Choose New Search / Collection → Recon; submit lnmangione and any other authorised selectors.", "Progress is visible. Discovered profiles, selector pivots, and enrichment results are grouped for review rather than treated as confirmed facts."),
                 ("4", "Review Digital Footprint, Timeline, Entity Graph, and Pattern of Life.", "Each view explains when data is absent and supports an analyst’s linkage/relevance judgement."),
                 ("5", "Use collection-ready profiles or enter targets and a date range; start collection.", "The workspace shows source/job progress and then makes returned content available in Posts and Media."),
                 ("6", "Search/filter content, inspect post details, and capture relevant evidence with an analyst note.", "Filters update visible content; captured items appear in Cited Posts inside the Case File."),
                 ("7", "Review Geo / Entities and Threat Assessment views. Run the assessment only when authorised.", "Observed signals and assessment coverage are clearly distinguished from analyst conclusions."),
                 ("8", "Document rationale, set disposition (e.g., Watchlist), choose cadence if applicable, save, and export the case report.", "The record remains searchable with its selected status/risk and the report reflects saved case-file content and cited evidence."),
             ], [700, 3900, 4300])]

    body += [p("3. Case management", "Heading1"), p("Purpose: provide the landing view for locating, prioritising, creating, editing, opening, and closing investigation records."),
             p("Menu and control inventory", "Heading2"), table(["Control", "User-visible behaviour", "Rules / acceptance criteria"], [
                 ("New Case", "Opens the Save Case Details form.", "Requires title, location, status, threat level, and retention. Saving creates a case and returns the user to a usable state."),
                 ("Case search", "Matches name, case number, or location.", "Filtering updates the list without changing records; empty state says no matching cases."),
                 ("Status filter", "Limits list to Open, Under Investigation, Closed, or Watchlist.", "All status is the reset option."),
                 ("Threat filter", "Limits list by the six defined threat levels.", "Unassessed is a selectable value, not a missing-data error."),
                 ("Sort", "Orders by last edit, opened date, threat, or title.", "Default is last edited, newest first."),
                 ("Case tile", "Shows identity, status/risk, location, and recency; opens a case.", "Metrics show open-case and watchlist totals consistent with the current list of cases."),
                 ("Case settings", "Edits identity, location, image, status/risk, cadence, and retention.", "Watchlist exposes a required monitoring cadence; saving updates the corresponding tile and case workspace."),
                 ("Settings", "Opens global configuration.", "Does not alter the active case unless a separate case action is taken."),
             ], [1800, 4000, 3100])]
    body += [p("Case states", "Heading2"), table(["State", "Meaning", "Required behaviour"], [
        ("Open", "New or active work.", "Counts as an open case; can be opened, edited, and searched."),
        ("Under Investigation", "Actively being developed.", "Counts as open; retains all navigation and reporting functions."),
        ("Watchlist", "Ongoing monitoring state.", "Requires a cadence; appears in Watchlist metric and can be filtered."),
        ("Closed", "Work concluded.", "Remains searchable/reportable; excluded from open-case count."),
    ], [1800, 3300, 3800])]

    body += [p("4. Case workspace and navigation", "Heading1"), p("Opening a case presents a dashboard whose header preserves case identity and exposes the primary case actions: Cases, Save & Quit Case, New Search / Collection, and Exit Session."),
             p("Navigation groups", "Heading2"), table(["Group", "Destination", "Functional purpose"], [
                 ("Overview", "Overview; Guide", "Show collection activity/status and a guided sequence of investigation steps."),
                 ("Collection", "Posts; Media", "Review text content or media-focused result cards, with common search/sort/filter behaviour."),
                 ("Digital Footprint", "Profiles; Pattern of Life; Timeline; Entity Graph", "Explore discovered profile relationships, location/routine indications, time-stamped events, and linked entities."),
                 ("Reporting", "Case Notes", "Open the case-file editor and cited-evidence register."),
             ], [1800, 2700, 4400]),
             p("Workspace rules", "Heading2")]
    for x in ["Exactly one primary workspace view is active at a time; the active tab is visibly distinguishable.", "The case title and case number remain visible while navigating the dashboard.", "When a view has no data, it states the missing prerequisite (for example, run recon first) instead of presenting a misleading blank panel.", "Back to Cases preserves the case list context where practical. Save & Quit offers a clear save path before leaving the case."]:
        body.append(bullet(x))

    body += [p("5. Recon and digital footprint", "Heading1"), p("New Search / Collection begins with a choice between Recon and Collection. Recon is used to develop authorised selectors into reviewable leads; it is not an automatic confirmation of identity or relevance."),
             p("Recon setup", "Heading2"), table(["Control", "Behaviour"], [
                 ("Selector rows", "Allow one or more selectors. Each selector has a type/value appropriate to a username, email, phone, or other supported input."),
                 ("Add selector", "Adds another selector row without discarding entered values."),
                 ("Run Recon", "Starts a visible, case-scoped process and shows progress/status."),
                 ("Use Active Profiles for Collection", "Appears/enables when recon returns usable profiles; transfers selected/active profiles to collection setup."),
                 ("Go to Assessment", "Appears/enables when there is material to review in the case workspace."),
             ], [2800, 7100]),
             p("Digital Footprint views", "Heading2"), table(["View", "What the user can do", "Expected empty / boundary state"], [
                 ("Profiles", "Review discovered accounts and exposure in priority order; inspect grouped, ranked selector pivots; optionally filter/collapse." , "Prompt to run recon when no results are available."),
                 ("Pattern of Life", "Review location signals, likely locations, platform mix, and inferred posting rhythm; refresh the estimate." , "State that additional location/timestamp data is needed; do not present an estimate as certainty."),
                 ("Timeline", "Review date-stamped activity signals and earliest events." , "State that recon must be run when no events exist."),
                 ("Entity Graph", "Search/select relationships among queried selectors, discovered profiles, and linked attributes; reset the view." , "State that recon must be run when no graph data exists."),
             ], [1800, 4400, 3700])]

    body += [p("6. Collection and content review", "Heading1"), p("Collection setup accepts target profiles and a start/end date. The workflow supports manual target addition, loading collection-ready profiles from recon, and username autofill where relevant."),
             p("Collection requirements", "Heading2"), table(["Feature", "Functional requirement"], [
                 ("Target management", "An analyst can add targets, load recon-derived profiles, and remove/adjust targets before submitting."),
                 ("Date range", "A start and end date are required. The form must prevent or explain an invalid date range."),
                 ("Collect and Open", "Starts the collection workflow, communicates status/progress, and opens/returns the case workspace when reviewable results are available."),
                 ("Overview board", "Shows collection streams, current state, and actions to refresh streams or retry failed streams."),
                 ("Manual Content Insert", "Allows freeform text or permitted document content to be saved as a case-scoped post with optional author/platform/source/date metadata."),
             ], [2600, 7300]),
             p("Posts and Media review", "Heading2"), table(["Control", "Behaviour", "Acceptance criteria"], [
                 ("Search", "Searches displayed posts by post text, username, or platform; supports the product’s documented Boolean syntax.", "Clear control resets the search; results update after input without losing the active case."),
                 ("Sort", "Orders result cards newest-first or oldest-first.", "Changing sort does not change filter choices."),
                 ("Filters: sources", "Includes Twitter/X, Reddit, TikTok, Bluesky, Instagram, and YouTube.", "Default shows all enabled sources; analyst can combine source filters."),
                 ("Filters: post type", "Includes posts, reposts, replies, quotes, and comments.", "Filtering is cumulative with source and signal filters."),
                 ("Filters: signals", "Includes selectors, ideological indicators, threat keywords, and primary/secondary assessment labels.", "A selected signal returns only posts with that signal; absence of data is communicated."),
                 ("Facial recognition", "Allows the analyst to run it, set a minimum confidence, and filter recurring faces where available.", "Before use, screen says it has not been run; unavailable/no-match states are explicit."),
                 ("Post detail", "Opens the full post context and supports evidence capture.", "Closing returns to the prior reviewed list and keeps filters/search intact."),
             ], [1900, 4200, 3500])]

    body += [p("7. Insights and assessment", "Heading1"), p("Insights help the analyst triage content. The interface must distinguish raw/observed indicators from model-assisted labels and from the analyst’s documented assessment."),
             table(["Panel", "Function"], [
                 ("Geo / Entities", "Displays a location map, entity mentions, parsed selectors, and configured keyword matches from currently reviewed content."),
                 ("Threat Assessment", "Displays assessment coverage, a manual Run AI Threat Assessment action, primary/secondary warning behaviour views, themes, ideological indicators, and threat-keyword parsing."),
                 ("AI Threat Assessment", "Explains that cost is estimated before the action; reports progress/status; analyses only the intended current case/content scope."),
                 ("OpenAI Post Analysis Sandbox", "An isolated test surface where a user pastes text with optional username/platform/source URL, runs analysis, and reviews a simulated post result without changing case evidence unless separately saved."),
             ], [2700, 7200]),
             p("Assessment guardrails", "Heading2")]
    for x in ["Assessment output is presented as an observed assistive signal, never as a final disposition.", "The UI labels manual-run scope and coverage so users can see what was and was not assessed.", "Analysts retain the ability to use filters and review underlying posts before recording a case-level risk decision.", "An empty, unavailable, or incomplete assessment state is explicit and actionable."]:
        body.append(bullet(x))

    body += [p("8. Case file, evidence, and reporting", "Heading1"), p("Case Notes is the structured, editable case-file editor. It enables an analyst to maintain subject context, assessment rationale, selectors, profiles, cited evidence, and report content."),
             p("Case-file sections", "Heading2"), table(["Section", "Fields / actions", "Rules"], [
                 ("Identity", "Name, known location, age, aliases, selected/uploaded subject image.", "Image is optional; upload/selection must not erase text fields."),
                 ("Context", "Freeform investigation context.", "Analyst can remove this section from the report without deleting underlying notes."),
                 ("Threat / Risk Assessment", "Freeform analyst assessment.", "This is the place for human rationale and must remain distinguishable from automated signals."),
                 ("Personal Details", "Freeform structured context.", "Optional and report-controllable."),
                 ("Selectors", "Emails, phones, usernames plus corroboration information.", "Multiple values retained as separate visible entries where possible."),
                 ("Profiles", "Known/discovered profile list; Add Profile action.", "Can be removed from report without deleting case data."),
                 ("Evidence Capture / Cited Posts", "Captured post references and analyst notes; popout control.", "Only items deliberately captured are included as cited evidence."),
                 ("Actions", "Save Notes, Export PDF, Cancel/Close.", "Save persists edits. Export uses saved case-file content and cited evidence. Cancel/close warns or preserves unsaved-work expectations."),
             ], [1900, 4200, 3500])]

    body += [p("9. Configuration and session controls", "Heading1"), table(["Surface", "User-visible functions", "Functional rules"], [
        ("Settings", "Maintain available API/integration credentials, view credential state, select default retention, and manage custom keyword pills.", "Secret values are never displayed as plain text after save; settings status communicates success/failure."),
        ("Custom keywords", "Add/remove organisation-specific detection terms.", "Duplicate/blank entry handling is clear; saved terms influence keyword parsing in subsequent review."),
        ("Exit Session", "Choose Exit Only, Exit and Save, or Exit and Wipe; Cancel closes without action.", "Wipe is visibly destructive and requires confirmation. Exit options must make data-retention consequence clear."),
        ("Demo / sandbox controls", "Optional demo-case generators and the isolated LLM sandbox support demonstrations/testing.", "Demo content is clearly identifiable as demonstration material and does not masquerade as case evidence."),
    ], [1900, 4300, 3400])]

    body += [p("10. Cross-cutting functional rules", "Heading1"), table(["Area", "Requirement"], [
        ("Case scoping", "All searches, collection results, notes, evidence, and exports must clearly indicate and operate within the active case."),
        ("Validation", "Required inputs identify the field and issue in plain language. Invalid dates, unsupported files, and incomplete Watchlist cadence are blocked or explained before save/submit."),
        ("Progress and recovery", "Long-running recon, collection, recognition, and assessment actions show an in-progress state, a completion result, and an understandable failure/retry state."),
        ("Empty states", "Every analysis/review view tells the user whether data is absent, filtered out, pending, or requires a preceding action."),
        ("Auditability", "The user can see relevant case status, updated recency, collection/assessment activity, and deliberately captured evidence. Product refinement should define detailed audit-event policy."),
        ("Accessibility", "Menus, tabs, controls, modals, and status updates support keyboard operation, visible focus, readable labels, and programmatic announcements for loading/status changes."),
        ("Data interpretation", "Discoveries, signal matches, and automated assessment labels are presented as aids for analyst review, not confirmed identity, intent, or risk conclusions."),
    ], [2100, 8100])]

    body += [p("11. Initial user-story backlog", "Heading1"), p("These stories deliberately express outcome and acceptance expectations. Teams may split them further by role, permission model, or release slice."),
             table(["ID", "User story", "Key acceptance criteria"], [
                 ("US-01", "As an analyst, I can create a case so that all investigation activity has a defined container.", "Required case fields validate; created case appears in list and can be opened."),
                 ("US-02", "As a reviewer, I can filter and sort cases so that I can prioritise the right work.", "Search, status, threat, and sort work together; metrics remain consistent."),
                 ("US-03", "As an analyst, I can maintain Watchlist cadence so that ongoing review has an explicit rhythm.", "Cadence is shown/required for Watchlist and persists on edit."),
                 ("US-04", "As an analyst, I can add selectors and run recon so that I can identify leads for review.", "Multiple selectors supported; progress and no-result states are visible; results remain case-scoped."),
                 ("US-05", "As an analyst, I can move recon-ready profiles into collection so that I do not retype targets.", "Transfer is explicit and editable before collection starts."),
                 ("US-06", "As an analyst, I can collect content across a date range so that I can review relevant activity.", "Dates validate; collection status/stream outcomes are visible; results open in active case."),
                 ("US-07", "As an analyst, I can search, sort, and filter content so that I can triage high-value posts.", "Filters combine; clear resets search; empty result explains current filter context."),
                 ("US-08", "As an analyst, I can capture a post as evidence so that it is cited in the case file and report.", "Capture adds analyst note and makes it visible in Cited Posts."),
                 ("US-09", "As an analyst, I can review footprint, timeline, graph, and pattern views so that I can assess relationships and context.", "Views have clear prerequisites and distinguish indications from conclusions."),
                 ("US-10", "As an analyst, I can run and review assistive assessment so that I can triage posts while retaining human judgement.", "Scope/cost/status/coverage visible; output is not framed as a final case conclusion."),
                 ("US-11", "As an analyst, I can save a structured case file and export a report so that the case can be reviewed or handed off.", "Saved fields and cited evidence appear in report; optional sections respect report inclusion choices."),
                 ("US-12", "As an administrator, I can manage retention and keyword defaults so that the workspace follows operating policy.", "Changes are acknowledged; secret fields remain protected; configured keywords affect later review."),
             ], [800, 4800, 4700])]

    body += [p("Appendix A. Screen reference images", "Heading1"), p("The following POC concept captures are included as visual aids for story grooming. They illustrate the intended operational layout and menu groupings; functional requirements in the preceding sections take precedence if a visual detail differs." )]
    for i, (title, path, caption) in enumerate(ASSETS, start=1):
        body += [p(title, "Heading2"), image_paragraph(f"rId{i+2}", str(i), 5943600, 3714750), p(caption, "Caption", italic=True, color="666666", after=240)]
    body.append('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720"/></w:sectPr>')
    document = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><w:body>' + ''.join(body) + '</w:body></w:document>'
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:lang w:val="en-US"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:color w:val="17324D"/><w:sz w:val="42"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:rPr><w:color w:val="3F6788"/><w:sz w:val="28"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:color w:val="17324D"/><w:sz w:val="30"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:color w:val="3F6788"/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:rPr><w:i/><w:color w:val="666666"/><w:sz w:val="18"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:hanging="360"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr></w:style></w:styles>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    docrels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for i in range(3): docrels.append(f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{i+1}.png"/>')
    docrels.append('</Relationships>')
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Orion Functional Specification and User-Story Foundation</dc:title><dc:creator>Codex</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">{date.today().isoformat()}T00:00:00Z</dcterms:created></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office Word</Application></Properties>'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types); z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles); z.writestr('word/_rels/document.xml.rels', ''.join(docrels))
        z.writestr('docProps/core.xml', core); z.writestr('docProps/app.xml', app)
        for i, (_, path, _) in enumerate(ASSETS, start=1): z.write(path, f'word/media/image{i}.png')
    print(OUT)

if __name__ == '__main__': main()
