"""One animated tile per feature, two to a row in the README.

Each tile is a drawing of the feature over its own text: a section label, a
title and the description, which rise in when the image loads. Every
drawing moves a little, and none of it moves with reduced motion on.
"""
from art import (
    AMBER, ART, BG, BLUE, BORDER, CARD, DIM, FAINT, FG, GOLD, GREEN, INSET, LINE, MUTED, RED, REDSOFT,
    SOFT, VIOLET, bar, begin, dot, folder, frame, hsl, line, padlock, path, rect, signature,
    signature_width, text, width, wrap,
)

W, H = 640, 400
BODY_SIZE, BODY_LEAD, BODY_WIDTH = 17, 24, 568

TILE_CSS = """
  .cyc { opacity: 0; animation: cyc var(--p, 8s) infinite; }
  .grow { transform-box: fill-box; transform-origin: left; animation: grow 3.4s ease-in-out infinite; }
  @keyframes grow { 0% { transform: scaleX(0); } 60%, 100% { transform: scaleX(1); } }
  .type { transform-box: fill-box; transform-origin: right; animation: type 5s steps(24) infinite; }
  @keyframes type { 0% { transform: scaleX(1); } 55%, 100% { transform: scaleX(0); } }
  .appear { animation: appear 6s ease-out infinite both; }
  @keyframes appear { 0%, 8% { opacity: 0; transform: translateY(5px); } 16%, 88% { opacity: 1; transform: none; } 96%, 100% { opacity: 0; } }
  .draw { stroke-dasharray: 100; animation: draw 5s ease-in-out infinite; }
  @keyframes draw { 0% { stroke-dashoffset: 100; } 55%, 100% { stroke-dashoffset: 0; } }
  .ride { animation: ride 4.8s linear infinite both; }
  @keyframes ride { 0% { transform: translateX(0); opacity: 0; } 10%, 85% { opacity: 1; } 100% { transform: translateX(var(--d, 240px)); opacity: 0; } }
  .knob { animation: knob 3.2s ease-in-out infinite; }
  @keyframes knob { 0%, 40% { transform: translateX(0); } 50%, 90% { transform: translateX(12px); } 100% { transform: translateX(0); } }
  .swap-a { animation: swapa 6s infinite; }
  .swap-b { animation: swapb 6s infinite; }
  @keyframes swapa { 0%, 46% { opacity: 1; } 50%, 96% { opacity: 0; } 100% { opacity: 1; } }
  @keyframes swapb { 0%, 46% { opacity: 0; } 50%, 96% { opacity: 1; } 100% { opacity: 0; } }
  .scan { animation: scan 2.4s ease-in-out infinite; }
  @keyframes scan { 0% { transform: translateX(0); } 100% { transform: translateX(var(--d, 400px)); } }
"""


def cycle_css(n, hold=0.9):
    """Keyframes that light item i of n for its share of the period."""
    share = 100 / n
    return (
        f"@keyframes cyc {{ 0% {{ opacity: 0; }} {share * 0.06:.2f}% {{ opacity: 1; }} "
        f"{share * hold:.2f}% {{ opacity: 1; }} {share:.2f}%, 100% {{ opacity: 0; }} }}"
    )


def cyc(i, n, period):
    return f"--p: {period}s; animation-delay: {i * period / n - period:.2f}s"


def rise(svg, delay):
    return f'<g class="rise" style="animation-delay: {delay:.2f}s">{svg}</g>'


def tile(number, section, title, body, draw, n_cycle=4):
    """A finished tile: `draw()` makes the art, then the text goes under it."""
    begin()
    art = draw()
    lines = wrap("medium", body, BODY_SIZE, BODY_WIDTH)
    if len(lines) > 3:
        raise ValueError(f"{title}: the description runs to {len(lines)} lines")
    label = (
        text("mono", f"{number:02d}", 36, 256, 12, RED, tracking=1)
        + path("M62 251.5H80", RED)
        + text("mono", section.upper(), 90, 256, 11, MUTED, tracking=1.2)
    )
    out = [art, rise(label, 0.1), rise(text("bold", title, 36, 292, 25, FG, tracking=-0.2), 0.18)]
    for i, l in enumerate(lines):
        out.append(rise(text("medium", l, 36, 326 + i * BODY_LEAD, BODY_SIZE, MUTED), 0.26 + i * 0.07))
    out.append(signature(W, H, (W - 36 - signature_width(), 244)))
    css = TILE_CSS + "  " + cycle_css(n_cycle) + "\n"
    return frame(W, H, "\n".join(out), title=title, desc=body, fade=("0", "1", "0", "0"), fade_from=0.42, css=css, r=18, mark=False)


def keycap(x, y, label, size=10.5):
    w = width("semibold", label, size) + 14
    return w, rect(x, y, w, 20, r=5, fill=INSET) + text("semibold", label, x + 7, y + 14, size, SOFT)


def chip(x, y, label, size=11, fill=INSET, color=MUTED, h=22, font="medium"):
    w = width(font, label, size) + 18
    return w, rect(x, y, w, h, r=7, fill=fill) + text(font, label, x + 9, y + h / 2 + size * 0.36, size, color)


def window(x, y, w, h, tabs=(), active=0):
    """An editor-like card with a tab strip."""
    out = [rect(x, y, w, h)]
    if tabs:
        out.append(path(f"M{x} {y + 30}H{x + w}", BORDER, 1))
        tx = x + 1
        for i, t in enumerate(tabs):
            tw = width("medium", t, 11.5) + 40
            if i == active:
                out.append(f'<rect x="{tx}" y="{y + 1}" width="{tw}" height="29" fill="{INSET}"/>')
                out.append(path(f"M{tx} {y + 29}H{tx + tw}", RED, 2))
            out.append(f'<rect x="{tx + 12}" y="{y + 10}" width="8" height="10" rx="1.5" fill="none" stroke="{ART}" stroke-width="1.2"/>')
            out.append(text("medium", t, tx + 26, y + 19.5, 11.5, FG if i == active else MUTED))
            tx += tw
    return "".join(out)


def code(x, y, tokens_per_line, size=12, lead=22, first=1, numbers=True, num_x=None):
    """Coloured code: a list of lines, each a list of (text, colour)."""
    out = []
    for i, tokens in enumerate(tokens_per_line):
        yy = y + i * lead
        if numbers:
            out.append(text("mono", str(first + i), num_x if num_x is not None else x - 34, yy, size - 1.5, DIM))
        xx = x
        for s, c in tokens:
            out.append(text("mono", s, xx, yy, size, c))
            xx += width("mono", s, size)
    return "".join(out)


def end_of(x, tokens, size=12):
    return x + sum(width("mono", s, size) for s, _ in tokens)


def check(cx, cy, color=GREEN, r=7):
    return dot(cx, cy, r, color) + path(f"M{cx - 3} {cy}l2.2 2.3 4-4.6", BG, 1.6)


def globe(cx, cy, r=8, stroke=ART):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="1.4"/>'
        + path(f"M{cx - r} {cy}H{cx + r}M{cx} {cy - r}c-{r * .55} {r * .5}-{r * .55} {r * 1.5} 0 {r * 2}M{cx} {cy - r}c{r * .55} {r * .5} {r * .55} {r * 1.5} 0 {r * 2}", stroke, 1.2)
    )


# --- Applications -----------------------------------------------------------

def link_park():
    o = [rect(36, 30, 224, 180), folder(52, 42), text("bold", "~/Code", 88, 58, 14, FG)]
    w, c = chip(186, 41, "Parked", 11)
    o.append(c)
    o.append(path("M36 78H260", BORDER, 1))
    for i, name in enumerate(("blog", "shop", "docs")):
        y = 104 + i * 38
        o.append(folder(52, y - 11))
        o.append(text("mono", name, 88, y + 4, 13, SOFT))
        o.append(text("mono", "public/", 244 - width("mono", "public/", 11), y + 4, 11, DIM))
        o.append(line([(260, y), (360, y)]))
        o.append(line([(260, y), (360, y)], RED, 1.5, "flow", style=f"animation-delay: {i * .3:.1f}s"))
        o.append(rect(360, y - 17, 244, 34, r=9))
        o.append(padlock(375, y - 7))
        o.append(text("mono", f"https://{name}.test", 391, y + 4.5, 12.5, FG))
        o.append(dot(588, y, 3.5, GREEN, f"pulse {'abc'[i]}"))
    return "".join(o)


