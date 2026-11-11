"""Drawings for the features added after the tile set: each in the style of
tiles.py, shown on the right of its README banner. Drawn on the tiles'
640 by 400 canvas, inside the part a banner shows (x 36..604, y 30..210).
"""
from art import AMBER, ART, BG, BLUE, BORDER, CARD, DIM, FG, GOLD, GREEN, INSET, LINE, MUTED, RED, REDSOFT, SOFT, bar, dot, line, logo, path, rect, text, width
from tiles import check, chip, code, cyc, globe, keycap, switch, window


# laravel-cloud

CLOUD_ROWS = (("Database", "MySQL"), ("Cache", "Redis"), ("Bucket", "S3"), ("Queue workers", "2"))
CLOUD_MISSING = 2


def laravel_cloud():
    o = []
    # Local application.
    o.append(rect(36, 30, 200, 180))
    o.append(globe(56, 48, 7))
    o.append(text("mono", "blog.test", 72, 52.5, 13, FG))
    w, c = chip(220 - (width("medium", "Local", 10.5) + 18), 37, "Local", 10.5, color=SOFT)
    o.append(c)
    o.append(path("M36 66H236", BORDER, 1))
    # Laravel Cloud environment.
    o.append(rect(368, 30, 236, 180))
    o.append(path("M386 56h14a5 5 0 0 0 .6-9.9 7 7 0 0 0-13.4-2 5 5 0 0 0-1.2 11.9z", SOFT, 1.4))
    o.append(text("bold", "Laravel Cloud", 410, 53, 13, FG))
    w, c = chip(590 - (width("mono", "production", 10) + 18), 37, "production", 10, color=SOFT, font="mono")
    o.append(c)
    o.append(path("M368 66H604", BORDER, 1))
    # The link between them.
    o.append(line([(236, 48), (368, 48)]))
    w, c = chip(302 - (width("semibold", "Linked", 10.5) + 18) / 2, 37, "Linked", 10.5, fill=INSET, color=SOFT, font="semibold")
    o.append(c)

    for i, (name, kind) in enumerate(CLOUD_ROWS):
        y = 88 + i * 26
        o.append(dot(52, y, 3.5, GREEN, f"pulse {'abca'[i]}"))
        o.append(text("semibold", name, 64, y + 4.5, 12.5, SOFT))
        o.append(text("mono", kind, 222 - width("mono", kind, 10.5), y + 4, 10.5, DIM))
        o.append(line([(236, y), (368, y)], LINE, 1))
        if i == CLOUD_MISSING:
            o.append(line([(236, y), (368, y)], RED, 1.5, "flow"))
            mw = width("semibold", "Missing", 10.5) + 18
            missing = (dot(386, y, 3.5, RED) + text("semibold", name, 398, y + 4.5, 12.5, FG)
                       + rect(590 - mw, y - 10, mw, 20, r=6, fill=REDSOFT, stroke=None)
                       + text("semibold", "Missing", 599 - mw, y + 4, 10.5, RED))
            created = (check(386, y, GREEN, 5.5) + text("semibold", name, 398, y + 4.5, 12.5, FG)
                       + text("medium", "Created", 590 - width("medium", "Created", 10.5), y + 4, 10.5, GREEN))
            o.append(f'<g class="swap-a">{missing}</g><g class="swap-b">{created}</g>')
        else:
            o.append(check(386, y, GREEN, 5.5))
            o.append(text("semibold", name, 398, y + 4.5, 12.5, SOFT))
            o.append(text("medium", "Ready", 590 - width("medium", "Ready", 10.5), y + 4, 10.5, MUTED))

    # Footers: where the code lives, and the deploy followed in Phun.
    o.append(path("M36 184H236", BORDER, 1))
    o.append(text("mono", "~/Code/blog", 52, 201, 10.5, MUTED))
    o.append(path("M368 184H604", BORDER, 1))
    o.append(dot(386, 197, 3.5, RED, "pulse"))
    o.append(text("semibold", "Deploy", 398, 201.5, 11.5, SOFT))
    o.append(bar(456, 194, 132, 6, DIM))
    o.append(f'<rect x="456" y="194" width="132" height="6" rx="3" fill="{RED}" class="grow" style="animation-duration: 6s"/>')
    o.append(line([(236, 197), (368, 197)], LINE, 1))
    o.append(line([(236, 197), (368, 197)], RED, 1.5, "flow"))
    return "".join(o)


