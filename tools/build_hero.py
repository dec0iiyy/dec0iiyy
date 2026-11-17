#!/usr/bin/env python3
"""Draws the profile header: an editor window with Kotlin code, a phone
running a Compose screen, and packets travelling from it to network nodes.
Writes assets/hero-dark.svg and assets/hero-light.svg.

Usage: python3 tools/build_hero.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH, HEIGHT = 1200, 470
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

# Catppuccin Mocha and Latte.
THEMES = {
    "dark": dict(
        base="#1e1e2e", mantle="#181825", crust="#11111b", surface0="#313244",
        surface1="#45475a", overlay0="#6c7086", overlay2="#9399b2", text="#cdd6f4",
        subtext="#a6adc8", mauve="#cba6f7", blue="#89b4fa", green="#a6e3a1",
        yellow="#f9e2af", peach="#fab387", red="#f38ba8", teal="#94e2d5",
        glow="0.24",
    ),
    "light": dict(
        base="#eff1f5", mantle="#e6e9ef", crust="#dce0e8", surface0="#ccd0da",
        surface1="#bcc0cc", overlay0="#9ca0b0", overlay2="#7c7f93", text="#4c4f69",
        subtext="#6c6f85", mauve="#8839ef", blue="#1e66f5", green="#40a02b",
        yellow="#df8e1d", peach="#fe640b", red="#d20f39", teal="#179299",
        glow="0.15",
    ),
}

DOT = "·"
# (token class, text) per line; an empty list is a blank line.
CODE = [
    [("c", f"// Android engineer {DOT} 3+ years in production")],
    [("k", "class"), ("n", " "), ("t", "Dec0iiyy"), ("o", " : "), ("t", "AndroidDeveloper"), ("o", "(), "),
     ("t", "RustContributor"), ("o", " {")],
    [],
    [("n", "    "), ("k", "val"), ("p", " languages"), ("o", " = "), ("f", "listOf"), ("o", "("),
     ("s", '"Kotlin"'), ("o", ", "), ("s", '"Rust"'), ("o", ")")],
    [("n", "    "), ("k", "val"), ("p", " ui"), ("o", " = "), ("f", "listOf"), ("o", "("),
     ("s", '"Jetpack Compose"'), ("o", ", "), ("s", '"Material 3"'), ("o", ")")],
    [("n", "    "), ("k", "val"), ("p", " concurrency"), ("o", " = "), ("s", '"Coroutines + Flow"')],
    [("n", "    "), ("k", "val"), ("p", " architecture"), ("o", " = "),
     ("s", f'"MVI {DOT} Clean {DOT} multi-module"')],
    [("n", "    "), ("k", "val"), ("p", " multiplatform"), ("o", " = "), ("s", '"KMP: Android + iOS"')],
    [("n", "    "), ("k", "val"), ("p", " networking"), ("o", " = "),
     ("s", f'"Rust: TLS {DOT} QUIC {DOT} DNS"')],
    [],
    [("n", "    "), ("k", "suspend fun"), ("f", " ship"), ("o", "() = "), ("f", "build"), ("o", "()."),
     ("f", "test"), ("o", "()."), ("f", "release"), ("o", "()")],
    [("o", "}")],
]

CODE_X, FIRST_BASELINE, LINE_HEIGHT, FONT_SIZE = 86, 94, 30, 19
COVER_WIDTH = 676
SECONDS_PER_CHAR, LINE_GAP = 0.013, 0.1

PHONE = (776, 86, 164, 314)
# The protocols the packets go to, each with the accent of the card it serves.
NODES = (("TLS", "blue"), ("QUIC", "green"), ("DNS", "peach"))
NODE_X, NODE_WIDTH, NODE_HEIGHT = 1052, 112, 36


def code_lines(theme):
    """The code, one <text> per line, with a cover that uncovers it as if typed."""
    parts, start = [], 0.35
    for index, tokens in enumerate(CODE):
        baseline = FIRST_BASELINE + index * LINE_HEIGHT
        parts.append(
            f'<text class="ln" x="58" y="{baseline}" text-anchor="end">{index + 1}</text>'
        )
        if not tokens:
            continue
        spans = "".join(f'<tspan class="{cls}">{escape(text)}</tspan>' for cls, text in tokens)
        parts.append(f'<text class="code" x="{CODE_X}" y="{baseline}" xml:space="preserve">{spans}</text>')
        chars = sum(len(text) for _, text in tokens)
        duration = max(chars * SECONDS_PER_CHAR, 0.1)
        parts.append(
            f'<rect class="cover" x="{CODE_X - 8}" y="{baseline - 22}" width="{COVER_WIDTH}" '
            f'height="{LINE_HEIGHT}" fill="{theme["base"]}" style="animation-duration:{duration:.2f}s;'
            f'animation-delay:{start:.2f}s;animation-timing-function:steps({chars},end)"/>'
        )
        start += duration + LINE_GAP
    caret_y = FIRST_BASELINE + (len(CODE) - 1) * LINE_HEIGHT - 17
    parts.append(
        f'<rect class="caret" x="{CODE_X + 18}" y="{caret_y}" width="10" height="21" rx="2" '
        f'fill="{theme["mauve"]}" style="animation-delay:{start:.2f}s"/>'
    )
    return "\n".join(parts)


def card_centre(index):
    """Where the phone's list card `index` sits, vertically."""
    return PHONE[1] + 8 + 80 + index * 60 + 25