def https():
    o = []
    cards = (
        (36, "Phun Local CA", "trusted root"),
        (236, "blog.test", "signed certificate"),
    )
    for x, title, sub in cards:
        o.append(rect(x, 80, 170, 80))
    o.append(f'<circle cx="62" cy="106" r="10" fill="none" stroke="{ART}" stroke-width="1.5"/>')
    o.append(path("M56 114l-3 11 6-3 3 5 2-9M68 114l3 11-6-3", ART, 1.3))
    o.append(text("bold", "Phun Local CA", 82, 111, 14, FG))
    o.append(text("mono", "trusted root", 52, 146, 11, MUTED))
    o.append(path("M254 94h16l6 6v18h-22z", ART, 1.4))
    o.append(path("M259 106h11M259 112h8", ART, 1.2))
    o.append(text("bold", "blog.test", 284, 111, 14, FG))
    o.append(text("mono", "signed certificate", 252, 146, 11, MUTED))
    o.append(rect(436, 80, 168, 80))
    for i in range(3):
        o.append(dot(450 + i * 10, 94, 3, DIM))
    o.append(rect(446, 106, 148, 22, r=6, fill=INSET))
    o.append(padlock(454, 109))
    o.append(text("mono", "https://blog.test", 468, 121, 11, SOFT))
    o.append(check(456, 145, GREEN, 6))
    o.append(text("semibold", "Secure connection", 468, 149.5, 11.5, GREEN))
    for x in (206, 406):
        o.append(line([(x, 120), (x + 30, 120)]))
        o.append(line([(x, 120), (x + 30, 120)], RED, 1.5, "flow"))
    o.append(f'<circle cx="520" cy="58" r="12" fill="{GREEN}" opacity=".18" class="pulse"/>')
    o.append(path("M520 46l9 4v6c0 6-4 10-9 12-5-2-9-6-9-12v-6z", GREEN, 1.5))
    o.append(path("M516 57l3 3 5-6", GREEN, 1.5))
    x = 36
    for label in ("Always on", "Every .test name", "No browser warnings"):
        w, c = chip(x, 180, label, 11.5, fill=CARD, color=SOFT)
        o.append(c)
        x += w + 8
    return "".join(o)


def php_per_app():
    o = []
    colours = (BLUE, VIOLET, GOLD)
    for i, name in enumerate(("blog.test", "shop.test", "legacy.test")):
        y = 62 + i * 58
        o.append(rect(36, y - 22, 344, 44))
        o.append(globe(58, y))
        o.append(text("mono", name, 76, y + 4.5, 13, FG))
        o.append(rect(262, y - 13, 106, 26, r=7, fill=INSET))
        o.append(dot(276, y, 3.5, colours[i]))
        o.append(text("semibold", "PHP", 285, y + 4.5, 12, SOFT))
        o.append(bar(316, y - 3, 26, 6, DIM))
        o.append(path(f"M350 {y - 2}l4 4 4-4", MUTED, 1.4))
    o.append(line([(368, 120), (404, 120)], LINE))
    o.append(rect(404, 34, 200, 172, r=10, fill=INSET))
    opts = (BLUE, VIOLET, GOLD, GREEN)
    for i, c in enumerate(opts):
        y = 58 + i * 38
        o.append(f'<rect x="412" y="{y - 15}" width="184" height="30" rx="7" fill="{REDSOFT}" class="cyc" style="{cyc(i, 4, 6)}"/>')
        o.append(dot(430, y, 4, c))
        o.append(text("semibold", "PHP", 442, y + 4.5, 12.5, FG))
        o.append(bar(476, y - 3, 34 + (i % 2) * 8, 6, DIM))
        if i == 1:
            o.append(path(f"M574 {y}l3.5 3.5 6.5-7", GREEN, 1.8))
    return "".join(o)