# framework-stack

STACK_N, STACK_P = 6, 9


def _stack_badge(x, y, name, version, framework=False):
    """A text badge: the library's name and its version, `y` its top."""
    pad = 22 if framework else 10
    nw = width("semibold", name, 11.5)
    vw = width("mono", version, 11)
    w = pad + nw + 5 + vw + 10
    o = rect(x, y, w, 26, r=7, fill=INSET)
    if framework:
        o += dot(x + 12, y + 13, 3.5, RED)
    o += text("semibold", name, x + pad, y + 17, 11.5, SOFT)
    o += text("mono", version, x + pad + nw + 5, y + 17, 11, FG)
    return w, o


def _stack_glow(x, y, w, i):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:.1f}" height="26" rx="7" fill="{RED}" fill-opacity=".1" '
            f'stroke="{RED}" class="cyc" style="{cyc(i, STACK_N, STACK_P)}"/>')


def framework_stack():
    o = [rect(36, 30, 294, 180)]
    o.append(globe(56, 52, 8))
    o.append(text("mono", "blog.test", 72, 56.5, 13, FG))
    fw, fb = _stack_badge(0, 0, "Laravel", "12", framework=True)
    fx = 314 - fw
    o.append(_stack_badge(fx, 39, "Laravel", "12", framework=True)[1])
    o.append(_stack_glow(fx, 39, fw, 0))
    o.append(path("M36 74H330", BORDER, 1))
    o.append(text("mono", "LIBRARIES", 52, 98, 10, MUTED, tracking=1))

    libs = (("Livewire", "3", 1), ("Filament", "3", 2), ("Alpine.js", "3", 5), ("Tailwind", "4", 3), ("Vite", "7", 4))
    x, y = 52, 108
    for name, ver, k in libs:
        w, _ = _stack_badge(0, 0, name, ver)
        if x + w > 314:
            x, y = 52, y + 34
        o.append(_stack_badge(x, y, name, ver)[1])
        o.append(_stack_glow(x, y, w, k))
        x += w + 8
    o.append(dot(56, 194, 3, GREEN, "pulse"))
    o.append(text("medium", "Installed versions first", 66, 198, 10.5, MUTED))

    files = (
        ("composer.json", 30, (("laravel/framework", "^12.0", 0), ("livewire/livewire", "^3.6", 1), ("filament/filament", "^3.3", 2))),
        ("package.json", 124, (("tailwindcss", "^4.1", 3), ("vite", "^7.0", 4), ("alpinejs", "^3.14", 5))),
    )
    for name, top, rows in files:
        o.append(rect(360, top, 244, 86, r=10, fill=CARD))
        o.append(path(f"M376 {top + 10}h8l4 4v9h-12z", ART, 1.2))
        o.append(text("mono", name, 396, top + 22, 11, SOFT))
        o.append(path(f"M360 {top + 32}H604", BORDER, 1))
        for j, (key, ver, k) in enumerate(rows):
            yy = top + 50 + j * 16
            o.append(f'<rect x="366" y="{yy - 11}" width="232" height="15" rx="4" fill="{RED}" fill-opacity=".12" '
                     f'class="cyc" style="{cyc(k, STACK_N, STACK_P)}"/>')
            o.append(text("mono", f'"{key}"', 376, yy, 10.5, MUTED))
            o.append(text("mono", ver, 588 - width("mono", ver, 10.5), yy, 10.5, FG))
    pts_a = [(330, 120), (345, 120), (345, 61), (360, 61)]
    pts_b = [(345, 120), (345, 155), (360, 155)]
    o.append(line(pts_a))
    o.append(line(pts_b))
    o.append(line(pts_a, RED, 1.5, "flow"))
    o.append(line(pts_b, RED, 1.5, "flow", style="animation-delay: .4s"))
    o.append(dot(345, 120, 3, DIM))
    return "".join(o)


