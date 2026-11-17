#!/usr/bin/env python3
"""Prepares the generated 3D contribution calendars for the README.

The generator draws a language pie beside the calendar. It counts public
repositories only, which says little about the work in private ones, so the
pie is removed, and so are the star and fork totals. The background also gets
the rounded border of the header.

Usage: python3 tools/frame_calendar.py <generated dir> <output dir>
"""
import re
import sys
from pathlib import Path

PIE = '<g transform="translate(40, 520)">'
# The first rectangle that spans the whole 1280 x 850 canvas, however its
# attributes are ordered: its attributes, then how the tag closes.
BACKGROUND = re.compile(r'<rect\b((?=[^>]*\bwidth="1280")(?=[^>]*\bheight="850")[^>]*?)(/?>)')
ATTRIBUTE = re.compile(r'([\w:-]+)="([^"]*)"')
# An icon drawn at double size on the totals line, and the number after it.
COUNTER = re.compile(
    r'<g transform="translate\(\d+, 802\), scale\(2\)">.*?</g>'
    r"<text[^>]*>\d+<title>\d+</title></text>",
    re.S,
)
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


def without_repository_counters(svg: str) -> str:
    """`svg` without the star and fork totals under the calendar: it is about
    contributions, and the README's own card carries the numbers."""
    result, count = COUNTER.subn("", svg)
    if count != 2:
        raise ValueError(f"expected the star and the fork counter, found {count}")
    return result


def framed(svg: str, border: str) -> str:
    """`svg` with a rounded, bordered background instead of a square one."""
    background = BACKGROUND.search(svg)
    if background is None:
        raise ValueError("background not found")
    attributes = dict(ATTRIBUTE.findall(background.group(1)))
    attributes.update(
        {"x": "1", "y": "1", "width": "1278", "height": "848", "rx": "24",
         "stroke": border, "stroke-width": "2"}
    )
    rect = "<rect " + " ".join(f'{name}="{value}"' for name, value in attributes.items())
    return svg[: background.start()] + rect + background.group(2) + svg[background.end():]


def main() -> None:
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    target.mkdir(parents=True, exist_ok=True)
    for name, border in BORDERS.items():
        svg = (source / name).read_text(encoding="utf-8")
        svg = without_repository_counters(without_group(svg, PIE))
        (target / name).write_text(framed(svg, border), encoding="utf-8")
        print(f"wrote {target / name}")


if __name__ == "__main__":
    main()
