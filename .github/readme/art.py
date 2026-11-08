"""Shared drawing kit for the README artwork.

Text is drawn as vector outlines from installed system fonts (see FONTS), so
every image looks the same wherever the README is viewed. Each glyph is
defined once per image and reused, which keeps paragraphs small.

Every image is watermarked three ways: a rights notice in its metadata, the
Phun mark woven into the dotted ground, and a small visible Phun mark.
"""
import colorsys

from ttf import Font, contour_path

FONTS = {
    "black": "/usr/share/fonts/truetype/lato/Lato-Black.ttf",
    "bold": "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
    "semibold": "/usr/share/fonts/truetype/lato/Lato-Semibold.ttf",
    "medium": "/usr/share/fonts/truetype/lato/Lato-Medium.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
F = {name: Font(path) for name, path in FONTS.items()}
PREFIX = {"black": "k", "bold": "b", "semibold": "s", "medium": "m", "mono": "o"}

OWNER = "Cloudcake"
SOURCE = "https://github.com/cloudcake/phun"
RIGHTS = f"Phun artwork. Copyright {OWNER}. All rights reserved. Not licensed for use outside {SOURCE}."


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


BG = hsl(225, 21, 7.5)
TILE = hsl(225, 21, 6)
CARD = hsl(222, 18, 11)
INSET = hsl(223, 19, 9)
BORDER = hsl(222, 15, 17.5)
LINE = hsl(222, 15, 26)
ART = hsl(222, 12, 40)
FG = hsl(220, 14, 96)
SOFT = hsl(220, 10, 82)
MUTED = hsl(220, 7, 58)
DIM = hsl(222, 12, 24)
FAINT = hsl(222, 12, 20)
RED = hsl(0, 65, 54)
REDSOFT = hsl(0, 40, 18)
GREEN = hsl(142, 55, 46)
AMBER = hsl(38, 70, 55)
GOLD = hsl(42, 60, 62)
BLUE = hsl(212, 60, 66)
VIOLET = hsl(262, 50, 70)

LOGO = "M78 48H144C204 48 220 80 220 116C220 156 198 188 140 188H114V208H78ZM114 84V152H138C170 152 184 136 184 116C184 96 168 84 138 84Z"

STYLE = """
  .pulse { animation: pulse 2.6s ease-in-out infinite; }
  .pulse.b { animation-delay: .5s; }
  .pulse.c { animation-delay: 1s; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }
  .flow { stroke-dasharray: 4 6; animation: flow 1.6s linear infinite; }
  @keyframes flow { to { stroke-dashoffset: -20; } }
  .blink { animation: blink 1.1s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  .rise { animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }
  @keyframes rise { from { opacity: 0; transform: translateY(8px); } }
  .spin { transform-box: fill-box; transform-origin: center; animation: spin 6s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .bob { animation: bob 3s ease-in-out infinite; }
  @keyframes bob { 50% { transform: translateY(-4px); } }
"""
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"

_glyphs = {}


def begin():
    """Start a new image: forget the glyphs of the previous one."""
    _glyphs.clear()


def _glyph_defs():
    return "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in _glyphs.items())


def text(font, s, x, baseline, size, fill, tracking=0.0, cls="", style=""):
    """`s` as reused glyph outlines starting at `x` on `baseline`."""
    f = F[font]
    k = size / f.units
    pen = 0.0
    uses = []
    for ch in s:
        gid = f.cmap.get(ord(ch), 0)
        contours = f.contours(gid)
        if contours:
            key = f"{PREFIX[font]}{gid}"
            if key not in _glyphs:
                _glyphs[key] = "".join(contour_path(c, 0, 0, 1) for c in contours)
            uses.append(f'<use href="#{key}" x="{round(pen)}"/>')
        pen += f.advance(gid) + tracking / k
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return f'<g fill="{fill}" transform="translate({x:g} {baseline:g}) scale({k:.5f})"{c}{st}>{"".join(uses)}</g>'


def signature_width():
    return 22 + width("bold", "phun", 12)


def width(font, s, size, tracking=0.0):
    f = F[font]
    k = size / f.units
    return sum(f.advance(f.cmap.get(ord(ch), 0)) * k + tracking for ch in s) - (tracking if s else 0)


def wrap(font, s, size, max_width):
    """`s` broken into lines no wider than `max_width`."""
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and width(font, trial, size) > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def rect(x, y, w, h, r=12, fill=CARD, stroke=BORDER, sw=1, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}"{s}{extra}/>'


def bar(x, y, w, h, fill=FAINT, cls="", style=""):
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{h / 2:g}" fill="{fill}"{c}{st}/>'


def dot(cx, cy, r, fill, cls="", style=""):
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}"{c}{st}/>'


def path(d, stroke=ART, sw=1.5, fill="none", cls="", style="", extra=""):
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s}{c}{st}{extra}/>'