# debugging

BUG_PATHS = ("M9 9v-1a3 3 0 0 1 6 0v1", "M8 9h8a6 6 0 0 1 1 3v3a5 5 0 0 1 -10 0v-3a6 6 0 0 1 1 -3",
       "M3 13l4 0", "M17 13l4 0", "M12 20l0 -6", "M4 19l3.35 -2", "M20 19l-3.35 -2", "M4 7l3.75 2.4", "M20 7l-3.75 2.4")


def bug_mark(x, y, size, stroke):
    k = size / 24
    paths = "".join(f'<path d="{d}"/>' for d in BUG_PATHS)
    return (f'<g transform="translate({x:g} {y:g}) scale({k:.4f})" fill="none" stroke="{stroke}" '
            f'stroke-width="{1.4 / k:.3f}" stroke-linecap="round" stroke-linejoin="round">{paths}</g>')


def debugging():
    o = [window(36, 30, 568, 84, ("UserController.php",))]
    # The bug_mark button, on: Xdebug is on for this application.
    o.append(rect(570, 35, 26, 20, r=6, fill=REDSOFT, stroke=None))
    o.append(bug_mark(576, 38, 14, RED))
    # The stopped line steps down with F8, one line per beat.
    lines = [
        [("$user", SOFT), (" = ", MUTED), ("User", GOLD), ("::", MUTED), ("findOrFail", BLUE), ("(", MUTED), ("$id", SOFT), (");", MUTED)],
        [("$posts", SOFT), (" = ", MUTED), ("$user", SOFT), ("->", MUTED), ("posts", BLUE), ("()->", MUTED), ("latest", BLUE), ("()->", MUTED), ("get", BLUE), ("();", MUTED)],
        [("return ", RED), ("view", BLUE), ("(", MUTED), ("'users.show'", GREEN), (", ", MUTED), ("compact", BLUE), ("(", MUTED), ("'user'", GREEN), (", ", MUTED), ("'posts'", GREEN), ("));", MUTED)],
    ]
    for i in range(3):
        y = 76 + i * 15
        o.append(f'<rect x="37" y="{y - 11}" width="566" height="15" fill="{RED}" fill-opacity=".12" class="cyc" style="{cyc(i, 3, 6)}"/>')
        o.append(f'<rect x="37" y="{y - 11}" width="2.5" height="15" fill="{RED}" class="cyc" style="{cyc(i, 3, 6)}"/>')
    o.append(code(90, 76, lines, size=11, lead=15, first=14, num_x=62))
    o.append(dot(51, 72.5, 4, RED))

    # The debug panel under the editor.
    o.append(rect(36, 120, 568, 90))
    x = 50
    steps = ((None, "F9"), ("over", "F8"), ("into", "F7"), ("out", "Shift+F8"))
    for kind, key in steps:
        cy = 136
        if kind is None:
            o.append(path(f"M{x} {cy - 5}v10l8-5z", GREEN, 1.4))
        elif kind == "over":
            o.append(path(f"M{x} {cy + 2}a5 5 0 0 1 10 0M{x + 7} {cy + 1}l3 2 2-3", SOFT, 1.3) + dot(x + 5, cy + 5, 1.6, SOFT))
        elif kind == "into":
            o.append(path(f"M{x + 5} {cy - 6}v7M{x + 2} {cy - 2}l3 3 3-3", SOFT, 1.3) + dot(x + 5, cy + 5, 1.6, SOFT))
        else:
            o.append(path(f"M{x + 5} {cy + 1}v-7M{x + 2} {cy - 3}l3-3 3 3", SOFT, 1.3) + dot(x + 5, cy + 5, 1.6, SOFT))
        w, c = keycap(x + 16, cy - 10, key)
        if key == "F8":
            o.append(f'<rect x="{x + 16}" y="{cy - 10}" width="{w:.1f}" height="20" rx="5" fill="none" stroke="{RED}" stroke-width="1.2" class="pulse"/>')
        o.append(c)
        x += 16 + w + 16
    status = "Paused on line 14"
    o.append(dot(588 - width("medium", status, 11) - 10, 136, 3.5, RED, "pulse"))
    o.append(text("medium", status, 588 - width("medium", status, 11), 140, 11, MUTED))
    o.append(path("M36 152H604", BORDER, 1))
    o.append(path("M300 152V210", BORDER, 1))

    # The stack.
    frames = (("UserController->show", "14"), ("Pipeline->then", "167"), ("{main}", "52"))
    for i, (name, ln) in enumerate(frames):
        y = 170 + i * 16
        if i == 0:
            o.append(rect(42, y - 11, 252, 15, r=4, fill=REDSOFT, stroke=None))
        o.append(text("mono", name, 52, y, 10.5, FG if i == 0 else SOFT))
        o.append(text("mono", ln, 286 - width("mono", ln, 10), y, 10, MUTED))

    # The variables: $user opens on its fields, then closes again.
    closed = (path("M318 166l3 3-3 3", MUTED, 1.3)
              + text("mono", "$user", 330, 170, 10.5, SOFT) + text("mono", "App\\Models\\User", 588 - width("mono", "App\\Models\\User", 10), 170, 10, DIM)
              + text("mono", "$id", 330, 186, 10.5, SOFT) + text("mono", "7", 588 - width("mono", "7", 10.5), 186, 10.5, BLUE))
    opened = (path("M316 167l3 3 3-3", MUTED, 1.3)
              + text("mono", "$user", 330, 170, 10.5, SOFT) + text("mono", "App\\Models\\User", 588 - width("mono", "App\\Models\\User", 10), 170, 10, DIM)
              + text("mono", "name", 346, 186, 10.5, MUTED) + text("mono", "'Ada'", 588 - width("mono", "'Ada'", 10.5), 186, 10.5, GREEN)
              + text("mono", "email", 346, 202, 10.5, MUTED) + text("mono", "'ada@blog.test'", 588 - width("mono", "'ada@blog.test'", 10.5), 202, 10.5, GREEN))
    o.append(f'<g class="swap-a">{closed}</g><g class="swap-b">{opened}</g>')
    return "".join(o)