def phone(theme):
    """A phone with a list screen: top bar, chips, three cards, a button, a nav bar."""
    x, y, w, h = PHONE
    sx, sy, sw, sh = x + 8, y + 8, w - 16, h - 16
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="{theme["crust"]}" '
        f'stroke="{theme["surface1"]}" stroke-width="1.5"/>',
        f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="23" fill="{theme["mantle"]}"/>',
        f'<circle cx="{x + w / 2}" cy="{sy + 11}" r="3.5" fill="{theme["crust"]}"/>',
        # Top app bar.
        f'<rect x="{sx + 14}" y="{sy + 30}" width="64" height="10" rx="5" fill="{theme["text"]}"/>',
        f'<circle cx="{sx + sw - 22}" cy="{sy + 35}" r="9" fill="url(#kotlin)"/>',
    ]
    # Filter chips.
    chip_x = sx + 14
    for index, (chip_w, fill) in enumerate(((40, theme["mauve"]), (30, theme["surface0"]), (34, theme["surface0"]))):
        out.append(
            f'<rect class="chip" x="{chip_x}" y="{sy + 54}" width="{chip_w}" height="14" rx="7" '
            f'fill="{fill}" style="animation-delay:{0.5 + index * 0.1:.2f}s"/>'
        )
        chip_x += chip_w + 6
    # List cards, one per network node.
    for index, (_, accent) in enumerate(NODES):
        cy = sy + 80 + index * 60
        delay = 0.75 + index * 0.22
        out.append(
            f'<g class="card" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{sx + 10}" y="{cy}" width="{sw - 20}" height="50" rx="12" fill="{theme["surface0"]}"/>'
            f'<circle cx="{sx + 31}" cy="{cy + 25}" r="11" fill="{theme[accent]}"/>'
            f'<rect class="shimmer" x="{sx + 50}" y="{cy + 15}" width="{62 - index * 8}" height="7" rx="3.5" '
            f'fill="{theme["text"]}" style="animation-delay:{index * 0.4:.1f}s"/>'
            f'<rect class="shimmer" x="{sx + 50}" y="{cy + 29}" width="{40 + index * 6}" height="7" rx="3.5" '
            f'fill="{theme["overlay0"]}" style="animation-delay:{0.2 + index * 0.4:.1f}s"/>'
            f"</g>"
        )
    # Floating action button with a pulse behind it.
    fx, fy = sx + sw - 50, sy + sh - 84
    out += [
        f'<rect class="pulse" x="{fx}" y="{fy}" width="38" height="38" rx="12" fill="url(#kotlin)"/>',
        f'<rect x="{fx}" y="{fy}" width="38" height="38" rx="12" fill="url(#kotlin)"/>',
        f'<path d="M{fx + 19} {fy + 11}v16M{fx + 11} {fy + 19}h16" stroke="#ffffff" stroke-width="2.6" '
        f'stroke-linecap="round"/>',
    ]
    # Navigation bar.
    nav_y = sy + sh - 34
    out.append(f'<rect x="{sx}" y="{nav_y}" width="{sw}" height="34" fill="{theme["crust"]}" opacity="0.55"/>')
    out.append(f'<rect x="{sx + 20}" y="{nav_y + 10}" width="34" height="14" rx="7" fill="{theme["mauve"]}" opacity="0.35"/>')
    for index in range(3):
        fill = theme["mauve"] if index == 0 else theme["overlay0"]
        out.append(f'<circle cx="{sx + 37 + index * 37}" cy="{nav_y + 17}" r="4.5" fill="{fill}"/>')
    return f'<g clip-path="url(#phone)">{"".join(out)}</g>'