def line(points, stroke=LINE, sw=1.5, cls="", r=8, style=""):
    """An orthogonal line with rounded corners, as on the infrastructure canvas."""
    d = f"M{points[0][0]:g} {points[0][1]:g}"
    for i in range(1, len(points)):
        x, y = points[i]
        if i < len(points) - 1:
            px, py = points[i - 1]
            nx, ny = points[i + 1]
            ilen = abs(x - px) + abs(y - py)
            olen = abs(nx - x) + abs(ny - y)
            k = min(r, ilen / 2, olen / 2)
            ax = x - (k if x > px else -k if x < px else 0)
            ay = y - (k if y > py else -k if y < py else 0)
            bx = x + (k if nx > x else -k if nx < x else 0)
            by = y + (k if ny > y else -k if ny < y else 0)
            d += f" L{ax:g} {ay:g} Q{x:g} {y:g} {bx:g} {by:g}"
        else:
            d += f" L{x:g} {y:g}"
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{c}{st}/>'


def padlock(x, y, fill=GREEN):
    return (
        f'<rect x="{x:g}" y="{y + 5:g}" width="8" height="6.5" rx="1.5" fill="{fill}"/>'
        f'<path d="M{x + 1.9:g} {y + 5.2:g}V{y + 3:g}a2.1 2.1 0 0 1 4.2 0V{y + 5.2:g}" fill="none" stroke="{fill}" stroke-width="1.4"/>'
    )


def folder(x, y, stroke=ART):
    return path(f"M{x} {y + 2}h9l3 3h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-24a2 2 0 0 1-2-2v-13a2 2 0 0 1 2-2z", stroke)


def logo(x, y, size, fill=FG, opacity=1.0):
    """The Phun P mark on its own, `size` pixels square, top-left at x, y."""
    o = f' opacity="{opacity:g}"' if opacity != 1 else ""
    return f'<path d="{LOGO}" transform="translate({x:g} {y:g}) scale({size / 256:.5f}) translate(-21 0)" fill="{fill}" fill-rule="evenodd"{o}/>'


def pill(x, y, label, size=14):
    w = width("semibold", label, size)
    return w + 34, (
        rect(x, y, w + 34, 30, r=9)
        + dot(x + 14, y + 15, 3, RED)
        + text("semibold", label, x + 24, y + 20, size, SOFT)
    )


def signature(w, h, corner="br"):
    """The visible watermark: the Phun mark and name, quiet, in one corner,
    or at an (x, y) top-left given as `corner`."""
    tw = width("bold", "phun", 12)
    bw = 16 + 6 + tw
    if isinstance(corner, tuple):
        x, y = corner
    else:
        x = w - 22 - bw if corner.endswith("r") else 22
        y = h - 34 if corner.startswith("b") else 18
    return f'<g opacity=".42">{logo(x, y, 16, MUTED)}{text("bold", "phun", x + 22, y + 12.5, 12, MUTED)}</g>'


def frame(w, h, body, title="", desc="", fade=("0", "0", "1", "0"), fade_from=0.25, css="", r=20, corner="br", mark=True):
    """The dark rounded card on its dotted ground, watermarked."""
    x1, y1, x2, y2 = fade
    sig = signature(w, h, corner) if mark else ""
    defs = _glyph_defs()
    return f'''<!-- {RIGHTS} -->
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
<metadata>
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <rdf:Description rdf:about="{SOURCE}">
      <dc:title>{title}</dc:title>
      <dc:creator>{OWNER}</dc:creator>
      <dc:rights>{RIGHTS}</dc:rights>
      <dc:source>{SOURCE}</dc:source>
    </rdf:Description>
  </rdf:RDF>
</metadata>
<style>{STYLE}{css}
  {REDUCED}
</style>
<defs>
  {defs}
  <clipPath id="card"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
  <pattern id="dots" width="100" height="100" patternUnits="userSpaceOnUse">{_ground()}</pattern>
  <linearGradient id="fade" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}">
    <stop offset="{fade_from}" stop-color="#fff" stop-opacity=".05"/>
    <stop offset="1" stop-color="#fff" stop-opacity=".16"/>
  </linearGradient>
  <mask id="dotmask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
  <radialGradient id="glow"><stop offset="0" stop-color="{RED}" stop-opacity=".22"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#dots)" mask="url(#dotmask)"/>
  {body}
  {sig}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r - .5:g}" fill="none" stroke="{BORDER}"/>
</svg>
'''


def _ground():
    """A 100px tile of the dotted ground with the Phun mark in place of one dot."""
    dots = []
    for row in range(5):
        for col in range(5):
            if (row, col) == (2, 2):
                continue
            dots.append(f'<circle cx="{10 + col * 20}" cy="{10 + row * 20}" r="1" fill="#fff"/>')
    dots.append(logo(46, 46, 8, "#fff"))
    return "".join(dots)