# technical-debt

def technical_debt():
    period, n = 10, 4
    o = []

    # Filter chips by kind, then the search box.
    chips = (("All", "4", True), ("Unfinished", "1", False), ("Needs a fix", "1", False), ("Workaround", "1", False), ("Known bug", "1", False))
    x = 36
    for label, count, on in chips:
        lw = width("medium", label, 10.5)
        w = lw + width("mono", count, 9.5) + 22
        o.append(rect(x, 30, w, 22, r=11, fill=INSET if on else CARD, stroke=LINE if on else BORDER))
        o.append(text("medium", label, x + 9, 44.8, 10.5, FG if on else MUTED))
        o.append(text("mono", count, x + 13 + lw, 44.5, 9.5, DIM if not on else MUTED))
        x += w + 5
    o.append(rect(440, 30, 164, 22, r=7, fill=INSET))
    o.append(f'<circle cx="453" cy="40.5" r="4" fill="none" stroke="{ART}" stroke-width="1.3"/>' + path("M456 43.5l3 3", ART, 1.4))
    o.append(text("medium", "Search text, files or names", 466, 44.8, 10.5, DIM))

    # Two file groups, each a header with the path and a row per note.
    tones = {"TODO": (INSET, SOFT, 1), "FIXME": (RED, RED, .16), "HACK": (AMBER, AMBER, .16), "BUG": (RED, RED, .16)}
    labels = {"TODO": "Unfinished", "FIXME": "Needs a fix", "HACK": "Workaround", "BUG": "Known bug"}
    groups = (
        (62, "app/Models/", "User.php", (("TODO", "Cache the avatar URL", "maya", 40), ("FIXME", "Guard against null emails", "sam", 72))),
        (140, "routes/", "web.php", (("HACK", "Skip CSRF for the webhook", "lee", 18), ("BUG", "Redirect loops on logout", None, 31))),
    )
    rows = []
    for gy, d, f, items in groups:
        o.append(rect(36, gy, 370, 22 + len(items) * 24, r=10))
        o.append(path(f"M36 {gy + 22}H406", BORDER, 1))
        o.append(text("mono", d, 48, gy + 15, 10.5, MUTED))
        o.append(text("mono", f, 48 + width("mono", d, 10.5), gy + 15, 10.5, FG))
        o.append(text("mono", str(len(items)), 394 - width("mono", str(len(items)), 10.5), gy + 15, 10.5, MUTED))
        for k, (tag, s, owner, ln) in enumerate(items):
            cy = gy + 22 + 12 + k * 24
            if k:
                o.append(path(f"M36 {cy - 12}H406", BORDER, 1))
            rows.append((cy, tag, s, owner, ln))
    for i, (cy, tag, s, owner, ln) in enumerate(rows):
        hl = (f'<rect x="37" y="{cy - 11.5}" width="368" height="23" fill="{RED}" fill-opacity=".1"/>'
              f'<rect x="37" y="{cy - 11.5}" width="2.5" height="23" fill="{RED}"/>')
        o.append(f'<g class="cyc" style="{cyc(i, n, period)}">{hl}</g>')
        fill, ink, op = tones[tag]
        o.append(f'<rect x="46" y="{cy - 8}" width="80" height="16" rx="5" fill="{fill}" fill-opacity="{op:g}"/>')
        lab = labels[tag]
        o.append(text("semibold", lab, 86 - width("semibold", lab, 10) / 2, cy + 3.6, 10, ink))
        o.append(text("medium", s, 136, cy + 4, 11.5, FG))
        if owner:
            ox = 136 + width("medium", s, 11.5) + 7
            ow = width("mono", "@" + owner, 9.5) + 10
            o.append(rect(ox, cy - 7.5, ow, 15, r=4, fill=INSET, stroke=None))
            o.append(text("mono", "@" + owner, ox + 5, cy + 3.4, 9.5, MUTED))
        lt = f"line {ln}"
        o.append(text("mono", lt, 396 - width("mono", lt, 10), cy + 3.5, 10, MUTED))

    # The editor, opened on the selected note's line.
    o.append(rect(428, 62, 176, 148))
    o.append(path("M428 92H604", BORDER, 1))
    states = (
        ("User.php", 38, [
            [("function ", RED), ("avatar", BLUE), ("()", MUTED)],
            [("{", MUTED)],
            [("  // ", MUTED), ("TODO", GOLD), ("(maya): cache", MUTED)],
            [("  return ", RED), ("$this", SOFT), ("->", MUTED), ("url", BLUE), (";", MUTED)],
            [("}", MUTED)],
        ]),
        ("User.php", 70, [
            [("$e", SOFT), (" = ", MUTED), ("$this", SOFT), ("->", MUTED), ("email", SOFT), (";", MUTED)],
            [("", MUTED)],
            [("// ", MUTED), ("FIXME", RED), ("(sam): null", MUTED)],
            [("return ", RED), ("trim", BLUE), ("(", MUTED), ("$e", SOFT), (");", MUTED)],
            [("}", MUTED)],
        ]),
        ("web.php", 16, [
            [("Route", GOLD), ("::", MUTED), ("post", BLUE), ("(", MUTED), ("'/hook'", GREEN), (",", MUTED)],
            [("  Hook", GOLD), ("::", MUTED), ("class", RED), (")", MUTED)],
            [("  // ", MUTED), ("HACK", AMBER), ("(lee): csrf", MUTED)],
            [("  ->", MUTED), ("name", BLUE), ("(", MUTED), ("'hook'", GREEN), (");", MUTED)],
            [("", MUTED)],
        ]),
        ("web.php", 29, [
            [("Route", GOLD), ("::", MUTED), ("post", BLUE), ("(", MUTED), ("'/logout'", GREEN), (",", MUTED)],
            [("  Logout", GOLD), ("::", MUTED), ("class", RED), (")", MUTED)],
            [("// ", MUTED), ("BUG", RED), (": loops back", MUTED)],
            [("  ->", MUTED), ("name", BLUE), ("(", MUTED), ("'logout'", GREEN), (");", MUTED)],
            [("", MUTED)],
        ]),
    )
    for i, ((f, first, src), (cy, *_)) in enumerate(zip(states, rows)):
        tw = width("medium", f, 11.5) + 40
        caret = 460 + sum(width("mono", s, 10) for s, _ in src[2]) + 2
        g = (
            f'<rect x="429" y="63" width="{tw:.1f}" height="29" fill="{INSET}"/>'
            + path(f"M429 91H{429 + tw:.1f}", RED, 2)
            + f'<rect x="441" y="72" width="8" height="10" rx="1.5" fill="none" stroke="{ART}" stroke-width="1.2"/>'
            + text("medium", f, 455, 81.5, 11.5, FG)
            + f'<rect x="429" y="139" width="174" height="18" fill="{RED}" fill-opacity=".1"/>'
            + f'<rect x="429" y="139" width="2.5" height="18" fill="{RED}"/>'
            + code(460, 113, src, size=10, lead=19, first=first, num_x=438)
            + f'<rect x="{caret:.1f}" y="141" width="1.5" height="13" fill="{RED}" class="blink"/>'
            + line([(406, cy), (417, cy), (417, 148), (428, 148)], LINE)
            + line([(406, cy), (417, cy), (417, 148), (428, 148)], RED, 1.5, "flow")
        )
        o.append(f'<g class="cyc" style="{cyc(i, n, period)}">{g}</g>')
    return "".join(o)


