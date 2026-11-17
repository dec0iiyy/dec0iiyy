#!/usr/bin/env python3
"""Prepares the generated 3D contribution calendars for the README.

The generator draws a language pie beside the calendar. It counts public
repositories only, which says little about the work in private ones, so the
pie is removed. The background also gets the rounded border of the header.

Usage: python3 tools/frame_calendar.py <generated dir> <output dir>
"""
import re
import sys
from pathlib import Path

PIE = '<g transform="translate(40, 520)">'
BACKGROUND = re.compile(r'<rect x="0" y="0" width="1280" height="850" fill="([^"]+)">')
BORDERS = {"calendar-dark.svg": "#313244", "calendar-light.svg": "#ccd0da"}


def without_group(svg: str, opening: str) -> str:
    """`svg` without the group that starts with `opening`, nested groups included."""
    start = svg.find(opening)
    if start < 0 or svg.find(opening, start + 1) >= 0:
        raise ValueError(f"expected exactly one {opening!r}")
    depth, position = 0, start
    for tag in re.finditer(r"<g[\s>]|</g>", svg[start:]):
        depth += -1 if tag.group() == "</g>" else 1
        if depth == 0:
            position = start + tag.end()
            break
    else:
        raise ValueError("the group never closes")
    return svg[:start] + svg[position:]


def framed(svg: str, border: str) -> str:
    """`svg` with a rounded, bordered background instead of a square one."""
    result, count = BACKGROUND.subn(
        rf'<rect x="1" y="1" width="1278" height="848" rx="24" fill="\1" '
        rf'stroke="{border}" stroke-width="2">',
        svg,
        count=1,
    )
    if count != 1:
        raise ValueError("background not found")
    return result


def main() -> None:
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    target.mkdir(parents=True, exist_ok=True)
    for name, border in BORDERS.items():
        svg = (source / name).read_text(encoding="utf-8")
        (target / name).write_text(framed(without_group(svg, PIE), border), encoding="utf-8")
        print(f"wrote {target / name}")


if __name__ == "__main__":
    main()
