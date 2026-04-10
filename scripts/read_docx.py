#!/usr/bin/env python3
"""
Extract plain text from a .docx file using only the Python standard library.

Usage:
    python3 read_docx.py <path-to-docx>

Why stdlib only: the user's system Python (3.9) has no extra packages installed,
and we don't want to make `pip install python-docx` a prerequisite for the skill.
A .docx is just a zip with an XML payload at word/document.xml — we can read
that directly.

The output is plain text, paragraph-separated, with simple heading detection.
It's not a perfect Word renderer — it's a "good enough" extractor for feeding
JD-matching and resume-tailoring logic.
"""

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_text(docx_path: Path) -> str:
    """Read a .docx file and return its text content, paragraph-separated."""
    if not docx_path.exists():
        raise FileNotFoundError(f"file not found: {docx_path}")

    with zipfile.ZipFile(docx_path) as zf:
        try:
            xml_bytes = zf.read("word/document.xml")
        except KeyError:
            raise ValueError(f"not a valid .docx (no word/document.xml): {docx_path}")

    root = ET.fromstring(xml_bytes)
    body = root.find(f"{WORD_NS}body")
    if body is None:
        return ""

    out_lines = []
    for para in body.iter(f"{WORD_NS}p"):
        # Detect heading style — Word stores it in pStyle val
        style_el = para.find(f"{WORD_NS}pPr/{WORD_NS}pStyle")
        is_heading = False
        heading_level = 0
        if style_el is not None:
            style_val = style_el.get(f"{WORD_NS}val", "")
            if style_val.lower().startswith("heading"):
                is_heading = True
                # Heading1, Heading2, etc.
                tail = style_val[7:]
                if tail.isdigit():
                    heading_level = int(tail)
                else:
                    heading_level = 1

        # Concatenate all the runs in this paragraph
        text_parts = []
        for run in para.iter(f"{WORD_NS}t"):
            if run.text:
                text_parts.append(run.text)
        text = "".join(text_parts).strip()

        if not text:
            # preserve paragraph breaks
            out_lines.append("")
            continue

        if is_heading:
            prefix = "#" * max(1, min(heading_level, 6))
            out_lines.append(f"{prefix} {text}")
        else:
            out_lines.append(text)

    # Collapse 3+ blank lines into 2
    cleaned = []
    blank_run = 0
    for line in out_lines:
        if line == "":
            blank_run += 1
            if blank_run <= 2:
                cleaned.append(line)
        else:
            blank_run = 0
            cleaned.append(line)

    return "\n".join(cleaned).strip() + "\n"


def main():
    if len(sys.argv) != 2:
        print("usage: read_docx.py <path-to-docx>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1]).expanduser().resolve()
    try:
        text = extract_text(path)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.stdout.write(text)


if __name__ == "__main__":
    main()
