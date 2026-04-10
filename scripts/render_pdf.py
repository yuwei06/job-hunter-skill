#!/usr/bin/env python3
"""
Render a tailored resume markdown file to PDF using typst.

Usage:
    python3 render_pdf.py <path-to-resume.md>

Why typst: it's a single binary (`brew install typst`), renders CJK out of the
box on macOS using PingFang/Songti, has no LaTeX-style toolchain pain, and
produces a clean modern resume in well under a second.

Why not pandoc: pandoc requires a TeX distribution for PDF output, and a
working TeX with CJK fonts is a 2GB install plus configuration. typst is ~50MB
and just works.

This script reads a markdown resume (the format described in
references/resume-tailoring.md) and pipes structured data into the typst
template at assets/resume.template.typ. It's intentionally a thin wrapper —
the formatting decisions live in the .typ file, not here.
"""

import sys
import shutil
import subprocess
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE = SKILL_DIR / "assets" / "resume.template.typ"


def check_typst() -> str:
    """Locate the typst binary or print a helpful error and exit."""
    typst = shutil.which("typst")
    if not typst:
        print(
            "error: typst is not installed.\n"
            "  install with:  brew install typst\n"
            "  why typst: single binary, CJK-friendly, no LaTeX needed.\n",
            file=sys.stderr,
        )
        sys.exit(1)
    return typst


def parse_markdown(md_text: str) -> dict:
    """
    Parse a tailored resume markdown into a structured dict the typst template
    can consume. The expected structure is documented in
    references/resume-tailoring.md.

    This is a permissive parser — it doesn't fail on minor format drift. If a
    section is missing, it just becomes an empty list / string. The typst
    template handles missing fields gracefully.
    """
    lines = md_text.splitlines()
    data = {
        "name": "",
        "title": "",
        "contact": "",
        "summary": "",
        "experience": [],
        "projects": [],
        "skills": "",
        "education": "",
    }

    # H1 is "name · title"
    section = None
    current_block = []
    current_item = None

    def flush_item():
        nonlocal current_item
        if current_item is not None:
            if section == "experience":
                data["experience"].append(current_item)
            elif section == "projects":
                data["projects"].append(current_item)
        current_item = None

    def flush_block():
        nonlocal current_block
        text = "\n".join(current_block).strip()
        current_block = []
        return text

    for raw in lines:
        line = raw.rstrip()

        # H1 — header line, e.g. "# Name · Title"
        if line.startswith("# ") and not line.startswith("## "):
            header = line[2:].strip()
            # split on · or | or whitespace dash
            parts = re.split(r"\s*[·\|]\s*", header, maxsplit=1)
            data["name"] = parts[0].strip()
            data["title"] = parts[1].strip() if len(parts) > 1 else ""
            continue

        # H2 — top-level section
        if line.startswith("## "):
            # close out previous section
            if section == "summary":
                data["summary"] = flush_block()
            elif section == "skills":
                data["skills"] = flush_block()
            elif section == "education":
                data["education"] = flush_block()
            elif section in ("experience", "projects"):
                flush_item()

            heading = line[3:].strip()
            if any(k in heading for k in ("个人概述", "概述", "Summary", "About")):
                section = "summary"
            elif any(k in heading for k in ("工作经历", "Experience", "工作经验")):
                section = "experience"
            elif any(k in heading for k in ("项目经验", "项目经历", "Projects")):
                section = "projects"
            elif any(k in heading for k in ("技术栈", "技能", "Skills")):
                section = "skills"
            elif any(k in heading for k in ("教育", "Education")):
                section = "education"
            else:
                section = None
            continue

        # H3 — item within experience or projects
        if line.startswith("### "):
            flush_item()
            current_item = {"heading": line[4:].strip(), "meta": "", "bullets": []}
            continue

        # contact line — first non-empty line right after the H1
        if not data["contact"] and data["name"] and not line.startswith("#") and line.strip() and section is None:
            data["contact"] = line.strip()
            continue

        # bullets within an item
        if current_item is not None and (line.startswith("- ") or line.startswith("* ")):
            current_item["bullets"].append(line[2:].strip())
            continue

        # meta line for an item — first bold line right after H3
        if current_item is not None and line.strip().startswith("**") and not current_item["meta"]:
            current_item["meta"] = re.sub(r"\*\*", "", line).strip()
            continue

        # block content (summary, skills, education)
        if section in ("summary", "skills", "education"):
            current_block.append(line)
            continue

    # final flush
    if section == "summary":
        data["summary"] = flush_block()
    elif section == "skills":
        data["skills"] = flush_block()
    elif section == "education":
        data["education"] = flush_block()
    flush_item()

    return data


def to_typst_string(s: str) -> str:
    """Escape a string for embedding inside typst source as a string literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def emit_typst_data(data: dict) -> str:
    """Convert the parsed dict into typst variable assignments at the top of a doc."""
    parts = []
    parts.append(f'#let resume-name = "{to_typst_string(data["name"])}"')
    parts.append(f'#let resume-title = "{to_typst_string(data["title"])}"')
    parts.append(f'#let resume-contact = "{to_typst_string(data["contact"])}"')
    parts.append(f'#let resume-summary = "{to_typst_string(data["summary"])}"')
    parts.append(f'#let resume-skills = "{to_typst_string(data["skills"])}"')
    parts.append(f'#let resume-education = "{to_typst_string(data["education"])}"')

    def emit_items(name, items):
        out = [f"#let {name} = ("]
        for item in items:
            out.append("  (")
            out.append(f'    heading: "{to_typst_string(item["heading"])}",')
            out.append(f'    meta: "{to_typst_string(item["meta"])}",')
            out.append("    bullets: (")
            for b in item["bullets"]:
                out.append(f'      "{to_typst_string(b)}",')
            out.append("    ),")
            out.append("  ),")
        out.append(")")
        return "\n".join(out)

    parts.append(emit_items("resume-experience", data["experience"]))
    parts.append(emit_items("resume-projects", data["projects"]))
    return "\n".join(parts)


def main():
    if len(sys.argv) != 2:
        print("usage: render_pdf.py <path-to-resume.md>", file=sys.stderr)
        sys.exit(2)

    md_path = Path(sys.argv[1]).expanduser().resolve()
    if not md_path.exists():
        print(f"error: file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    if not TEMPLATE.exists():
        print(f"error: template missing: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    typst = check_typst()

    md_text = md_path.read_text(encoding="utf-8")
    data = parse_markdown(md_text)
    data_block = emit_typst_data(data)

    # Build a one-shot typst document: data block + import + render call.
    template_content = TEMPLATE.read_text(encoding="utf-8")
    full_doc = data_block + "\n\n" + template_content

    # Write to a temp .typ next to the resume.md so debugging is easy
    typ_path = md_path.with_suffix(".typ")
    typ_path.write_text(full_doc, encoding="utf-8")

    pdf_path = md_path.with_suffix(".pdf")
    result = subprocess.run(
        [typst, "compile", str(typ_path), str(pdf_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("typst compile failed:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print(f"rendered: {pdf_path}")


if __name__ == "__main__":
    main()