def network(theme):
    """Three protocol nodes and the packets that travel between them and the phone."""
    x, _, w, _ = PHONE
    start_x = x + w + 6
    first_y = card_centre(0) - 62
    out = [
        f'<text class="ui" x="{NODE_X + NODE_WIDTH / 2}" y="{first_y - 34}" font-size="13" '
        f'text-anchor="middle" fill="{theme["overlay0"]}">Rust {DOT} networking</text>'
    ]
    for index, (label, accent) in enumerate(NODES):
        from_y = card_centre(index)
        to_y = first_y + index * 122
        link = (
            f"M{start_x} {from_y}C{start_x + 52} {from_y} {NODE_X - 54} {to_y} {NODE_X} {to_y}"
        )
        out.append(
            f'<path id="link{index}" d="{link}" fill="none" stroke="{theme["surface1"]}" '
            f'stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>'
        )
        # A request out and an answer back, hidden wherever animation is off.
        for back, radius, fill, offset in ((False, 4, theme[accent], 0.0), (True, 3, theme["text"], 1.25)):
            direction = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if back else ""
            out.append(
                f'<circle class="packet" r="{radius}" fill="{fill}" opacity="0">'
                f'<set attributeName="opacity" to="{0.75 if back else 1}" begin="0s"/>'
                f'<animateMotion dur="2.5s" begin="-{offset + index * 0.55:.2f}s" repeatCount="indefinite"{direction}>'
                f'<mpath href="#link{index}" xlink:href="#link{index}"/></animateMotion></circle>'
            )
        out.append(
            f'<rect x="{NODE_X}" y="{to_y - NODE_HEIGHT / 2}" width="{NODE_WIDTH}" height="{NODE_HEIGHT}" '
            f'rx="{NODE_HEIGHT / 2}" fill="{theme["surface0"]}" stroke="{theme["surface1"]}"/>'
            f'<circle cx="{NODE_X + 20}" cy="{to_y}" r="5.5" fill="{theme[accent]}"/>'
            f'<text x="{NODE_X + 36}" y="{to_y + 5.5}" font-size="16" fill="{theme["text"]}">{label}</text>'
        )
    return "".join(out)


def build(name):
    theme = THEMES[name]
    px, py, pw, ph = PHONE
    status_y = HEIGHT - 36
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="hero-title hero-desc">
<title id="hero-title">dec0iiyy: Android engineer and Rust contributor</title>
<desc id="hero-desc">An editor window with a Kotlin class that lists Kotlin and Rust, Jetpack Compose, coroutines, MVI, Kotlin Multiplatform and networking in Rust. Next to it, a phone shows a list screen and exchanges packets with TLS, QUIC and DNS nodes.</desc>
<defs>
<linearGradient id="kotlin" x1="0" y1="1" x2="1" y2="0">
<stop offset="0" stop-color="#7F52FF"/><stop offset="0.5" stop-color="#C711E1"/><stop offset="1" stop-color="#E44857"/>
</linearGradient>
<radialGradient id="glow">
<stop offset="0" stop-color="{theme["mauve"]}" stop-opacity="{theme["glow"]}"/>
<stop offset="1" stop-color="{theme["mauve"]}" stop-opacity="0"/>
</radialGradient>
<clipPath id="window"><rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="20"/></clipPath>
<clipPath id="phone"><rect x="{px - 1}" y="{py - 1}" width="{pw + 2}" height="{ph + 2}" rx="31"/></clipPath>
</defs>
<style>
text {{ font-family: {MONO}; }}
.ui {{ font-family: {SANS}; }}
.code {{ font-size: {FONT_SIZE}px; fill: {theme["text"]}; }}
.ln {{ font-size: 15px; fill: {theme["overlay0"]}; }}
.k {{ fill: {theme["mauve"]}; }}
.t {{ fill: {theme["yellow"]}; }}
.f {{ fill: {theme["blue"]}; }}
.s {{ fill: {theme["green"]}; }}
.p {{ fill: {theme["text"]}; }}
.o {{ fill: {theme["overlay2"]}; }}
.c {{ fill: {theme["overlay0"]}; font-style: italic; }}
.cover {{ transform-box: fill-box; transform-origin: 100% 50%; transform: scaleX(0);
  animation-name: type; animation-fill-mode: backwards; }}
