"""The README's feature lists: three long images, each a section header over
its features as bullets. Every bullet has its own icon and accent in a
tinted badge; the bullets rise in when the image loads and a soft halo
travels down the list. Nothing moves with reduced motion on.
"""
from art import AMBER, BLUE, BORDER, FG, GOLD, GREEN, INSET, MUTED, RED, VIOLET, begin, frame, rect, text, width, wrap
from icons import ICONS
from tiles import SECTIONS, TILES

W = 1280
MARGIN = 72
GUTTER = 64
COL = (W - 2 * MARGIN - GUTTER) / 2
BADGE = 56
TEXT_X = BADGE + 24
TEXT_W = COL - TEXT_X
TITLE_SIZE, BODY_SIZE, BODY_LEAD = 22, 17.5, 25
ACCENTS = (RED, BLUE, GREEN, AMBER, VIOLET, GOLD)
STEP = 0.45

LIST_CSS = """
  .halo { opacity: 0; transform-box: fill-box; transform-origin: center; animation: halo var(--p) ease-out infinite; }
  @keyframes halo { 0% { opacity: 0; transform: scale(.92); } 4% { opacity: .85; } 14%, 100% { opacity: 0; transform: scale(1.32); } }
"""

# (file, number, title, subtitle, [(group label or None, [tile stems])])
LISTS = (
    ("lists/serve.svg", 1, "Serve every application",
     "Link or park a folder and it is served at its own .test address over trusted HTTPS, with its own PHP and native databases, cache, mail and storage beside it.",
     [(SECTIONS[0], None), (SECTIONS[1], None)]),
    ("lists/editor.svg", 2, "A code editor that knows Laravel",
     "Completion from your models and routes, live PHP checks, refactors, formatting and git, built into the app.",
     [(None, 2)]),
    ("lists/insight.svg", 3, "See what your applications do",
     "Metrics, every request, logs, terminals and a database browser for each application, with a command palette, the phun command and an MCP server around it all.",
     [(SECTIONS[3], None), (SECTIONS[4], None)]),
)


def section_items(label, index):
    want = SECTIONS.index(label) if label is not None else index
    return [(stem, title, body) for stem, section, title, body, _draw, _n in TILES if section == want]


def badge(x, y, stem, accent, i, period):
    icon = "".join(f'<path d="{d}"/>' for d in ICONS[stem])
    s = 1.3
    ox, oy = x + (BADGE - 24 * s) / 2, y + (BADGE - 24 * s) / 2
    halo = rect(x - 3, y - 3, BADGE + 6, BADGE + 6, r=17, fill="none", stroke=accent, sw=1.5,
                extra=f' class="halo" style="--p: {period:.2f}s; animation-delay: {i * STEP:.2f}s"')
    return (
        halo
        + rect(x, y, BADGE, BADGE, r=14, fill=INSET, stroke=None)
        + rect(x, y, BADGE, BADGE, r=14, fill=accent, stroke=None, extra=' fill-opacity=".12"')
        + rect(x + .5, y + .5, BADGE - 1, BADGE - 1, r=13.5, fill="none", stroke=accent, extra=' stroke-opacity=".4"')
        + f'<g transform="translate({ox:g} {oy:g}) scale({s})" fill="none" stroke="{accent}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
    )


def bullet(x, y, stem, title, body, accent, i, period):
    lines = wrap("medium", body, BODY_SIZE, TEXT_W)
    out = [badge(x, y, stem, accent, i, period), text("bold", title, x + TEXT_X, y + 22, TITLE_SIZE, FG, tracking=-0.1)]
    for n, line in enumerate(lines):
        out.append(text("medium", line, x + TEXT_X, y + 51 + n * BODY_LEAD, BODY_SIZE, MUTED))
    height = max(BADGE, 51 + (len(lines) - 1) * BODY_LEAD + 6)
    delay = 0.15 + i * 0.07
    return f'<g class="rise" style="animation-delay: {delay:.2f}s">{"".join(out)}</g>', height


def feature_list(number, title, subtitle, groups):
    begin()
    out = [
        text("mono", f"{number:02d}", MARGIN, 92, 13, RED, tracking=1),
        f'<path d="M{MARGIN + 28} 87.5H{MARGIN + 56}" stroke="{RED}" stroke-width="1.5" stroke-linecap="round"/>',
        text("bold", title, MARGIN, 142, 38, FG, tracking=-0.4),
    ]
    sub = wrap("medium", subtitle, 19, 900)
    for n, line in enumerate(sub):
        out.append(text("medium", line, MARGIN, 184 + n * 28, 19, MUTED))
    y = 184 + (len(sub) - 1) * 28 + 66
    items = [(label, section_items(label, index)) for label, index in groups]
    total = sum(len(group) for _label, group in items)
    period = max(total * STEP, 6)
    i = 0
    for label, group in items:
        if label:
            caps = label.upper()
            out.append(text("mono", caps, MARGIN, y, 12, MUTED, tracking=1.6))
            lx = MARGIN + width("mono", caps, 12, tracking=1.6) + 16
            out.append(f'<path d="M{lx:g} {y - 4.5}H{W - MARGIN}" stroke="{BORDER}"/>')
            y += 34
        for row in range(0, len(group), 2):
            heights = []
            for col, (stem, t, body) in enumerate(group[row:row + 2]):
                x = MARGIN + col * (COL + GUTTER)
                svg, h = bullet(x, y, stem, t, body, ACCENTS[i % len(ACCENTS)], i, period)
                out.append(svg)
                heights.append(h)
                i += 1
            y += max(heights) + 40
        y += 16
    height = int(y + 24)
    desc = f"{title}. " + " ".join(f"{t}: {body}" for _l, group in items for _s, t, body in group)
    return frame(W, height, "\n".join(out), title=title, desc=desc, fade=("0", "0", "1", "1"), css=LIST_CSS)


def build_all(write):
    for name, number, title, subtitle, groups in LISTS:
        write(name, feature_list(number, title, subtitle, groups))