# notifications

# Toasts and the Do not disturb switch share the 6s swap period: toasts slide
# in one after another while it is off, and stay away while it is on.
NOTIFY_TOASTS = (
    ("Job failed", "SendInvoice · blog.test", "job"),
    ("Mail caught", "Welcome, Sam · blog.test", "mail"),
    ("Scheduled task failed", "backup:run · shop.test", "task"),
)
NOTIFY_KINDS = ("Queued jobs", "Scheduled tasks", "Caught mail", "Log errors")
TOAST_X, TOAST_W, TOAST_H = 36, 296, 52
CARD_X, CARD_W = 352, 252


def _toast_badge(x, y, kind):
    """The 28px icon square at the left of a toast."""
    out = rect(x, y, 28, 28, r=7, fill=REDSOFT if kind != "mail" else INSET, stroke=None)
    cx, cy = x + 14, y + 14
    if kind == "job":
        out += path(f"M{cx - 4} {cy - 4}l8 8M{cx + 4} {cy - 4}l-8 8", RED, 1.8)
    elif kind == "mail":
        out += path(f"M{cx - 7} {cy - 5}h14v10h-14zM{cx - 7} {cy - 5}l7 5.5 7-5.5", ART, 1.4)
    else:
        out += f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{RED}" stroke-width="1.5"/>'
        out += path(f"M{cx} {cy - 4}V{cy}l3 2", RED, 1.5)
    return out