.caret {{ animation: blink 1.1s steps(1, end) infinite backwards; }}
.card {{ animation: rise 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; }}
.chip {{ animation: fade 0.5s ease-out backwards; }}
.shimmer {{ animation: shimmer 2.4s ease-in-out infinite alternate; }}
.pulse {{ transform-box: fill-box; transform-origin: center; opacity: 0;
  animation: pulse 2.6s ease-out 2s infinite; }}
@keyframes type {{ from {{ transform: scaleX(1); }} to {{ transform: scaleX(0); }} }}
@keyframes blink {{ 0% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes shimmer {{ from {{ opacity: 1; }} to {{ opacity: 0.55; }} }}
@keyframes pulse {{ 0% {{ opacity: 0.45; transform: scale(1); }} 70%, 100% {{ opacity: 0; transform: scale(1.7); }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .packet {{ display: none; }} }}
</style>
<g clip-path="url(#window)">
<rect width="{WIDTH}" height="{HEIGHT}" fill="{theme["base"]}"/>
<rect width="{WIDTH}" height="52" fill="{theme["mantle"]}"/>
<circle cx="34" cy="26" r="7" fill="{theme["red"]}"/>
<circle cx="58" cy="26" r="7" fill="{theme["yellow"]}"/>
<circle cx="82" cy="26" r="7" fill="{theme["green"]}"/>
<path d="M118 52V22a10 10 0 0 1 10-10h176a10 10 0 0 1 10 10v30z" fill="{theme["base"]}"/>
<path d="M138 23h16l-8 8 8 8h-16z" fill="url(#kotlin)"/>
<text class="ui" x="166" y="37" font-size="15" fill="{theme["text"]}">Developer.kt</text>
<circle cx="346" cy="31" r="6" fill="none" stroke="{theme["peach"]}" stroke-width="3"/>
<text class="ui" x="362" y="37" font-size="15" fill="{theme["overlay2"]}">net.rs</text>
<text class="ui" x="{WIDTH - 30}" y="32" font-size="14" text-anchor="end" fill="{theme["overlay0"]}">github.com/dec0iiyy</text>
{code_lines(theme)}
<circle cx="{px + pw + 40}" cy="{py + ph / 2}" r="270" fill="url(#glow)"/>
{network(theme)}
{phone(theme)}
<rect y="{status_y}" width="{WIDTH}" height="36" fill="{theme["mantle"]}"/>
<rect x="18" y="{status_y + 7}" width="70" height="22" rx="11" fill="{theme["blue"]}"/>
<text class="ui" x="53" y="{status_y + 23}" font-size="13" font-weight="600" text-anchor="middle" fill="{theme["base"]}">main</text>
<circle cx="108" cy="{status_y + 18}" r="4.5" fill="{theme["green"]}"/>
<text class="ui" x="120" y="{status_y + 23}" font-size="13" fill="{theme["subtext"]}">build passing</text>
<text class="ui" x="{WIDTH - 30}" y="{status_y + 23}" font-size="13" text-anchor="end" fill="{theme["subtext"]}">Kotlin + Rust {DOT} UTF-8</text>
</g>
<rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="20" fill="none" stroke="{theme["surface0"]}" stroke-width="1.5"/>
</svg>
'''


def main():
    assets = Path(__file__).resolve().parent.parent / "assets"
    assets.mkdir(exist_ok=True)
    for name in THEMES:
        (assets / f"hero-{name}.svg").write_text(build(name), encoding="utf-8")
        print(f"wrote assets/hero-{name}.svg")


if __name__ == "__main__":
    main()