def new_app():
    o = []
    kinds = ("Laravel", "WordPress", "CodeIgniter", "CakePHP", "Slim", "Static site", "HTML app", "Git repository")
    for i, k in enumerate(kinds):
        x, y = 36 + (i % 4) * 143, 36 + (i // 4) * 88
        o.append(rect(x, y, 136, 78))
        o.append(rect(x + 14, y + 14, 28, 28, r=7, fill=INSET))
        if k == "Git repository":
            o.append(dot(x + 23, y + 21, 2.5, ART) + dot(x + 23, y + 35, 2.5, ART) + dot(x + 33, y + 25, 2.5, ART))
            o.append(path(f"M{x + 23} {y + 23.5}V{y + 32.5}M{x + 33} {y + 27.5}c0 5-10 3-10 5", ART, 1.3))
        elif k in ("Static site", "HTML app"):
            o.append(path(f"M{x + 23} {y + 23}l-4 5 4 5M{x + 33} {y + 23}l4 5-4 5", ART, 1.5))
        else:
            o.append(text("bold", k[0], x + 28 - width("bold", k[0], 15) / 2, y + 33.5, 15, SOFT))
        o.append(text("semibold", k, x + 14, y + 63, 13, FG))
        o.append(f'<rect x="{x}" y="{y}" width="136" height="78" rx="12" fill="{RED}" fill-opacity=".08" stroke="{RED}" stroke-width="1.5" class="cyc" style="{cyc(i, 8, 9.6)}"/>')
    return "".join(o)


def domains():
    o = []
    rows = (
        ("blog.test", "host", "PHP-FPM", GREEN),
        ("*.blog.test", "wildcard", "PHP-FPM", GREEN),
        ("blog.test/reverb", "path", "localhost:8080", BLUE),
        ("vite.test", "proxy", "localhost:5173", BLUE),
    )
    for i, (src, kind, dst, c) in enumerate(rows):
        y = 50 + i * 42
        o.append(rect(36, y - 17, 254, 34, r=9))
        o.append(globe(56, y, 7))
        o.append(text("mono", src, 72, y + 4.5, 12.5, FG))
        o.append(text("mono", kind, 278 - width("mono", kind, 10.5), y + 4, 10.5, DIM))
        o.append(line([(290, y), (370, y)]))
        o.append(line([(290, y), (370, y)], RED, 1.5, "flow", style=f"animation-delay: {i * .25:.2f}s"))
        o.append(rect(370, y - 17, 234, 34, r=9, fill=INSET))
        o.append(dot(388, y, 3.5, c, f"pulse {'abcab'[i]}"))
        o.append(text("mono", dst, 400, y + 4.5, 12.5, SOFT))
    return "".join(o)


def share():
    o = [rect(36, 92, 160, 56), globe(58, 120), text("mono", "blog.test", 74, 124.5, 13, FG)]
    cloud = "M276 136h52a14 14 0 0 0 2-28 20 20 0 0 0-38-6 14 14 0 0 0-16 34z"
    o.append(f'<circle cx="303" cy="118" r="34" fill="url(#glow)"/>')
    o.append(path(cloud, SOFT, 1.6))
    o.append(text("medium", "Cloudflare Tunnel", 303 - width("medium", "Cloudflare Tunnel", 11) / 2, 164, 11, MUTED))
    o.append(line([(196, 120), (268, 120)]))
    o.append(line([(196, 120), (268, 120)], RED, 1.5, "flow"))
    o.append(line([(338, 120), (370, 120), (370, 54), (404, 54)]))
    o.append(line([(370, 120), (370, 154), (404, 154)]))
    o.append(line([(338, 120), (370, 120), (370, 54), (404, 54)], RED, 1.5, "flow"))
    o.append(rect(404, 30, 200, 48, r=10))
    o.append(globe(424, 54, 7))
    o.append(text("mono", "https://", 438, 58, 11.5, SOFT))
    o.append(bar(496, 51, 56, 6, DIM))
    w, c = chip(560, 43, "Copy", 10.5, color=SOFT)
    o.append(c)
    devices = (("Phone", "phone"), ("Demo", "laptop"), ("Webhook", "hook"))
    for i, (label, kind) in enumerate(devices):
        x = 404 + i * 69
        o.append(rect(x, 112, 62, 84, r=10))
        cx = x + 31
        if kind == "phone":
            o.append(rect(cx - 9, 128, 18, 30, r=4, fill="none", stroke=ART, sw=1.4) + bar(cx - 3, 153, 6, 2, ART))
        elif kind == "laptop":
            o.append(rect(cx - 13, 131, 26, 18, r=2.5, fill="none", stroke=ART, sw=1.4) + path(f"M{cx - 17} 154h34", ART, 1.6))
        else:
            o.append(path(f"M{cx - 4} 132a6 6 0 1 1 6 9l-6 10M{cx - 8} 152a6 6 0 1 1 3-11M{cx + 8} 152h-11", ART, 1.4))
        o.append(dot(cx, 168, 2.5, GREEN, f"pulse {'abc'[i]}"))
        o.append(text("medium", label, cx - width("medium", label, 10.5) / 2, 186, 10.5, MUTED))
    return "".join(o)


def no_admin():
    o = [rect(56, 30, 528, 180)]
    for i in range(3):
        o.append(dot(74 + i * 13, 48, 4, DIM))
    o.append(rect(124, 38, 444, 22, r=7, fill=INSET))
    url = "http://localhost/~blog.test"
    tw = width("mono", url, 12)
    o.append(text("mono", url, 138, 53.5, 12, FG))
    o.append(f'<rect x="136" y="41" width="{tw + 4:.1f}" height="16" fill="{INSET}" class="type"/>')
    o.append(f'<rect x="{138 + tw + 2:.1f}" y="43" width="1.5" height="13" fill="{RED}" class="blink"/>')
    o.append(path("M56 70H584", BORDER, 1))
    o.append(bar(80, 92, 160, 10, hsl(220, 10, 30)))
    for i, w in enumerate((420, 380, 300)):
        o.append(bar(80, 116 + i * 16, w, 6, FAINT))
    o.append(bar(80, 172, 84, 16, RED))
    w, c = chip(404, 168, "No admin rights needed", 11.5, fill=CARD, color=SOFT, h=26)
    o.append(c)
    return "".join(o)


def infrastructure():
    o = [rect(36, 92, 140, 56), rect(52, 110, 18, 14, r=3, fill="none", stroke=ART, sw=1.4), text("bold", "blog.test", 78, 122, 13.5, FG)]
    services = (("MySQL", 52), ("Redis", 120), ("Storage", 188))
    for i, (name, y) in enumerate(services):
        o.append(rect(226, y - 22, 140, 44))
        o.append(dot(244, y, 3.5, GREEN, f"pulse {'abc'[i]}"))
        o.append(text("bold", name, 256, y + 4.5, 13, FG))
        o.append(line([(201, 120), (201, y), (226, y)]))
    o.append(line([(176, 120), (201, 120)]))
    o.append(dot(201, 120, 3.5, RED))
    o.append(rect(400, 30, 204, 180, fill=INSET))
    o.append(text("mono", ".env", 416, 52, 11, MUTED))
    env = ("DB_CONNECTION=mysql", "DB_PORT=3306", "REDIS_HOST=127.0.0.1", "FILESYSTEM_DISK=s3")
    for i, e in enumerate(env):
        y = 84 + i * 30
        o.append(f'<g class="appear" style="animation-delay: {i * .5:.1f}s">{text("mono", "+", 416, y, 11.5, GREEN)}{text("mono", e, 432, y, 11.5, SOFT)}</g>')
    o.append(line([(366, 120), (400, 120)]))
    o.append(line([(366, 120), (400, 120)], RED, 1.5, "flow"))
    return "".join(o)


# --- PHP and services -------------------------------------------------------

def switch(x, y, on=True, animated=False):
    knob_x = x + 7 + (12 if on and not animated else 0)
    track = rect(x, y, 26, 14, r=7, fill=GREEN if on else DIM, stroke=None)
    k = f'<circle cx="{knob_x}" cy="{y + 7}" r="5" fill="{FG}"{" class=\"knob\"" if animated else ""}/>'
    if animated:
        track = f'<rect x="{x}" y="{y}" width="26" height="14" rx="7" fill="{GREEN}" class="swap-b"/><rect x="{x}" y="{y}" width="26" height="14" rx="7" fill="{DIM}" class="swap-a"/>'
    return track + k


def php_versions():
    o = []
    for i, c in enumerate((BLUE, VIOLET, GOLD)):
        x = 36 + i * 118
        o.append(rect(x, 22, 110, 26, r=8, fill=INSET if i == 0 else CARD))
        o.append(dot(x + 15, 35, 3.5, c))
        o.append(text("semibold", "PHP", x + 25, 39.5, 12, FG if i == 0 else MUTED))
        o.append(bar(x + 56, 32, 26 + (i % 2) * 6, 6, DIM))
        if i == 0:
            o.append(path(f"M{x + 10} 47H{x + 100}", RED, 2))
    o.append(rect(36, 56, 568, 154))
    o.append(dot(56, 80, 4, BLUE))
    o.append(text("bold", "PHP", 68, 85, 15, FG))
    o.append(bar(104, 77, 30, 7, DIM))
    w, c = chip(144, 69, "Default", 10.5, color=SOFT)
    o.append(c)
    o.append(path("M36 100H604", BORDER, 1))
    o.append(path("M318 100V210", BORDER, 1))
    o.append(text("mono", "PHP.INI", 52, 122, 10, MUTED, tracking=1))
    for i, (k, v) in enumerate((("memory_limit", "512M"), ("upload_max_filesize", "64M"), ("max_execution_time", "60"))):
        y = 148 + i * 24
        o.append(text("mono", k, 52, y, 11.5, MUTED))
        o.append(text("mono", v, 302 - width("mono", v, 11.5), y, 11.5, FG))
    o.append(text("mono", "EXTENSIONS", 334, 122, 10, MUTED, tracking=1))
    for i, (ext, on, anim) in enumerate((("mbstring", True, False), ("opcache", True, False), ("redis", False, True))):
        y = 148 + i * 24
        o.append(text("mono", ext, 334, y, 11.5, SOFT))
        o.append(switch(564, y - 11, on, anim))
    return "".join(o)


def native_services():
    o = []
    svc = (("MySQL", "database"), ("MariaDB", "database"), ("PostgreSQL", "database"),
           ("MongoDB", "documents"), ("Redis", "cache, queues"), ("Meilisearch", "search"))
    for i, (name, sub) in enumerate(svc):
        x, y = 36 + (i % 3) * 194, 40 + (i // 3) * 88
        o.append(rect(x, y, 180, 74))
        o.append(dot(x + 18, y + 22, 3.5, GREEN, f"pulse {'abc'[i % 3]}"))
        o.append(text("bold", name, x + 30, y + 27, 14, FG))
        o.append(text("mono", sub, x + 16, y + 56, 11, MUTED))
        o.append(text("medium", "running", x + 166 - width("medium", "running", 10.5), y + 56, 10.5, GREEN))
    return "".join(o)


def mail():
    o = [rect(36, 30, 222, 180)]
    msgs = (("Welcome to Blog", "hello@blog.test"), ("Reset your password", "no-reply@blog.test"), ("Your invoice #1042", "billing@shop.test"))
    for i, (subj, frm) in enumerate(msgs):
        y = 38 + i * 58
        inner = (
            rect(44, y, 206, 52, r=9, fill=INSET if i == 0 else CARD, stroke=BORDER if i == 0 else None)
            + dot(62, y + 26, 10, DIM)
            + text("semibold", subj, 80, y + 22, 12, FG)
            + text("mono", frm, 80, y + 39, 10, MUTED)
        )
        if i == 0:
            inner += dot(238, y + 14, 3.5, RED)
            o.append(f'<g class="appear">{inner}</g>')
        else:
            o.append(inner)
    o.append(rect(272, 30, 332, 180))
    tabs = ("Rendered", "Text", "Source")
    tx = 290
    for i, t in enumerate(tabs):
        tw = width("medium", t, 12)
        o.append(text("medium", t, tx, 54, 12, SOFT))
        o.append(f'<rect x="{tx}" y="62" width="{tw:.1f}" height="2" fill="{RED}" class="cyc" style="{cyc(i, 3, 9)}"/>')
        tx += tw + 22
    o.append(path("M272 66H604", BORDER, 1))
    rendered = (
        bar(292, 84, 70, 10, RED) + bar(292, 106, 200, 8, hsl(220, 10, 30))
        + bar(292, 124, 280, 5, FAINT) + bar(292, 136, 250, 5, FAINT) + bar(292, 148, 270, 5, FAINT)
        + rect(292, 166, 96, 24, r=6, fill=RED, stroke=None) + bar(308, 176, 64, 4, "#fff")
    )
    plain = "".join(bar(292, 86 + i * 16, w, 5, FAINT) for i, w in enumerate((240, 280, 200, 260, 160, 220)))
    source = "".join(
        text("mono", s, 292, 90 + i * 20, 10.5, c)
        for i, (s, c) in enumerate((("MIME-Version: 1.0", MUTED), ("From: hello@blog.test", MUTED), ("Subject: Welcome to Blog", SOFT),
                                    ("Content-Type: text/html", MUTED), ("<h1>Welcome</h1>", BLUE), ("<a href=\"...\">", BLUE)))
    )
    for i, g in enumerate((rendered, plain, source)):
        o.append(f'<g class="cyc" style="{cyc(i, 3, 9)}">{g}</g>')
    return "".join(o)


def storage():
    o = [rect(36, 60, 180, 56), globe(58, 88), text("mono", "blog.test", 74, 92.5, 13, FG)]
    o.append(rect(36, 132, 226, 50, r=10, fill=INSET))
    o.append(text("mono", "Storage::put($path,", 50, 153, 11, SOFT))
    o.append(text("mono", "  $file);", 50, 170, 11, SOFT))
    o.append(line([(216, 88), (280, 88), (280, 120), (300, 120)]))
    o.append(line([(262, 157), (280, 157), (280, 120)]))
    o.append(line([(216, 88), (280, 88), (280, 120), (300, 120)], RED, 1.5, "flow"))
    o.append(rect(300, 30, 304, 180))
    o.append(path("M318 46h20l-2 18h-16z", ART, 1.4))
    o.append(path("M317 46c0-3 22-3 22 0", ART, 1.4))
    o.append(text("bold", "uploads", 348, 60, 14, FG))
    w, c = chip(530, 44, "Private", 10.5, color=SOFT)
    o.append(f'<g class="swap-a">{c}</g>')
    w, c = chip(536, 44, "Public", 10.5, color=GREEN)
    o.append(f'<g class="swap-b">{c}</g>')
    o.append(path("M300 78H604", BORDER, 1))
    rows = (("photos/beach.jpg", "1.2 MB"), ("avatars/7.png", "24 KB"), ("invoices/1042.pdf", "88 KB"), ("exports/report.csv", "3 KB"))
    for i, (name, size) in enumerate(rows):
        y = 102 + i * 28
        g = (path(f"M316 {y - 9}h8l4 4v9h-12z", ART, 1.2)
             + text("mono", name, 338, y + 3.5, 11.5, FG if i == 0 else SOFT)
             + text("mono", size, 588 - width("mono", size, 11), y + 3.5, 11, MUTED))
        o.append(f'<g class="appear">{g}</g>' if i == 0 else g)
    return "".join(o)


def laravel_workers():
    o = []
    rows = (("Queue workers", "3 running"), ("Scheduler", "every minute"), ("Reverb", "WebSockets"))
    for i, (name, sub) in enumerate(rows):
        y = 30 + i * 62
        o.append(rect(36, y, 568, 54))
        o.append(text("bold", name, 82, y + 24, 14, FG))
        o.append(text("mono", sub, 82, y + 41, 11, MUTED))
    o.append(path("M52 47h20M52 52h20M52 57h20", ART, 1.6))
    o.append(path("M318 57H588", LINE, 1))
    for j in range(5):
        o.append(f'<rect x="318" y="50" width="14" height="14" rx="3" fill="{AMBER if j == 2 else GREEN}" class="ride" style="--d: 256px; animation-delay: {-j * .96:.2f}s"/>')
    o.append(f'<circle cx="62" cy="119" r="10" fill="none" stroke="{ART}" stroke-width="1.5"/>')
    o.append(f'<path d="M62 119V112" stroke="{RED}" stroke-width="1.6" stroke-linecap="round" class="spin" style="transform-origin: 62px 119px; transform-box: view-box"/>')
    for k in range(12):
        x = 318 + k * 24
        o.append(path(f"M{x} 112V126", LINE if k % 4 else ART, 1.2))
    o.append(f'<rect x="316" y="108" width="4" height="22" rx="2" fill="{RED}" class="ride" style="--d: 268px; animation-duration: 12s"/>')
    o.append(dot(62, 181, 3, RED))
    for k, cls in enumerate(("pulse", "pulse b", "pulse c")):
        r = 7 + k * 5
        o.append(path(f"M{62 + r * .7:.1f} {181 - r * .7:.1f}a{r} {r} 0 0 1 0 {r * 1.4:.1f}", RED if k == 0 else ART, 1.4, cls=cls))
    for k in range(4):
        x = 360 + k * 62
        o.append(line([(320, 181), (x, 181)], LINE, 1) if k == 0 else "")
        o.append(rect(x, 169, 44, 24, r=7, fill=INSET))
        o.append(dot(x + 14, 181, 3, GREEN, f"pulse {'abcab'[k]}"))
        o.append(bar(x + 21, 179, 14, 4, DIM))
    o.append(line([(320, 181), (604 - 10, 181)], RED, 1.2, "flow"))
    return "".join(o)


def dev_tools():
    o = []
    tools = (("Composer", "composer"), ("Node.js", "node, npm, npx"), ("Bun", "bun"),
             ("NVM", "nvm"), ("Laravel installer", "laravel"), ("WP-CLI", "wp"))
    for i, (name, cmd) in enumerate(tools):
        x, y = 36 + (i % 2) * 290, 34 + (i // 2) * 62
        o.append(rect(x, y, 278, 54))
        o.append(f'<circle cx="{x + 26}" cy="{y + 27}" r="14" fill="{INSET}" stroke="{BORDER}"/>')
        o.append(text("bold", name[0], x + 26 - width("bold", name[0], 13) / 2, y + 31.5, 13, SOFT))
        o.append(text("bold", name, x + 50, y + 24, 13.5, FG))
        o.append(text("mono", cmd, x + 50, y + 41, 11, MUTED))
        if name == "Bun":
            o.append(bar(x + 186, y + 34, 76, 5, DIM))
            o.append(bar(x + 186, y + 34, 76, 5, AMBER, "grow"))
            o.append(text("medium", "Installing", x + 262 - width("medium", "Installing", 10.5), y + 24, 10.5, AMBER))
        else:
            lab = "Installed"
            o.append(dot(x + 262 - width("medium", lab, 10.5) - 8, y + 23, 3, GREEN))
            o.append(text("medium", lab, x + 262 - width("medium", lab, 10.5), y + 27, 10.5, GREEN))
    return "".join(o)


# --- Editor -----------------------------------------------------------------

def highlighting():
    o = []
    langs = ("PHP", "Blade", "JavaScript", "TypeScript", "Vue", "HTML", "CSS", "Sass", "JSON", "YAML", "Markdown", "Shell", ".env")
    x, y = 36, 30
    spots = []
    for l in langs:
        w = width("medium", l, 11.5) + 20
        if x + w > 604:
            x, y = 36, y + 30
        spots.append((x, y, w, l))
        x += w + 6
    for i, (x, y, w, l) in enumerate(spots):
        o.append(rect(x, y, w, 24, r=7, fill=CARD))
        o.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="24" rx="7" fill="{RED}" fill-opacity=".1" stroke="{RED}" class="cyc" style="{cyc(i, len(spots), 13)}"/>')
        o.append(text("medium", l, x + 10, y + 16, 11.5, SOFT))
    o.append(window(36, 98, 568, 112, ("index.blade.php",)))
    o.append(code(84, 150, [
        [("@foreach", RED), (" (", MUTED), ("$posts", SOFT), (" as ", RED), ("$post", SOFT), (")", MUTED)],
        [("    <x-card", BLUE), (" :title", GOLD), ("=", MUTED), ('"$post->title"', GREEN), (" />", BLUE)],
        [("@endforeach", RED)],
    ], size=12, lead=20, num_x=52))
    return "".join(o)


def completion():
    o = [window(36, 26, 568, 184, ("PostController.php",))]
    l1 = [("$post", SOFT), (" = ", MUTED), ("Post", GOLD), ("::", MUTED), ("findOrFail", BLUE), ("(", MUTED), ("$id", SOFT), (");", MUTED)]
    l2 = [("return ", RED), ("$post", SOFT), ("->", MUTED)]
    o.append(code(84, 82, [l1, l2], size=12.5, lead=24, first=14, num_x=52))
    cx = end_of(84, l2, 12.5)
    o.append(f'<rect x="{cx + 1:.1f}" y="94" width="1.5" height="15" fill="{RED}" class="blink"/>')
    px, py = cx - 6, 116
    items = (("title", "string", "p"), ("author", "BelongsTo", "r"), ("comments", "HasMany", "r"), ("published_at", "datetime", "p"))
    o.append(rect(px, py, 268, 86, r=8, fill=INSET))
    for i, (name, kind, k) in enumerate(items):
        y = py + 6 + i * 19
        o.append(f'<rect x="{px + 4:.1f}" y="{y}" width="260" height="18" rx="5" fill="{REDSOFT}" class="cyc" style="{cyc(i, 4, 6)}"/>')
        o.append(rect(px + 10, y + 3, 12, 12, r=3, fill=BLUE if k == "p" else VIOLET, stroke=None))
        o.append(text("bold", k, px + 13.5, y + 12.5, 9, BG))
        o.append(text("mono", name, px + 30, y + 13, 11.5, FG))
        o.append(text("mono", kind, px + 256 - width("mono", kind, 10.5), y + 13, 10.5, MUTED))
    return "".join(o)


def squiggle(x1, x2, y):
    d = f"M{x1:.1f} {y}"
    x, up = x1, True
    while x < x2:
        d += f" q1.5 {-2.5 if up else 2.5} 3 0"
        x += 3
        up = not up
    return path(d, RED, 1.2)


def problems():
    o = [window(36, 26, 568, 184, ("Post.php",))]
    lines = [
        [("public function ", RED), ("summary", BLUE), ("(): ", MUTED), ("string", GOLD)],
        [("{", MUTED)],
        [("    return ", RED), ("Str", GOLD), ("::", MUTED), ("limit", BLUE), ("(", MUTED), ("$this", SOFT), ("->", MUTED), ("body", SOFT), (", ", MUTED), ("$lenght", SOFT), (");", MUTED)],
        [("}", MUTED)],
    ]
    o.append(code(84, 78, lines, size=12, lead=21, first=21, num_x=52))
    bad_x = end_of(84, lines[2][:9], 12)
    bad_w = width("mono", "$lenght", 12)
    o.append(squiggle(bad_x, bad_x + bad_w, 124))
    o.append(dot(46, 116, 3.5, RED, "pulse"))
    tx = bad_x - 30
    o.append(rect(tx, 134, 226, 30, r=7, fill=INSET))
    o.append(dot(tx + 14, 149, 3.5, RED))
    o.append(text("medium", "Undefined variable $lenght", tx + 24, 153, 12, FG))
    o.append(path("M36 184H604", BORDER, 1))
    o.append(dot(54, 197, 3.5, RED))
    o.append(text("medium", "1 problem", 64, 201, 11.5, SOFT))
    w, c = keycap(546, 187, "F2")
    o.append(c)
    o.append(text("medium", "next", 540 - width("medium", "next", 11), 201, 11, MUTED))
    return "".join(o)


def navigate():
    o = [window(36, 26, 268, 118, ("PostController.php",))]
    l1 = [("use ", RED), ("App\\Models\\", MUTED), ("User", GOLD), (";", MUTED)]
    l2 = [("$user", SOFT), (" = ", MUTED), ("User", BLUE), ("::", MUTED), ("find", BLUE), ("(1);", MUTED)]
    o.append(code(52, 82, [l1, l2], size=12, lead=26, numbers=False))
    ux = end_of(52, l2[:2], 12)
    uw = width("mono", "User", 12)
    o.append(path(f"M{ux:.1f} 112H{ux + uw:.1f}", BLUE, 1.2))
    o.append(path(f"M{ux + uw - 4:.1f} 104l0 14 3.5-3.5 2.5 5.5 2.5-1-2.5-5.5h5z", None, fill=FG))
    o.append(window(336, 26, 268, 118, ("User.php",)))
    o.append(code(352, 82, [[("class ", RED), ("User", GOLD)], [("  extends ", RED), ("Authenticatable", GOLD)]], size=12, lead=26, numbers=False))
    o.append(f'<rect x="350" y="70" width="80" height="18" rx="4" fill="{RED}" fill-opacity=".14" class="pulse"/>')
    o.append(line([(ux + uw + 12, 108), (320, 108), (320, 79), (336, 79)]))
    o.append(line([(ux + uw + 12, 108), (320, 108), (320, 79), (336, 79)], RED, 1.5, "flow"))
    o.append(rect(36, 158, 568, 48, r=10))
    o.append(f'<circle cx="60" cy="180" r="6" fill="none" stroke="{ART}" stroke-width="1.5"/>')
    o.append(path("M64.5 184.5l4 4", ART, 1.6))
    o.append(text("mono", "PostCon", 80, 186, 13, FG))
    o.append(f'<rect x="{80 + width("mono", "PostCon", 13) + 2:.1f}" y="173" width="1.5" height="16" fill="{RED}" class="blink"/>')
    o.append(text("medium", "Search everywhere", 300, 186, 12, MUTED))
    w1, c1 = keycap(500, 172, "Shift")
    w2, c2 = keycap(500 + w1 + 6, 172, "Shift")
    o.append(c1 + c2)
    return "".join(o)


def refactor():
    o = [rect(36, 26, 568, 184)]
    o.append(text("semibold", "Rename class", 54, 52, 13, FG))
    o.append(rect(54, 62, 300, 30, r=8, fill=INSET))
    o.append(text("mono", "Article", 68, 82, 13, FG))
    o.append(f'<rect x="{68 + width("mono", "Article", 13) + 2:.1f}" y="69" width="1.5" height="16" fill="{RED}" class="blink"/>')
    o.append(text("mono", "was Post", 368, 82, 11.5, MUTED))
    o.append(text("mono", "PREVIEW", 54, 114, 10, MUTED, tracking=1))
    rows = (("app/Models/Article.php", "renamed"), ("app/Http/Controllers/PostController.php", "3"), ("routes/web.php", "2"), ("database/factories/PostFactory.php", "1"))
    for i, (f, n) in enumerate(rows):
        y = 136 + i * 21
        g = (check(62, y - 4, GREEN, 5.5) + text("mono", f, 76, y, 11, SOFT)
             + text("mono", n, 588 - width("mono", n, 10.5), y, 10.5, MUTED))
        o.append(f'<g class="appear" style="animation-delay: {i * .35:.2f}s">{g}</g>')
    return "".join(o)


def formatting():
    o = [text("medium", "Before", 36, 52, 11.5, MUTED), text("medium", "After", 354, 52, 11.5, MUTED)]
    w, c = chip(604 - (width("mono", ".editorconfig", 10.5) + 18), 37, ".editorconfig", 10.5, color=SOFT, font="mono")
    o.append(c)
    o.append(rect(36, 64, 250, 146))
    o.append(rect(354, 64, 250, 146))
    messy = ((10, 120), (34, 90), (6, 150), (52, 70), (18, 130), (40, 60), (0, 40))
    tidy = ((0, 120), (16, 90), (16, 150), (32, 70), (32, 130), (16, 60), (0, 40))
    for i, ((mx, mw), (tx, tw)) in enumerate(zip(messy, tidy)):
        y = 82 + i * 17
        o.append(bar(52 + mx, y, mw, 6, FAINT if i % 3 else hsl(220, 10, 30)))
        o.append(f'<g class="appear" style="animation-delay: {i * .12:.2f}s">{bar(370 + tx, y, tw, 6, BLUE if i in (0, 6) else (GOLD if i == 3 else hsl(220, 10, 34)))}</g>')
    o.append(f'<circle cx="320" cy="137" r="15" fill="{CARD}" stroke="{BORDER}"/>')
    o.append(f'<circle cx="320" cy="137" r="20" fill="none" stroke="{RED}" stroke-width="1.2" stroke-dasharray="3 5" class="spin"/>')
    o.append(path("M313 137h13M321 132l5 5-5 5", RED, 1.6))
    w, c = chip(320 - (width("medium", "Pint or Prettier", 11) + 18) / 2, 22, "Pint or Prettier", 11, fill=CARD, color=SOFT)
    o.append(c)
    return "".join(o)


def git():
    o = [rect(36, 26, 168, 184)]
    tree = (("app", None, 0, True), ("Models", None, 1, True), ("Post.php", "M", 2, False), ("Tag.php", "A", 2, False),
            ("routes", None, 0, True), ("web.php", "M", 1, False), ("README.md", None, 0, False))
    for i, (name, st, depth, is_dir) in enumerate(tree):
        y = 48 + i * 22
        x = 50 + depth * 14
        if is_dir:
            o.append(path(f"M{x} {y - 6}h5l2 2h6v8h-13z", ART, 1.2))
        else:
            o.append(path(f"M{x + 1} {y - 7}h7l3 3v8h-10z", ART, 1.1))
        c = {"M": hsl(38, 45, 62), "A": GREEN}.get(st, SOFT)
        o.append(text("medium", name, x + 20, y + 4, 11.5, c))
        if st:
            o.append(text("mono", st, 190 - width("mono", st, 10.5), y + 4, 10.5, c))
        elif is_dir and i in (0, 1, 4):
            o.append(dot(188, y, 2.5, hsl(38, 45, 62)))
    o.append(window(216, 26, 388, 184, ("Changes", "Post.php")))
    diff = (
        (" ", "class Post extends Model", None),
        (" ", "{", None),
        ("-", "    protected $fillable = ['title'];", RED),
        ("+", "    protected $fillable = [", GREEN),
        ("+", "        'title', 'body',", GREEN),
        ("+", "    ];", GREEN),
    )
    for i, (sign, s, c) in enumerate(diff):
        y = 76 + i * 19
        if c:
            o.append(f'<rect x="217" y="{y - 13}" width="386" height="18" fill="{c}" fill-opacity=".1"/>')
            o.append(f'<rect x="217" y="{y - 13}" width="2.5" height="18" fill="{c}"/>')
        o.append(text("mono", sign, 228, y, 11, c or DIM))
        o.append(text("mono", s, 244, y, 11, SOFT if c else MUTED))
    o.append(path("M216 188H604", BORDER, 1))
    o.append(dot(232, 199, 2, ART) + dot(240, 193, 2, ART) + path("M232 199v-6m0 3c0-3 8-1 8-3", ART, 1.1))
    o.append(text("mono", "main", 250, 203, 11, SOFT))
    o.append(text("mono", "+3 -1", 590 - width("mono", "+3 -1", 11), 203, 11, MUTED))
    return "".join(o)


def markdown():
    o = [window(36, 26, 276, 184, ("NOTES.md",))]
    src = [
        [("# Release notes", RED)],
        [("", MUTED)],
        [("Phun is ", SOFT), ("**fast**", GOLD), (".", SOFT)],
        [("- Link a folder", SOFT)],
        [("- Share it", SOFT)],
        [("```php", MUTED)],
        [("echo ", RED), ("'hello'", GREEN), (";", MUTED)],
    ]
    o.append(code(52, 76, src, size=11.5, lead=18, numbers=False))
    o.append(f'<rect x="{52 + width("mono", "- Share it", 11.5) + 2:.1f}" y="141" width="1.5" height="13" fill="{RED}" class="blink"/>')
    o.append(rect(328, 26, 276, 184))
    o.append(text("medium", "Preview", 344, 46, 11.5, MUTED))
    o.append(path("M328 58H604", BORDER, 1))
    o.append(text("bold", "Release notes", 344, 88, 18, FG))
    o.append(text("medium", "Phun is ", 344, 112, 12.5, SOFT))
    o.append(text("bold", "fast.", 344 + width("medium", "Phun is ", 12.5), 112, 12.5, FG))
    for i, s in enumerate(("Link a folder", "Share it")):
        y = 134 + i * 18
        o.append(dot(350, y - 4, 2.2, MUTED))
        g = text("medium", s, 360, y, 12, SOFT)
        o.append(f'<g class="appear">{g}</g>' if i == 1 else g)
    o.append(rect(344, 166, 244, 30, r=6, fill=INSET))
    o.append(code(356, 185, [[("echo ", RED), ("'hello'", GREEN), (";", MUTED)]], size=11, numbers=False))
    return "".join(o)


# --- Insight ----------------------------------------------------------------

def metrics():
    o = []
    stats = (("REQUESTS", "1,284"), ("RESPONSE", "38 ms"), ("ERRORS", "0.4%"), ("MEMORY", "62 MB"), ("CPU", "3%"))
    for i, (k, v) in enumerate(stats):
        x = 36 + i * 115
        o.append(rect(x, 26, 107, 58, r=10))
        o.append(text("mono", k, x + 12, 46, 9.5, MUTED, tracking=0.8))
        o.append(text("bold", v, x + 12, 72, 17, FG))
    o.append(rect(36, 96, 568, 114))
    for gy in (122, 150, 178):
        o.append(path(f"M52 {gy}H588", BORDER, 1, extra=' stroke-dasharray="2 4"'))
    series = (
        (GREEN, (190, 170, 176, 150, 160, 130, 138, 116, 124)),
        (BLUE, (196, 190, 192, 180, 186, 172, 178, 166, 170)),
        (AMBER, (200, 199, 196, 199, 194, 198, 192, 197, 196)),
    )
    for c, ys in series:
        pts = " L".join(f"{52 + i * 67} {y}" for i, y in enumerate(ys))
        o.append(f'<path d="M{pts}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" pathLength="100" class="draw"/>')
    return "".join(o)


def requests_tile():
    o = [rect(36, 26, 300, 184)]
    w, c = chip(50, 36, "Errors only", 10.5, color=SOFT)
    o.append(c)
    o.append(switch(50 + w + 8, 40, False))
    rows = (("GET", "/posts?page=2", "200", "18ms", GREEN), ("POST", "/login", "302", "41ms", BLUE),
            ("GET", "/api/posts", "200", "12ms", GREEN), ("GET", "/missing", "404", "6ms", AMBER), ("PUT", "/posts/7", "200", "33ms", GREEN))
    for i, (m, p, s, ms, col) in enumerate(rows):
        y = 84 + i * 26
        if i == 0:
            o.append(rect(42, y - 16, 288, 24, r=6, fill=REDSOFT, stroke=None))
        o.append(text("mono", m, 52, y, 11, SOFT))
        o.append(text("mono", p, 92, y, 11, FG))
        o.append(text("mono", s, 236, y, 11, col))
        o.append(text("mono", ms, 320 - width("mono", ms, 11), y, 11, MUTED))
    o.append(rect(350, 26, 254, 184))
    o.append(text("mono", "GET /posts?page=2", 366, 52, 12, FG))
    o.append(dot(370, 70, 3, GREEN) + text("medium", "200 in 18 ms", 380, 74, 11.5, SOFT))
    o.append(path("M350 88H604", BORDER, 1))
    heads = (("accept", "text/html", SOFT), ("user-agent", "Mozilla/5.0", SOFT), ("cookie", "not kept", DIM), ("authorization", "not kept", DIM))
    for i, (k, v, c) in enumerate(heads):
        y = 110 + i * 24
        g = text("mono", k, 366, y, 11, MUTED) + text("mono", v, 476, y, 11, c)
        o.append(f'<g class="appear" style="animation-delay: {i * .3:.1f}s">{g}</g>')
    return "".join(o)


def dock():
    o = [rect(36, 26, 568, 184)]
    o.append(bar(56, 44, 120, 8, hsl(220, 10, 28)))
    o.append(bar(56, 62, 300, 5, FAINT) + bar(56, 74, 240, 5, FAINT))
    o.append(path("M36 90H604", BORDER, 1))
    tabs = ("Logs", "Artisan", "Tinker", "Console")
    tx = 54
    for i, t in enumerate(tabs):
        tw = width("medium", t, 12)
        o.append(text("medium", t, tx, 112, 12, SOFT))
        o.append(f'<rect x="{tx}" y="119" width="{tw:.1f}" height="2" fill="{RED}" class="cyc" style="{cyc(i, 4, 12)}"/>')
        tx += tw + 24
    o.append(path("M36 122H604", BORDER, 1))
    logs = (text("mono", "[12:01:07] local.INFO: Post published", 54, 146, 11, SOFT)
            + text("mono", "[12:01:09] local.WARNING: Slow query", 54, 166, 11, AMBER)
            + text("mono", "[12:01:12] local.INFO: Mail sent", 54, 186, 11, SOFT))
    artisan = (text("mono", "make:model", 54, 146, 11.5, FG) + text("mono", "--policy", 140, 146, 11.5, MUTED)
               + rect(54, 156, 190, 44, r=6, fill=INSET) + text("mono", "Post", 66, 173, 11, FG) + text("mono", "Comment", 66, 191, 11, MUTED)
               + text("mono", "model", 230 - width("mono", "model", 10), 173, 10, DIM))
    tinker = (text("mono", "> User::count()", 54, 146, 11.5, FG) + text("mono", "= 42", 54, 166, 11.5, GREEN)
              + text("mono", "> Post::latest()->value('title')", 54, 186, 11.5, FG))
    console = (text("mono", "$ composer test", 54, 146, 11.5, FG)
               + text("mono", "PASS", 54, 166, 11, GREEN) + text("mono", "Tests\\Feature\\PostTest", 94, 166, 11, SOFT)
               + text("mono", "Tests: 24 passed", 54, 186, 11, MUTED))
    for i, g in enumerate((logs, artisan, tinker, console)):
        o.append(f'<g class="cyc" style="{cyc(i, 4, 12)}">{g}</g>')
    return "".join(o)


def database():
    o = [rect(36, 26, 568, 184)]
    tables = ("comments", "jobs", "migrations", "posts", "users")
    o.append(text("mono", "TABLES", 50, 48, 9.5, MUTED, tracking=1))
    for i, t in enumerate(tables):
        y = 72 + i * 25
        if t == "posts":
            o.append(rect(42, y - 15, 108, 22, r=6, fill=REDSOFT, stroke=None))
        o.append(text("mono", t, 52, y, 11.5, FG if t == "posts" else SOFT))
    o.append(path("M156 26V210", BORDER, 1))
    o.append(f'<g class="pulse">{dot(156, 112, 1.6, MUTED)}{dot(156, 118, 1.6, MUTED)}{dot(156, 124, 1.6, MUTED)}</g>')
    o.append(rect(170, 38, 420, 32, r=8, fill=INSET))
    o.append(code(184, 58, [[("select ", RED), ("* ", MUTED), ("from ", RED), ("posts ", GOLD), ("limit ", RED), ("50", BLUE)]], size=11.5, numbers=False))
    w, c = chip(590 - 52, 43, "Run", 10.5, fill=RED, color="#fff", font="semibold")
    o.append(c)
    cols = (("id", 184), ("title", 220), ("author_id", 372), ("created_at", 462))
    for name, x in cols:
        o.append(text("mono", name, x, 96, 10.5, MUTED))
    o.append(path("M170 104H590", BORDER, 1))
    data = (("1", "Hello world", "3", "2026-11-02"), ("2", "Phun on Linux", "1", "2026-11-04"), ("3", "Schema canvas", "3", "2026-11-06"), ("4", "Release notes", "2", "2026-11-08"))
    for i, row in enumerate(data):
        y = 126 + i * 21
        o.append(f'<rect x="172" y="{y - 14}" width="416" height="20" rx="5" fill="{REDSOFT}" class="cyc" style="{cyc(i, 4, 8)}"/>')
        for (name, x), v in zip(cols, row):
            o.append(text("mono", v, x, y, 11, FG if name == "title" else SOFT))
    return "".join(o)


def blueprint(x, y, name, fields, w=150):
    h = 34 + len(fields) * 20
    out = rect(x, y, w, h, r=10)
    out += f'<path d="M{x} {y + 30}H{x + w}" stroke="{BORDER}"/>'
    out += rect(x + 12, y + 9, 12, 12, r=3, fill="none", stroke=GOLD, sw=1.3)
    out += text("bold", name, x + 32, y + 20, 13, FG)
    for i, (f, kind) in enumerate(fields):
        fy = y + 48 + i * 20
        out += text("mono", f, x + 14, fy, 10.5, SOFT)
        out += text("mono", kind, x + w - 12 - width("mono", kind, 9.5), fy, 9.5, DIM)
    return out


def schema():
    o = []
    o.append(blueprint(36, 46, "User", (("id", "bigint"), ("name", "string"), ("email", "string"))))
    o.append(blueprint(246, 76, "Post", (("id", "bigint"), ("user_id", "bigint"), ("title", "string"))))
    o.append(blueprint(454, 30, "Comment", (("id", "bigint"), ("post_id", "bigint"), ("body", "text"))))
    o.append(line([(186, 104), (216, 104), (216, 134), (246, 134)], LINE, 1.6))
    o.append(text("mono", "hasMany", 198, 96 - 2, 9.5, MUTED))
    o.append(line([(396, 134), (424, 134), (424, 104), (454, 104)], RED, 1.6, "flow"))
    w, c = chip(400, 140, "new", 9.5, fill=REDSOFT, color=RED, h=18)
    o.append(c)
    o.append(f'<g class="pulse">{rect(436, 170, 168, 30, r=8, fill=RED, stroke=None)}</g>')
    o.append(text("semibold", "Review 1 change", 452, 189.5, 12, "#fff"))
    o.append(text("medium", "Drag to pan, Ctrl and the wheel to zoom", 36, 206, 10.5, DIM))
    return "".join(o)


def audits():
    o = [rect(36, 26, 568, 118)]
    rows = (("Composer packages", "composer.lock", "112 scanned"), ("JavaScript packages", "package-lock.json", "486 scanned"))
    for i, (name, f, n) in enumerate(rows):
        y = 58 + i * 46
        o.append(check(56, y - 4, GREEN, 7))
        o.append(text("bold", name, 72, y, 13, FG))
        o.append(text("mono", f, 72, y + 17, 10.5, MUTED))
        o.append(text("mono", n, 380, y, 11, SOFT))
        o.append(text("medium", "No advisories", 588 - width("medium", "No advisories", 11.5), y, 11.5, GREEN))
    o.append(f'<rect x="36" y="27" width="60" height="116" fill="{RED}" fill-opacity=".07" class="scan" style="--d: 508px"/>')
    o.append(rect(36, 156, 568, 54))
    o.append(switch(52, 176, True))
    o.append(text("semibold", "Wait before installing new releases", 90, 188, 12.5, FG))
    w, c = chip(604 - 16 - (width("medium", "7 days", 11) + 18), 172, "7 days", 11, color=SOFT)
    o.append(c)
    return "".join(o)


# --- Around the app ---------------------------------------------------------

def palette():
    o = [rect(76, 26, 488, 184)]
    o.append(f'<circle cx="100" cy="50" r="6" fill="none" stroke="{ART}" stroke-width="1.5"/>' + path("M104.5 54.5l4 4", ART, 1.6))
    o.append(text("mono", "blog", 120, 55, 13, FG))
    o.append(f'<rect x="{120 + width("mono", "blog", 13) + 2:.1f}" y="42" width="1.5" height="16" fill="{RED}" class="blink"/>')
    o.append(path("M76 70H564", BORDER, 1))
    groups = (("BLOG.TEST", ("Open in editor", "Artisan", "Tinker")), ("SERVICES", ("Install or update a service",)))
    y, i = 88, 0
    for g, items in groups:
        o.append(text("mono", g, 94, y, 9.5, MUTED, tracking=1))
        y += 20
        for it in items:
            o.append(f'<rect x="84" y="{y - 14}" width="472" height="22" rx="6" fill="{REDSOFT}" class="cyc" style="{cyc(i, 4, 6)}"/>')
            o.append(text("medium", it, 94, y + 1.5, 12.5, FG))
            i += 1
            y += 24
        y += 2
    w, c = keycap(546 - (width("semibold", "Enter", 10.5) + 14), 40, "Enter")
    o.append(c)
    return "".join(o)


def themes():
    o = []
    looks = (
        ("Daybreak", hsl(220, 14, 97), hsl(220, 12, 92), hsl(220, 10, 82), RED),
        ("Nightfall", hsl(225, 7, 8), hsl(225, 7, 6), hsl(225, 6, 22), RED),
    )
    for i, (name, bg, side, bars, accent) in enumerate(looks):
        x = 135 + i * 198
        o.append(f'<rect x="{x}" y="34" width="172" height="126" rx="10" fill="{bg}" stroke="{BORDER}"/>')
        o.append(f'<path d="M{x + 10} 34h36v126h-36a10 10 0 0 1-10-10v-106a10 10 0 0 1 10-10z" fill="{side}"/>')
        for k in range(4):
            o.append(bar(x + 10, 52 + k * 14, 26, 5, bars if k else accent))
        o.append(bar(x + 58, 50, 70, 8, bars))
        for k, w in enumerate((96, 80, 100)):
            o.append(bar(x + 58, 70 + k * 12, w, 5, bars))
        o.append(f'<rect x="{x + 58}" y="112" width="48" height="16" rx="5" fill="{accent}"/>')
        o.append(text("semibold", name, x + 86 - width("semibold", name, 12.5) / 2, 186, 12.5, SOFT))
        o.append(f'<rect x="{x - 5}" y="29" width="182" height="136" rx="14" fill="none" stroke="{RED}" stroke-width="2" class="cyc" style="{cyc(i, 2, 7.5)}"/>')
    return "".join(o)


def mcp():
    o = [rect(36, 40, 250, 88)]
    o.append(path("M52 58l3 6 6 3-6 3-3 6-3-6-6-3 6-3z", VIOLET, 1.3))
    o.append(text("semibold", "Your AI agent", 70, 71, 12, SOFT))
    o.append(text("medium", "Give blog a database and", 52, 98, 12.5, FG))
    o.append(text("medium", "use the newest PHP.", 52, 116, 12.5, FG))
    o.append(rect(36, 146, 250, 44, r=10, fill=INSET))
    o.append(text("mono", "phun mcp", 52, 173, 12.5, GREEN))
    o.append(text("medium", "MCP server", 270 - width("medium", "MCP server", 11), 173, 11, MUTED))
    o.append(line([(286, 84), (316, 84), (316, 120), (330, 120)]))
    o.append(line([(286, 84), (316, 84), (316, 120), (330, 120)], RED, 1.5, "flow"))
    o.append(rect(330, 30, 274, 180))
    o.append(text("mono", "TOOL CALLS", 348, 54, 9.5, MUTED, tracking=1))
    calls = (("list_sites", "3 sites"), ("create_database", "blog"), ("list_available_php", "4 versions"), ("set_site_php", "blog"))
    for i, (name, res) in enumerate(calls):
        y = 84 + i * 32
        g = check(352, y - 4, GREEN, 6) + text("mono", name, 366, y, 11.5, FG) + text("mono", res, 588 - width("mono", res, 10.5), y, 10.5, MUTED)
        o.append(f'<g class="appear" style="animation-delay: {i * .45:.2f}s">{g}</g>')
    return "".join(o)


def cli():
    o = [rect(36, 26, 568, 184)]
    for i in range(3):
        o.append(dot(54 + i * 13, 44, 4, DIM))
    o.append(text("medium", "Terminal", 320 - width("medium", "Terminal", 11.5) / 2, 48, 11.5, MUTED))
    o.append(path("M36 60H604", BORDER, 1))
    steps = (
        ("phun link", "blog is served at https://blog.test"),
        ("phun secure blog", "HTTPS is on for blog.test"),
        ("phun share blog", "Shared on a public URL"),
        ("phun doctor fix", "All checks passed"),
    )
    for i, (cmd, out) in enumerate(steps):
        y = 84 + i * 34
        g = (text("mono", "$", 54, y, 12, RED) + text("mono", cmd, 70, y, 12, FG)
             + check(60, y + 12, GREEN, 4.5) + text("mono", out, 70, y + 16, 11, MUTED))
        o.append(f'<g class="appear" style="animation-delay: {i * .5:.1f}s">{g}</g>')
    return "".join(o)


def health():
    o = [rect(36, 26, 568, 184)]
    o.append(text("bold", "Diagnostics", 54, 54, 14, FG))
    w, c = chip(604 - 18 - (width("semibold", "Fix all", 11) + 18), 37, "Fix all", 11, fill=CARD, color=SOFT, font="semibold")
    o.append(c)
    o.append(path("M36 70H604", BORDER, 1))
    rows = ("Resolver installed", None, "Privileged ports bound", "Default PHP installed")
    for i, r in enumerate(rows):
        y = 96 + i * 30
        if r:
            o.append(check(56, y - 4, GREEN, 6.5) + text("medium", r, 72, y, 12.5, SOFT))
        else:
            bad = (dot(56, y - 4, 6.5, RED) + path(f"M53 {y - 7}l6 6M59 {y - 7}l-6 6", BG, 1.6)
                   + text("medium", "Local CA not trusted", 72, y, 12.5, FG)
                   + rect(520, y - 17, 64, 24, r=7, fill=RED, stroke=None) + text("semibold", "Fix", 552 - width("semibold", "Fix", 11.5) / 2, y - 1, 11.5, "#fff"))
            good = check(56, y - 4, GREEN, 6.5) + text("medium", "Local CA trusted", 72, y, 12.5, SOFT)
            o.append(f'<g class="swap-a">{bad}</g><g class="swap-b">{good}</g>')
    return "".join(o)


def updates():
    o = [rect(76, 26, 488, 184)]
    o.append(rect(96, 44, 40, 40, r=10, fill=BG))
    from art import logo
    o.append(logo(98, 46, 36, FG))
    o.append(text("bold", "Phun", 150, 62, 16, FG))
    o.append(f'<g class="swap-a">{text("medium", "Downloading the new version", 150, 80, 12, MUTED)}</g>')
    o.append(f'<g class="swap-b">{text("medium", "Ready to install", 150, 80, 12, GREEN)}</g>')
    o.append(bar(96, 100, 448, 6, DIM))
    o.append(f'<rect x="96" y="100" width="448" height="6" rx="3" fill="{RED}" class="grow" style="animation-duration: 6s"/>')
    o.append(f'<g class="swap-b">{rect(424, 44, 120, 30, r=8, fill=RED, stroke=None)}{text("semibold", "Restart", 484 - width("semibold", "Restart", 12) / 2, 63.5, 12, "#fff")}</g>')
    o.append(text("mono", "WHAT'S NEW", 96, 134, 9.5, MUTED, tracking=1))
    for i, w in enumerate((380, 330, 410, 260)):
        y = 150 + i * 14
        o.append(dot(100, y + 2.5, 2, MUTED) + bar(110, y, w, 5, FAINT))
    return "".join(o)


SECTIONS = ("Applications", "PHP and services", "Editor", "Insight", "Around the app")

# (file stem, section index, title, description, drawing, items the cycle walks)
TILES = (
    ("link-and-park", 0, "Link a folder, or park them all",
     "Link a folder, or park a whole directory, and every project in it is served at name.test. The web root is found for you.", link_park, 4),
    ("https", 0, "Trusted HTTPS everywhere",
     "Every application is served over HTTPS from Phun's own local certificate authority, trusted by your browsers.", https, 4),
    ("php-per-application", 0, "PHP per application",
     "Each application picks its own PHP version, and the rest keep theirs. Switch from the app or with phun use.", php_per_app, 4),
    ("new-application", 0, "Start something new",
     "Create a Laravel, WordPress, CodeIgniter, CakePHP, Slim, static or HTML application, or bring an existing project or a Git repository.", new_app, 8),
    ("domains-and-proxies", 0, "Domains and proxies",
     "Add subdomains and wildcards, proxy a .test name to a local port, or send one path such as /reverb to another server.", domains, 4),
    ("share", 0, "Share on a public URL",
     "Share an application through Cloudflare Tunnel, for webhooks, demos and other devices.", share, 4),
    ("no-admin", 0, "Works without admin rights",
     "No admin rights to hand? Every application is also reachable at http://localhost/~name.test.", no_admin, 4),
    ("infrastructure", 0, "An infrastructure canvas",
     "Each application's services drawn as a canvas. Add a database, cache or storage and Phun writes the settings into its .env.", infrastructure, 4),

    ("php-versions", 1, "Every PHP version you need",
     "Several PHP versions side by side, each with its own php.ini settings and extensions.", php_versions, 4),
    ("services", 1, "Native services",
     "MySQL, MariaDB, PostgreSQL, MongoDB, Redis and Meilisearch as native services, started with the app. No Docker, no VM.", native_services, 4),
    ("mail", 1, "Every email, caught",
     "Every email your applications send is caught and readable in the Mail viewer: rendered, as plain text or as raw source.", mail, 3),
    ("object-storage", 1, "S3-compatible storage",
     "Object storage on your machine, with public or private buckets and a browser for what is in them.", storage, 4),
    ("laravel-workers", 1, "Queues, scheduler and Reverb",
     "Queue workers, as many as you need, the scheduler and Reverb, for each Laravel application.", laravel_workers, 4),
    ("developer-tools", 1, "Developer tools on demand",
     "Composer, Node.js, Bun, NVM, the Laravel installer and WP-CLI, installed when you need them, without a system package manager.", dev_tools, 4),

    ("highlighting", 2, "A code editor in the app",
     "Highlighting for PHP, Blade, JavaScript, TypeScript, Vue, HTML, CSS, JSON, YAML, Markdown, shell scripts and .env files.", highlighting, 13),
    ("completion", 2, "Completion that knows Laravel",
     "Your models' attributes and relations, routes, views, config, translations, validation rules and Blade components.", completion, 4),
    ("problems", 2, "Problems as you type",
     "PHP is checked by the application's own PHP as you type, with the message on hover and F2 to the next one.", problems, 4),
    ("navigation", 2, "Jump anywhere",
     "Ctrl-click a class to open it, see every usage of a method, go to any file, and search everywhere with a double Shift.", navigate, 4),
    ("refactoring", 2, "Refactor with a preview",
     "Rename across the application, extract a variable, and move classes between namespaces with their references updated.", refactor, 4),
    ("formatting", 2, "Formatting your way",
     "Format with the project's own Pint or Prettier. Its .editorconfig, .prettierrc and pint.json always win.", formatting, 4),
    ("git", 2, "Git, built in",
     "Changed lines in the gutter, changed files in the tree, the branch in the status line and the diff in a tab.", git, 4),
    ("markdown-preview", 2, "Markdown, previewed",
     "Markdown files show their rendered preview beside them, updated as you type, with code blocks in colour.", markdown, 4),

    ("metrics", 3, "Metrics per application",
     "Requests, response times, errors, memory and CPU for every application, charted as they happen.", metrics, 4),
    ("request-inspector", 3, "A request inspector",
     "The newest requests with status, timing, query string and headers. Cookies and authorization headers are never kept.", requests_tile, 4),
    ("terminal-dock", 3, "Logs and terminals in a dock",
     "Logs, Artisan, Tinker and a console at the bottom of the window. Artisan offers your models, tables and routes as you type.", dock, 4),
    ("database-browser", 3, "A database browser",
     "Browse any table in one grid, and write SQL that completes tables and columns. MySQL, MariaDB and PostgreSQL.", database, 4),
    ("schema-canvas", 3, "Draw your schema",
     "For Laravel: tables and model relationships as blueprints. Drag one model onto another to relate them, and review the code first.", schema, 4),
    ("dependency-audits", 3, "Dependency audits",
     "Audit Composer and JavaScript dependencies, update them all within your constraints, and make package managers wait before installing brand-new releases.", audits, 4),

    ("command-palette", 4, "A command palette",
     "Every page, application, Artisan command and action, a few keystrokes away.", palette, 4),
    ("themes", 4, "Two themes",
     "Daybreak and Nightfall, or follow the system. Your choice reaches every window and the editor.", themes, 2),
    ("mcp", 4, "An MCP server for AI agents",
     "Turn it on and agents such as Claude Code can list sites, switch PHP, create databases and read caught mail.", mcp, 4),
    ("cli", 4, "The phun command",
     "Link, park, secure, share and switch PHP from your terminal. The app and the command share one daemon.", cli, 4),
    ("health-checks", 4, "Health checks with fixes",
     "Built-in checks for DNS, certificates, ports and PHP, each with a one-click fix when something is off.", health, 4),
    ("updates", 4, "Updates itself",
     "Phun checks for new versions and installs them from the app, with the release notes beside them.", updates, 4),
)


def build_all(write):
    for i, (stem, section, title, body, draw, n) in enumerate(TILES):
        write(f"features/{stem}.svg", tile(i + 1, SECTIONS[section], title, body, draw, n))