def notifications():
    o = []
    toasts = []
    for i, (title, sub, kind) in enumerate(NOTIFY_TOASTS):
        y = 34 + i * (TOAST_H + 8)
        right = TOAST_X + TOAST_W - 14
        g = (
            rect(TOAST_X, y, TOAST_W, TOAST_H, r=10)
            + _toast_badge(TOAST_X + 12, y + 12, kind)
            + text("semibold", title, TOAST_X + 52, y + 22, 12.5, FG)
            + text("mono", sub, TOAST_X + 52, y + 39, 10.5, MUTED)
            + text("medium", "now", right - width("medium", "now", 10.5), y + 22, 10.5, DIM)
            + logo(right - 12, y + 30, 12, ART)
        )
        delay = -0.2 + i * 0.7
        toasts.append(f'<g class="appear" style="animation-duration: 6s; animation-delay: {delay:.2f}s">{g}</g>')
    o.append(f'<g class="swap-a">{"".join(toasts)}</g>')

    # While Do not disturb is on: a quiet moon where the toasts were.
    mx, my = TOAST_X + TOAST_W / 2, 112
    label = "Do not disturb"
    lw = width("semibold", label, 12)
    quiet = (
        path(f"M{mx + 4} {my - 22}a12 12 0 1 0 10 16a9.5 9.5 0 0 1-10-16z", ART, 1.5)
        + text("semibold", label, mx - lw / 2, my + 20, 12, MUTED)
    )
    o.append(f'<g class="swap-b">{quiet}</g>')

    o.append(rect(CARD_X, 30, CARD_W, 180))
    o.append(text("bold", "Notifications", CARD_X + 16, 53, 13.5, FG))
    o.append(path(f"M{CARD_X} 66H{CARD_X + CARD_W}", BORDER, 1))
    sx = CARD_X + CARD_W - 16 - 26
    for i, kind in enumerate(NOTIFY_KINDS):
        y = 89 + i * 22
        o.append(text("semibold", kind, CARD_X + 16, y, 12, SOFT))
        o.append(switch(sx, y - 11, on=True))
    o.append(path(f"M{CARD_X} 170H{CARD_X + CARD_W}", BORDER, 1))
    o.append(text("semibold", label, CARD_X + 16, 194, 12, FG))
    sy = 183
    o.append(
        f'<rect x="{sx}" y="{sy}" width="26" height="14" rx="7" fill="{GREEN}" class="swap-b"/>'
        f'<rect x="{sx}" y="{sy}" width="26" height="14" rx="7" fill="{DIM}" class="swap-a"/>'
        f'<circle cx="{sx + 7}" cy="{sy + 7}" r="5" fill="{FG}" class="knob" style="animation-duration: 6s"/>'
    )
    return "".join(o)


