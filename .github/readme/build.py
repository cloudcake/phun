"""Build the README artwork: the banner, the three feature lists, and a
header per platform. The card per feature group and the tile per feature are
kept for reuse elsewhere; the README no longer shows them.

Run `python3 .github/readme/build.py` from anywhere. The look follows the Phun
app: its dark theme, the infrastructure canvas's dotted ground, rounded cards,
thin orthogonal lines and the brand red. The drawing kit is in art.py, the
feature tiles in tiles.py and the platform headers in platforms.py.
"""
import os

from art import *  # noqa: F401,F403
from art import begin

HERE = os.path.dirname(os.path.abspath(__file__))


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


def around_art():
    out = [rect(700, 34, 516, 232)]
    out.append(f'<circle cx="726" cy="62" r="7" fill="none" stroke="{ART}" stroke-width="1.6"/>')
    out.append(f'<path d="M731 67l5 5" stroke="{ART}" stroke-width="1.8" stroke-linecap="round"/>')
    out.append(text("mono", "blog", 748, 67.5, 14, FG))
    out.append(f'<rect x="{748 + width("mono", "blog", 14) + 2:.1f}" y="53" width="1.5" height="18" fill="{RED}" class="blink"/>')
    out.append(f'<path d="M700 88H1216" stroke="{BORDER}"/>')
    items = (("blog.test", "Open in editor", "Enter"), ("blog.test", "Artisan", ""),
             ("blog.test", "Tinker", ""), ("blog.test", "Console", ""))
    for i, (scope, action, key) in enumerate(items):
        y = 116 + i * 38
        if i == 0:
            out.append(rect(710, y - 21, 496, 32, r=8, fill=hsl(0, 40, 18), stroke=None))
        out.append(text("mono", scope, 726, y, 12, MUTED))
        out.append(text("medium", action, 846, y, 14, FG if i == 0 else SOFT))
        if key:
            kw = width("semibold", key, 11) + 14
            out.append(rect(1196 - kw, y - 15, kw, 20, r=5, fill=INSET))
            out.append(text("semibold", key, 1196 - kw + 7, y - 1, 11, SOFT))
    return "".join(out)


def write(name, svg):
    out = os.path.join(HERE, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        fh.write(svg)
    print(f"{name}: {len(svg) // 1024} KB")


def drawn(fn, *args):
    begin()
    return fn(*args)


def build_banner_and_sections():
    write("banner.svg", drawn(banner))
    sections = (
        ("applications.svg", 1, "Every application on .test", [
            "Link or park a folder and it is served at its own .test",
            "address over trusted HTTPS, with the PHP version it needs.",
        ], "applications_art", "Folders linked to .test addresses over HTTPS."),
        ("services.svg", 2, "PHP and services, natively", [
            "Several PHP versions side by side, with databases, cache,",
            "search, mail and storage beside them. No Docker, no VM.",
        ], "services_art", "An application joined to PHP, databases, cache, mail, search and storage."),
        ("editor.svg", 3, "A code editor that knows Laravel", [
            "Completion from your models and routes, live PHP checks,",
            "refactors, formatting and git, built into the app.",
        ], "editor_art", "The built-in editor with completion and git markers."),
        ("insight.svg", 4, "See what your applications do", [
            "Metrics, every request, logs, terminals, a database",
            "browser and dependency audits, for each application.",
        ], "insight_art", "A request chart and the latest requests with their status."),
        ("around.svg", 5, "Everything around it", [
            "A command palette, themes, an MCP server for AI agents,",
            "the phun command, health checks and self-updates.",
        ], "around_art", "The command palette over a list of Phun's actions."),
    )
    for name, number, title, lines, art_name, desc in sections:
        begin()
        write(name, feature(number, title, lines, globals()[art_name](), desc))


if __name__ == "__main__":
    import sys

    import lists
    import platforms
    import tiles

    only = sys.argv[1:] or ["sections", "tiles", "platforms", "lists"]
    if "sections" in only:
        build_banner_and_sections()
    if "tiles" in only:
        tiles.build_all(write)
    if "platforms" in only:
        platforms.build_all(write)
    if "lists" in only:
        lists.build_all(write)
