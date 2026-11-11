"""The README's Features section: a full-width banner per feature, in the
style of the download cards. Each has the feature's icon in the same tile,
its title beside it, its description under the title, and the
feature's moving drawing from tiles.py on the right. A banner is as tall as
a download card, and only grows when the text needs more room.
"""
from art import BORDER, FG, MUTED, SOFT, TILE as TILE_BG, begin, frame, rect, text, width, wrap
from icons import ICONS
import drawings
import tiles

W = 1280
MIN_H = 204
TILE_X, TILE_Y, TILE = 32, 24, 80
TEXT_X = TILE_X + TILE + 24

# The part of a tile's 640 by 400 canvas its drawing occupies, and where the
# drawing sits in the banner: right-aligned, as tall as a download card allows.
CROP_X, CROP_Y, CROP_W, CROP_H = 20, 18, 600, 204
ART_PAD = 16
ART_GAP = 28

TITLE_SIZE, TITLE_MIN = 34, 28
BODY_SIZE, BODY_LEAD = 18, 26


def icon(stem, x, y, size):
    """A feature's Tabler outline icon, `size` px square at (x, y)."""
    k = size / 24
    paths = "".join(f'<path d="{d}"/>' for d in ICONS[stem])
    return (
        f'<g transform="translate({x:g} {y:g}) scale({k:.4f})" fill="none" stroke="{SOFT}" '
        f'stroke-width="{2.6 / k:.3f}" stroke-linecap="round" stroke-linejoin="round">{paths}</g>'
    )


def banner(_number, _section, title, body, draw, n_cycle, stem):
    begin()
    art = draw()
    scale = (MIN_H - 2 * ART_PAD) / CROP_H
    art_w = CROP_W * scale
    art_x = W - TILE_X - art_w
    text_w = art_x - ART_GAP - TEXT_X
    size = TITLE_SIZE
    while size > TITLE_MIN and width("black", title, size, tracking=-0.4) > text_w - 40:
        size -= 1
    lines = wrap("semibold", body, BODY_SIZE, text_w)
    body_top = TILE_Y + 70
    h = max(MIN_H, int(body_top + (len(lines) - 1) * BODY_LEAD + 34))

    out = [f'<circle cx="{TILE_X + TILE / 2}" cy="{TILE_Y + TILE / 2}" r="90" fill="url(#glow)"/>']
    out.append(rect(TILE_X, TILE_Y, TILE, TILE, r=20, fill=TILE_BG, stroke=BORDER, sw=1.5))
    out.append(icon(stem, TILE_X + 20, TILE_Y + 20, 40))

    out.append(text("black", title, TEXT_X, TILE_Y + 38, size, FG, tracking=-0.4))
    for i, line in enumerate(lines):
        out.append(text("semibold", line, TEXT_X, body_top + i * BODY_LEAD, BODY_SIZE, MUTED))

    art_y = (h - CROP_H * scale) / 2
    out.append(
        f'<g transform="translate({art_x - CROP_X * scale:.2f} {art_y - CROP_Y * scale:.2f}) scale({scale:.4f})">{art}</g>'
    )
    css = tiles.TILE_CSS + "  " + tiles.cycle_css(n_cycle) + "\n"
    return frame(W, h, "\n".join(out), title=title, desc=body, css=css, fade_from=0.4, mark=False)


# Features added since the tile set, in the same shape as tiles.TILES.
ADDED = (
    ("laravel-cloud", 0, "Laravel Cloud",
     "Link an application to Laravel Cloud, create what Cloud is missing and deploy, or bring a Cloud application home with the same infrastructure.", drawings.laravel_cloud, 4),
    ("framework-stack", 0, "Your stack, recognised",
     "Every application shows its framework and the libraries it uses with their versions: Laravel, Livewire, Filament, Vue, React, Inertia, Tailwind, Vite and more.", drawings.framework_stack, 6),
    ("debugging", 2, "Debugging with Xdebug",
     "Turn Xdebug on for an application, set breakpoints beside the line numbers, and step through a request with its stack and variables.", drawings.debugging, 3),
    ("technical-debt", 3, "Technical debt, listed",
     "The work your team put off and noted in the code, grouped by file with who it is for. Select one to open the editor on that line.", drawings.technical_debt, 4),
    ("notifications", 4, "Notifications in the background",
     "Jobs finishing or failing, failed scheduled tasks, caught mail and errors in a log arrive as desktop notifications, even with the window closed.", drawings.notifications, 3),
    ("key-binds", 4, "Key binds of your own",
     "Give any action in the command palette a key of your own. A backtick opens the Console for the application you are on, and closes it again.", drawings.key_binds, 3),
    ("diagnostics-report", 4, "A problem report, redacted",
     "One file with what a bug report needs: versions, services, health checks and recent logs, with passwords, tokens and email addresses removed.", drawings.diagnostics_report, 4),
)


def features():
    """Every feature in README order: section by section, the tile set's
    features first and the added ones after them."""
    out = []
    for section in range(len(tiles.SECTIONS)):
        out.extend(f for f in tiles.TILES if f[1] == section)
        out.extend(f for f in ADDED if f[1] == section)
    return out


def build_all(write):
    for i, (stem, section, title, body, draw, n) in enumerate(features()):
        write(f"banners/{stem}.svg", banner(i + 1, tiles.SECTIONS[section], title, body, draw, n, stem))