# key-binds

def key_binds():
    def caps(right, y, keys):
        """Key caps for a chord, right-aligned to `right`, 20px tall from `y`."""
        ws = [max(22, width("semibold", k, 10.5) + 14) for k in keys]
        x = right - sum(ws) - 5 * (len(keys) - 1)
        out = []
        for k, w in zip(keys, ws):
            out.append(rect(x, y, w, 20, r=5, fill=INSET))
            if k == "`":
                out.append(text("mono", k, x + w / 2 - width("mono", k, 14) / 2, y + 17, 14, SOFT))
            else:
                out.append(text("semibold", k, x + w / 2 - width("semibold", k, 10.5) / 2, y + 14, 10.5, SOFT))
            x += w + 5
        return "".join(out)

    o = [rect(36, 26, 568, 184)]
    o.append(rect(54, 41, 22, 16, r=4, fill="none", stroke=ART, sw=1.4))
    o.append(path("M59 46.5h.01M65 46.5h.01M71 46.5h.01M61 51.5h6", ART, 1.4))
    o.append(text("bold", "Key binds", 86, 54, 14, FG))
    o.append(rect(404, 37, 182, 24, r=7, fill=INSET))
    o.append(f'<circle cx="420" cy="48" r="4.5" fill="none" stroke="{ART}" stroke-width="1.3"/>' + path("M423.5 51.5l3 3", ART, 1.4))
    o.append(text("medium", "Filter actions", 434, 53, 11.5, DIM))
    o.append(path("M36 70H604", BORDER, 1))

    rows = (
        ("Open Console", "Terminals", ("`",)),
        ("Next terminal", "Terminals", ("Shift", "`")),
        ("Code editor", "Application", None),
        ("Search commands", "Palette", ("Ctrl", "K")),
    )
    for i, (name, group, keys) in enumerate(rows):
        y = 87 + i * 34
        if i:
            o.append(path(f"M54 {y - 17}H586", BORDER, 1))
        if keys is None:
            o.append(rect(44, y - 14, 552, 28, r=7, fill=INSET, stroke=None))
        o.append(text("medium", name, 58, y + 4.5, 12.5, FG))
        o.append(text("medium", group, 210, y + 4, 11, MUTED))
        if keys:
            o.append(caps(586, y - 10, keys))
            continue
        old = caps(586, y - 10, ("Ctrl", "E"))
        rw = width("semibold", "Recording…", 10.5) + 30
        rec = (rect(586 - rw, y - 11, rw, 22, r=6, fill=REDSOFT, stroke=RED)
               + dot(586 - rw + 11, y, 3, RED, "pulse")
               + text("semibold", "Recording…", 586 - rw + 20, y + 4, 10.5, FG))
        new = caps(586, y - 10, ("Ctrl", "Shift", "E"))
        nw = sum(max(22, width("semibold", k, 10.5) + 14) for k in ("Ctrl", "Shift", "E")) + 10
        new += text("medium", "Reset", 586 - nw - 12 - width("medium", "Reset", 11), y + 4, 11, MUTED)
        for k, g in enumerate((old, rec, new)):
            o.append(f'<g class="cyc" style="{cyc(k, 3, 7.5)}">{g}</g>')
    return "".join(o)


