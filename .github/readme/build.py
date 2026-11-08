"""Build the README artwork: the banner and one card per feature group.

Run `python3 .github/readme/build.py` from the repository root. Text is drawn
as vector outlines from Lato and DejaVu Sans Mono (installed system fonts, see
FONTS below), so every image looks the same wherever the README is viewed.
The look follows the Phun app: its dark theme, the infrastructure canvas's
dotted ground, rounded cards, thin orthogonal lines and the brand red.
"""
import colorsys
import os

from ttf import Font, text_path, text_width

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = {
    "black": "/usr/share/fonts/truetype/lato/Lato-Black.ttf",
    "bold": "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
    "semibold": "/usr/share/fonts/truetype/lato/Lato-Semibold.ttf",
    "medium": "/usr/share/fonts/truetype/lato/Lato-Medium.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
F = {name: Font(path) for name, path in FONTS.items()}


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
RED = hsl(0, 65, 54)
GREEN = hsl(142, 55, 46)
AMBER = hsl(38, 70, 55)
GOLD = hsl(42, 60, 62)
BLUE = hsl(212, 60, 66)

LOGO = "M78 48H144C204 48 220 80 220 116C220 156 198 188 140 188H114V208H78ZM114 84V152H138C170 152 184 136 184 116C184 96 168 84 138 84Z"

STYLE = """
<style>
  .pulse { animation: pulse 2.6s ease-in-out infinite; }
  .pulse.b { animation-delay: .5s; }
  .pulse.c { animation-delay: 1s; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }
  .flow { stroke-dasharray: 4 6; animation: flow 1.6s linear infinite; }
  @keyframes flow { to { stroke-dashoffset: -20; } }
  @media (prefers-reduced-motion: reduce) { .pulse, .flow { animation: none; } }
</style>
"""


def text(font, s, x, baseline, size, fill, tracking=0.0, cls=""):
    d, _ = text_path(F[font], s, x, baseline, size, tracking)
    c = f' class="{cls}"' if cls else ""
    return f'<path d="{d}" fill="{fill}"{c}/>'


def width(font, s, size, tracking=0.0):
    return text_width(F[font], s, size, tracking)


def rect(x, y, w, h, r=12, fill=CARD, stroke=BORDER, sw=1, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{extra}/>'


def dot(cx, cy, r, fill, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{c}/>'


def line(points, stroke=LINE, sw=1.5, cls="", r=8):
    """An orthogonal line with rounded corners, as on the infrastructure canvas."""
    d = f"M{points[0][0]} {points[0][1]}"
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
            d += f" L{ax} {ay} Q{x} {y} {bx} {by}"
        else:
            d += f" L{x} {y}"
    c = f' class="{cls}"' if cls else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{c}/>'


def padlock(x, y, fill=GREEN):
    return (
        f'<rect x="{x}" y="{y + 5}" width="8" height="6.5" rx="1.5" fill="{fill}"/>'
        f'<path d="M{x + 1.9} {y + 5.2}V{y + 3}a2.1 2.1 0 0 1 4.2 0V{y + 5.2}" fill="none" stroke="{fill}" stroke-width="1.4"/>'
    )


def frame(w, h, body, fade_from=0.25, title="", desc=""):
    """The dark rounded card with the dotted ground fading in from the left."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{STYLE}
<defs>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="20"/></clipPath>
  <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="#fff"/></pattern>
  <linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">
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
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="{BORDER}"/>
</svg>
'''


def pill(x, y, label, size=14):
    w = width("semibold", label, size)
    return w + 34, (
        rect(x, y, w + 34, 30, r=9)
        + dot(x + 14, y + 15, 3, RED)
        + text("semibold", label, x + 24, y + 20, size, SOFT)
    )


def banner():
    W, H = 1280, 400
    body = [f'<circle cx="140" cy="200" r="150" fill="url(#glow)"/>']
    tx, tile = 236, 128
    ty = 136
    body.append(rect(72, ty, tile, tile, r=29, fill=TILE, stroke=BORDER, sw=1.5))
    body.append(f'<path d="{LOGO}" transform="translate(72 {ty}) scale({tile / 256}) translate(-21 0)" fill="{FG}" fill-rule="evenodd"/>')
    body.append(text("black", "Phun", tx, 196, 78, FG, tracking=-1))
    body.append(text("semibold", "Your pocket-sized PHP playground.", tx, 238, 26, SOFT))
    body.append(text("medium", "For macOS, Linux and Windows.", tx, 270, 19, MUTED))
    x = tx
    for label in ("Every application on .test", "Trusted HTTPS", "Databases, cache and mail"):
        w, svg = pill(x, 296, label)
        body.append(svg)
        x += w + 10

    bx, by, bw, bh = 836, 52, 380, 140
    body.append(rect(bx, by, bw, bh))
    for i in range(3):
        body.append(dot(bx + 20 + i * 14, by + 19, 4, DIM))
    body.append(rect(bx + 64, by + 10, bw - 80, 19, r=6, fill=INSET))
    body.append(padlock(bx + 74, by + 13))
    body.append(text("mono", "https://blog.test", bx + 88, by + 24, 11.5, SOFT))
    body.append(f'<path d="M{bx} {by + 39}H{bx + bw}" stroke="{BORDER}"/>')
    body.append(rect(bx + 18, by + 54, 132, 8, r=4, fill=hsl(220, 10, 30), stroke=None))
    for i, w in enumerate((300, 270, 220)):
        body.append(rect(bx + 18, by + 74 + i * 14, w, 5, r=2.5, fill=hsl(222, 12, 20), stroke=None))
    body.append(rect(bx + 18, by + 116, 68, 11, r=5.5, fill=RED, stroke=None))

    sy = 264
    services = (("PHP", "per application"), ("MySQL", "databases"), ("Mail", "captured"))
    centres = []
    for i, (title, sub) in enumerate(services):
        x = 836 + i * 132
        body.append(rect(x, sy, 116, 72))
        body.append(dot(x + 17, sy + 21, 3.5, GREEN, f"pulse {'abc'[i]}"))
        body.append(text("bold", title, x + 28, sy + 26, 15, FG))
        body.append(text("mono", sub, x + 14, sy + 54, 10.5, MUTED))
        centres.append(x + 58)
    hub = 230
    body.append(line([(bx + bw / 2, by + bh), (bx + bw / 2, hub)]))
    body.append(line([(centres[0], sy), (centres[0], hub), (centres[-1], hub), (centres[-1], sy)]))
    body.append(line([(centres[1], hub), (centres[1], sy)]))
    body.append(line([(centres[0], hub), (centres[-1], hub)], stroke=RED, sw=1.5, cls="flow"))
    body.append(dot(bx + bw / 2, hub, 4, RED))
    return frame(W, H, "\n".join(body), title="Phun", desc="Phun, your pocket-sized PHP playground, for macOS, Linux and Windows.")


def feature(number, title, lines, art, desc):
    W, H = 1280, 300
    body = [
        text("mono", f"{number:02d}", 64, 92, 13, RED, tracking=1),
        f'<path d="M92 87.5H120" stroke="{RED}" stroke-width="1.5" stroke-linecap="round"/>',
        text("bold", title, 64, 140, 34, FG, tracking=-0.3),
    ]
    for i, l in enumerate(lines):
        body.append(text("medium", l, 64, 182 + i * 28, 19, MUTED))
    body.append(art)
    return frame(W, H, "\n".join(body), fade_from=0.45, title=title, desc=desc)


def applications_art():
    out = []
    folders = (("blog", "Laravel"), ("shop", "WordPress"), ("docs", "Static site"))
    for i, (name, kind) in enumerate(folders):
        y = 52 + i * 70
        out.append(rect(640, y, 190, 50))
        out.append(f'<path d="M656 {y + 18}h9l3 3h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-24a2 2 0 0 1-2-2v-13a2 2 0 0 1 2-2z" fill="none" stroke="{ART}" stroke-width="1.5" stroke-linejoin="round"/>')
        out.append(text("mono", f"~/Code/{name}", 692, y + 23, 12, SOFT))
        out.append(text("medium", kind, 692, y + 40, 11, MUTED))
        out.append(line([(830, y + 25), (930, y + 25)]))
        out.append(dot(880, y + 25, 3, RED))
        out.append(rect(930, y, 286, 50))
        out.append(padlock(948, y + 19))
        out.append(text("mono", f"https://{name}.test", 964, y + 30, 13, FG))
        out.append(dot(1196, y + 25, 3.5, GREEN, f"pulse {'abc'[i]}"))
    return "".join(out)


def services_art():
    out = [rect(640, 110, 150, 84)]
    out.append(f'<rect x="656" y="128" width="20" height="16" rx="3" fill="none" stroke="{ART}" stroke-width="1.5"/>')
    out.append(text("bold", "Application", 684, 141, 15, FG))
    out.append(text("mono", "blog.test", 656, 176, 11, MUTED))
    names = (("PHP", "FPM pools", GREEN), ("MySQL", "MariaDB, Postgres", GREEN), ("Redis", "cache, queues", GREEN),
             ("Mail", "captured", GREEN), ("Meilisearch", "search", GREEN), ("Storage", "S3 compatible", GREEN))
    for i, (name, sub, pip) in enumerate(names):
        col, row = i % 2, i // 2
        x, y = 880 + col * 172, 34 + row * 80
        out.append(rect(x, y, 156, 62))
        out.append(dot(x + 16, y + 21, 3.5, pip, f"pulse {'abc'[i % 3]}"))
        out.append(text("bold", name, x + 27, y + 26, 14, FG))
        out.append(text("mono", sub, x + 14, y + 47, 10.5, MUTED))
    out.append(line([(790, 152), (836, 152)]))
    out.append(line([(836, 65), (836, 225)]))
    for row in range(3):
        y = 34 + row * 80 + 31
        out.append(line([(836, y), (880, y)]))
    out.append(dot(836, 152, 4, RED))
    return "".join(out)


def editor_art():
    x0, y0, w, h = 640, 30, 576, 240
    out = [rect(x0, y0, w, h)]
    out.append(f'<path d="M{x0} {y0 + 34}H{x0 + w}" stroke="{BORDER}"/>')
    out.append(f'<rect x="{x0 + 1}" y="{y0 + 1}" width="130" height="33" fill="{INSET}"/>')
    out.append(f'<path d="M{x0 + 1} {y0 + 33}H{x0 + 130}" stroke="{RED}" stroke-width="2"/>')
    out.append(text("medium", "Post.php", x0 + 34, y0 + 22, 12, FG))
    out.append(f'<rect x="{x0 + 16}" y="{y0 + 11}" width="10" height="12" rx="2" fill="none" stroke="{ART}" stroke-width="1.3"/>')
    out.append(text("medium", "web.php", x0 + 162, y0 + 22, 12, MUTED))
    code = [
        [("class ", RED), ("Post ", GOLD), ("extends ", RED), ("Model", GOLD)],
        [("{", MUTED)],
        [("    public function ", RED), ("author", BLUE), ("(): ", MUTED), ("BelongsTo", GOLD)],
        [("    {", MUTED)],
        [("        return ", RED), ("$this", SOFT), ("->", MUTED), ("belongsTo", BLUE), ("(", MUTED), ("User", GOLD), ("::class", MUTED), (");", MUTED)],
        [("    }", MUTED)],
        [("}", MUTED)],
    ]
    anchor = (x0 + 356, y0 + 156)
    for i, tokens in enumerate(code):
        y = y0 + 64 + i * 22
        out.append(text("mono", str(i + 7), x0 + 18, y, 11, DIM if i != 4 else MUTED))
        x = x0 + 56
        for s, c in tokens:
            if i == 4 and s == "User":
                anchor = (x - 10, y + 9)
            out.append(text("mono", s, x, y, 12.5, c))
            x += width("mono", s, 12.5)
    out.append(f'<rect x="{x0 + 44}" y="{y0 + 99}" width="3" height="40" rx="1.5" fill="{GREEN}"/>')
    out.append(f'<rect x="{x0 + 44}" y="{y0 + 143}" width="3" height="18" rx="1.5" fill="{AMBER}"/>')
    px, py = anchor
    out.append(rect(px, py, 196, 72, r=8, fill=INSET))
    for i, (name, kind) in enumerate((("User", "App\\Models"), ("UserPolicy", "App\\Policies"))):
        yy = py + 10 + i * 28
        if i == 0:
            out.append(rect(px + 6, yy - 4, 184, 26, r=6, fill=hsl(0, 40, 18), stroke=None))
        out.append(text("mono", name, px + 16, yy + 13, 12, FG))
        out.append(text("mono", kind, px + 108, yy + 13, 10, MUTED))
    return "".join(out)


def insight_art():
    out = [rect(640, 30, 270, 240)]
    out.append(text("mono", "REQUESTS", 660, 58, 10.5, MUTED, tracking=1))
    out.append(dot(653, 54.5, 3, RED))
    pts = [(660, 210), (690, 196), (720, 204), (750, 170), (780, 182), (810, 138), (840, 152), (870, 110), (890, 120)]
    area = "M" + " L".join(f"{x} {y}" for x, y in pts) + " L890 250 L660 250 Z"
    out.append(f'<defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity=".28"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>')
    out.append(f'<path d="{area}" fill="url(#area)"/>')
    out.append(f'<path d="M' + " L".join(f"{x} {y}" for x, y in pts) + f'" fill="none" stroke="{RED}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for gy in (110, 170, 230):
        out.append(f'<path d="M660 {gy}H890" stroke="{BORDER}" stroke-dasharray="2 4"/>')
    out.append(rect(930, 30, 286, 240))
    out.append(text("mono", "LATEST", 950, 58, 10.5, MUTED, tracking=1))
    rows = (("GET", "/", "200", "12ms", GREEN), ("POST", "/login", "302", "41ms", BLUE), ("GET", "/api/posts", "200", "18ms", GREEN), ("GET", "/missing", "404", "6ms", AMBER), ("PUT", "/posts/7", "200", "33ms", GREEN))
    for i, (m, path, status, ms, c) in enumerate(rows):
        y = 92 + i * 34
        if i:
            out.append(f'<path d="M946 {y - 22}H1200" stroke="{BORDER}"/>')
        out.append(text("mono", m, 950, y, 11.5, SOFT))
        out.append(text("mono", path, 996, y, 11.5, FG))
        out.append(text("mono", status, 1118, y, 11.5, c))
        out.append(text("mono", ms, 1160, y, 11.5, MUTED))
    return "".join(out)


def write(name, svg):
    path = os.path.join(HERE, name)
    with open(path, "w") as fh:
        fh.write(svg)
    print(f"{name}: {len(svg) // 1024} KB")


if __name__ == "__main__":
    write("banner.svg", banner())
    write("applications.svg", feature(1, "Every application on .test", [
        "Link or park a folder and it is served at its own .test",
        "address over trusted HTTPS, with the PHP version it needs.",
    ], applications_art(), "Folders linked to .test addresses over HTTPS."))
    write("services.svg", feature(2, "PHP and services, natively", [
        "Several PHP versions side by side, with databases, cache,",
        "search, mail and storage beside them. No Docker, no VM.",
    ], services_art(), "An application joined to PHP, databases, cache, mail, search and storage."))
    write("editor.svg", feature(3, "A code editor that knows Laravel", [
        "Completion from your models and routes, live PHP checks,",
        "refactors, formatting and git, built into the app.",
    ], editor_art(), "The built-in editor with completion and git markers."))
    write("insight.svg", feature(4, "See what your applications do", [
        "Metrics, every request, logs, terminals, captured mail",
        "and a database browser, for each application.",
    ], insight_art(), "A request chart and the latest requests with their status."))
