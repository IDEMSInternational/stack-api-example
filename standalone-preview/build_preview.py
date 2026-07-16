#!/usr/bin/env python3
# =============================================================================
# standalone-preview/build_preview.py
# Authored with Claude (Anthropic). This whole file is Claude-generated.
# =============================================================================
"""Build a self-contained interactive STACK preview HTML from a question XML.

The output is ONE .html file the author can double-click. On open it asks a
CORS-enabled STACK API to render the question, validate inputs live, and grade
submissions — all from the author's browser. Claude never calls the API; this
script only stamps the (offline) XML into the template.

Usage:
    python3 build_preview.py QUESTION.xml [-o OUT.html] [--api URL] [--title T]

Defaults:
    -o     : QUESTION-preview.html next to the input
    --api  : https://stack-api.maths.ed.ac.uk   (Edinburgh public demo; CORS-enabled)
    --title: the <name> of the STACK question, else the file stem

Notes:
  * The template lives at preview_template.html next to this script.
  * The whole question XML is base64-embedded, so the preview needs no sibling
    files and works from file:// (browsers block fetch() of local files, so we
    must NOT rely on fetching the .xml at runtime).
  * The XML must contain <deployedseed> entries for randomised questions, or the
    API returns "no deployed variants". The authoring workflow emits these.
"""
from __future__ import annotations  # so "str | None" annotations work on Python 3.7–3.9

import argparse
import base64
import re
import sys
from pathlib import Path

DEFAULT_API = "https://stack-api.maths.ed.ac.uk"


def question_name(xml: str) -> str | None:
    # First <name><text>...</text></name> — the question's name.
    m = re.search(r"<name>\s*<text>(.*?)</text>\s*</name>", xml, re.DOTALL)
    return m.group(1).strip() if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a STACK preview HTML from a question XML.")
    ap.add_argument("xml", help="Path to the Moodle/STACK question XML.")
    ap.add_argument("-o", "--out", help="Output HTML path (default: <xml>-preview.html).")
    ap.add_argument("--api", default=DEFAULT_API,
                    help=f"STACK API base URL (default: {DEFAULT_API}).")
    ap.add_argument("--title", help="Title shown in the preview (default: question name).")
    ap.add_argument("--template",
                    help="Override template path (default: preview-template.html).")
    args = ap.parse_args()

    xml_path = Path(args.xml)
    if not xml_path.is_file():
        print(f"error: no such file: {xml_path}", file=sys.stderr)
        return 1
    xml = xml_path.read_text(encoding="utf-8")

    if "type=\"stack\"" not in xml and "type='stack'" not in xml:
        print("warning: no <question type=\"stack\"> found — is this a STACK export?",
              file=sys.stderr)

    tmpl_path = Path(args.template) if args.template \
        else Path(__file__).resolve().parent / "preview_template.html"
    if not tmpl_path.is_file():
        print(f"error: template not found: {tmpl_path}", file=sys.stderr)
        return 1
    template = tmpl_path.read_text(encoding="utf-8")

    title = args.title or question_name(xml) or xml_path.stem
    b64 = base64.b64encode(xml.encode("utf-8")).decode("ascii")

    # Order matters: inject b64 (large) via a plain replace on the exact token.
    html = (template
            .replace("{{API_URL}}", args.api.rstrip("/"))
            .replace("{{TITLE}}", _html_escape(title))
            .replace("{{QUESTION_B64}}", b64))

    out_path = Path(args.out) if args.out else xml_path.with_name(xml_path.stem + "-preview.html")
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote {out_path}")
    if "<deployedseed>" not in xml:
        print("note: no <deployedseed> in the XML. A randomised question needs deployed "
              "seeds or the API will report 'no deployed variants'.", file=sys.stderr)
    return 0


def _html_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


if __name__ == "__main__":
    raise SystemExit(main())