# diagnostics-report

def diagnostics_report():
    o = [rect(36, 30, 344, 180)]
    o.append(path("M54 41h10l5 5v15h-15z", ART, 1.3) + path("M64 41v5h5M57 51h7M57 55h5", ART, 1.1))
    o.append(text("bold", "Diagnostics report", 78, 56, 13, FG))
    w, c = chip(364 - (width("medium", "Redacted", 10.5) + 18), 41, "Redacted", 10.5, fill=REDSOFT, color=RED)
    o.append(c)
    o.append(path("M36 68H380", BORDER, 1))

    vx = 150
    o.append(text("mono", "VERSIONS", 52, 87, 9.5, MUTED, tracking=1))
    o.append(text("mono", "PHP 8.4  MySQL 8.4", vx, 87, 11, SOFT))
    o.append(text("mono", "SERVICES", 52, 106, 9.5, MUTED, tracking=1))
    o.append(dot(vx + 4, 102.5, 3, GREEN, "pulse"))
    o.append(text("mono", "mysql, redis running", vx + 14, 106, 11, SOFT))
    o.append(text("mono", "HEALTH", 52, 125, 9.5, MUTED, tracking=1))
    o.append(check(vx + 4, 121.5, GREEN, 4.5))
    o.append(text("mono", "All checks passed", vx + 14, 125, 11, SOFT))
    o.append(text("mono", "LOGS", 52, 144, 9.5, MUTED, tracking=1))

    logs = (("DB_PASSWORD=", ""), ("Bearer ", ""), ("mail to ", ""), ("/home/", "/blog"))
    red = "[redacted]"
    rw = width("mono", red, 10.5) + 10
    for i, (before, after) in enumerate(logs):
        y = 144 + i * 19
        o.append(text("mono", before, vx, y, 11, MUTED))
        cx = vx + width("mono", before, 11) + 2
        o.append(rect(cx, y - 12, rw, 16, r=4, fill=REDSOFT, stroke=None))
        o.append(text("mono", red, cx + 5, y, 10.5, RED))
        o.append(f'<rect x="{cx:.1f}" y="{y - 12}" width="{rw:.1f}" height="16" rx="4" fill="none" stroke="{RED}" class="cyc" style="{cyc(i, 4, 8)}"/>')
        if after:
            o.append(text("mono", after, cx + rw + 2, y, 11, MUTED))
    o.append(f'<rect x="140" y="129" width="46" height="76" fill="{RED}" fill-opacity=".08" class="scan" style="--d: 180px"/>')

    o.append(rect(396, 30, 208, 180))
    o.append(text("mono", "REMOVED", 412, 53, 9.5, MUTED, tracking=1))
    o.append(path("M396 68H604", BORDER, 1))
    for i, label in enumerate(("Passwords", "Tokens", "Email addresses", "User name")):
        y = 88 + i * 21
        o.append(f'<rect x="402" y="{y - 13}" width="196" height="19" rx="5" fill="{REDSOFT}" class="cyc" style="{cyc(i, 4, 8)}"/>')
        o.append(dot(414, y - 3.5, 3, RED))
        o.append(text("medium", label, 424, y, 11.5, SOFT))
    w1, c1 = chip(412, 176, "Copy", 11, color=SOFT, h=24, font="semibold")
    o.append(c1)
    w2, c2 = chip(412 + w1 + 8, 176, "Save file", 11, fill=RED, color="#fff", h=24, font="semibold")
    o.append(c2)
    return "".join(o)
