"""Build the Phun documentation site into docs/, for GitHub Pages.

The site is static: HTML, one stylesheet and one small script. Its drawings
are the README artwork from .github/readme (the feature banners' moving
drawings and the banner's diagram), cut out of the built SVGs and given a
Daybreak twin, so nothing is redrawn here and no fonts are needed. The command
reference is read from the README's tables.

    python3 .github/site/build.py

GitHub Pages serves docs/ from main, so the output is checked in. The README
artwork workflow runs this after redrawing, and whenever .github/site changes. Page text lives in pages.py.
"""
import colorsys
import html
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
README_ART = os.path.join(REPO, ".github", "readme")
OUT = os.path.join(REPO, "docs")

sys.path.insert(0, README_ART)
from icons import ICONS  # noqa: E402

import pages  # noqa: E402

SITE_URL = "https://cloudcake.github.io/phun/"
GITHUB = "https://github.com/cloudcake/phun"
RELEASES = GITHUB + "/releases/latest"
DISCUSSIONS = GITHUB + "/discussions"

LOGO = "M78 48H144C204 48 220 80 220 116C220 156 198 188 140 188H114V208H78ZM114 84V152H138C170 152 184 136 184 116C184 96 168 84 138 84Z"


# ── Daybreak twins of the artwork ────────────────────────────────────────
def _hsl(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss * 100, ll * 100


def _hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


# The README palette (art.py) and its Daybreak counterpart, after the app's
# light tokens: cards turn white on a pale ground, text turns dark, and the
# accents deepen to keep their contrast.
LIGHT = {
    "#0f1117": _hex(220, 20, 97),    # BG
    "#0c0e13": _hex(220, 16, 95),    # TILE
    "#171a21": "#ffffff",            # CARD
    "#13151b": _hex(220, 16, 95),    # INSET
    "#262a33": _hex(223, 14, 87),    # BORDER
    "#363a45": _hex(223, 12, 76),    # LINE
    "#5a6172": _hex(220, 9, 56),     # ART
    "#f3f4f6": _hex(223, 17, 8),     # FG
    "#cdd0d6": _hex(223, 12, 24),    # SOFT
    "#8c919b": _hex(220, 9, 42),     # MUTED
    "#383e4c": _hex(220, 12, 76),    # DIM
    "#2d3139": _hex(220, 14, 89),    # FAINT
    "#d63d3d": "#d63d3d",            # RED
    "#401c1c": _hex(0, 70, 94),      # REDSOFT
    "#35b664": _hex(142, 71, 34),    # GREEN
    "#dda23c": _hex(38, 92, 40),     # AMBER
    "#d8b564": _hex(38, 70, 36),     # GOLD
    "#74a5dc": _hex(217, 75, 44),    # BLUE
    "#a88cd9": _hex(262, 55, 50),    # VIOLET
}


def _light_colour(hexcol):
    key = hexcol.lower()
    if len(key) == 4:
        key = "#" + "".join(c * 2 for c in key[1:])
    if key in LIGHT:
        return LIGHT[key]
    h, s, l = _hsl(key)
    if s < 30 or l > 92:
        return _hex(h, min(s, 16), max(6, min(97, 100 - l * 0.92)))
    return _hex(h, s, max(30, l - 14))


def daybreak(svg):
    """The same drawing for the light theme, every colour mapped. White mask
    stops stay white, since a mask reads them as alpha."""
    return re.sub(r'(fill|stroke|stop-color)="(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})"',
                  lambda m: f'{m.group(1)}="{m.group(2) if m.group(2).lower() in ("#fff", "#ffffff") and m.group(1) == "stop-color" else _light_colour(m.group(2))}"',
                  svg)


def bare(svg):
    """The drawing without its card: no ground, no dots, no red glow and no
    frame, so it sits on the page's own art panel in either theme."""
    svg = re.sub(r'<rect width="\d+" height="\d+" fill="#[0-9a-f]{6}"/>\s*', "", svg, count=1)
    svg = re.sub(r'<rect width="\d+" height="\d+" fill="url\(#dots\)" mask="url\(#dotmask\)"/>\s*', "", svg)
    svg = re.sub(r'<circle [^>]*fill="url\(#glow\)"/>\s*', "", svg)
    svg = re.sub(r'<rect x="\.5" y="\.5" [^>]*fill="none" stroke="#[0-9a-f]{6}"/>\s*', "", svg)
    return svg


def crop(svg, x, y, w, h):
    svg = re.sub(r'(<svg[^>]*?) width="\d+" height="\d+" viewBox="[^"]*"',
                 lambda m: f'{m.group(1)} width="{w:g}" height="{h:g}" viewBox="{x:g} {y:g} {w:g} {h:g}"', svg, count=1)
    return svg.replace('<g clip-path="url(#card)">', "<g>", 1)


def read(rel):
    with open(os.path.join(README_ART, rel), encoding="utf-8") as fh:
        return fh.read()


def title_desc(svg):
    t = re.search(r"<title[^>]*>(.*?)</title>", svg, re.S)
    d = re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S)
    return html.unescape(t.group(1).strip()), html.unescape(d.group(1).strip())


ART_DONE = {}


def write_art(name, svg):
    for theme, body in (("dark", svg), ("light", daybreak(svg))):
        path = os.path.join(OUT, "art", theme, name + ".svg")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)


def drawing(stem):
    """A feature banner's moving drawing (its right-hand side), with the
    banner's title and description. Geometry follows banners.py."""
    if stem not in ART_DONE:
        svg = read(f"banners/{stem}.svg")
        h = int(re.search(r'<svg[^>]* height="(\d+)"', svg).group(1))
        scale = (204 - 32) / 204
        art_w = 600 * scale
        art_x = 1280 - 32 - art_w
        art_h = 204 * scale
        art_y = (h - art_h) / 2
        write_art(stem, crop(bare(svg), round(art_x - 6), round(art_y - 4), round(art_w + 12), round(art_h + 8)))
        ART_DONE[stem] = title_desc(svg)
    return ART_DONE[stem]


def hero_art():
    write_art("hero", crop(bare(read("banner.svg")), 812, 40, 424, 316))


# ── Markup helpers ───────────────────────────────────────────────────────
def esc(s):
    return html.escape(s, quote=True)


def icon(stem, cls=""):
    paths = "".join(f'<path d="{d}"/>' for d in ICONS[stem])
    c = f' class="{cls}"' if cls else ""
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"{c}>{paths}</svg>'


def mark_svg():
    """The small P on its dark tile, for the top bar and footer."""
    return (
        '<svg viewBox="0 0 256 256" aria-hidden="true"><rect width="256" height="256" rx="58" fill="#131417"/>'
        '<rect x="0.75" y="0.75" width="254.5" height="254.5" rx="57.25" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="1.5"/>'
        f'<path d="{LOGO}" transform="translate(-15 4)" fill="#fff" fill-rule="evenodd"/></svg>'
    )


def app_icon():
    """The app icon as build.py draws it: the white P on a dark gray tile lit
    red from the corner. The P resolves as the dots land."""
    return (
        '<svg class="icon" viewBox="0 0 256 256" aria-hidden="true"><defs>'
        '<radialGradient id="icon-glow" cx="0.72" cy="0.78" r="0.7"><stop offset="0" stop-color="#d63d3d" stop-opacity="0.55"/>'
        '<stop offset="1" stop-color="#d63d3d" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="icon-mark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/>'
        '<stop offset="1" stop-color="#d9dbe0"/></linearGradient></defs>'
        '<g class="tile"><rect width="256" height="256" rx="58" fill="#131417"/>'
        '<rect width="256" height="256" rx="58" fill="url(#icon-glow)"/>'
        '<rect x="0.75" y="0.75" width="254.5" height="254.5" rx="57.25" fill="none" stroke="#ffffff" stroke-opacity="0.09" stroke-width="1.5"/></g>'
        f'<path class="mark" d="{LOGO}" transform="translate(-15 4)" fill="url(#icon-mark)" fill-rule="evenodd"/></svg>'
    )


def art_img(name, alt, cls=""):
    c = f" {cls}" if cls else ""
    return (
        f'<img class="art-dark{c}" src="{{root}}art/dark/{name}.svg" alt="{esc(alt)}" loading="lazy" decoding="async">'
        f'<img class="art-light{c}" src="{{root}}art/light/{name}.svg" alt="" aria-hidden="true" loading="lazy" decoding="async">'
    )


def figure(stem, caption=None):
    title, desc = drawing(stem)
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure><div class="art-panel">{art_img(stem, title + ". " + desc)}</div>{cap}</figure>'


SUN = '<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
GITHUB_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></svg>'
DOWNLOAD_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M7 11l5 5 5-5M12 4v12"/></svg>'
BOOK_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 19a9 9 0 0 1 9 0 9 9 0 0 1 9 0M3 6a9 9 0 0 1 9 0 9 9 0 0 1 9 0M3 6v13M12 6v13M21 6v13"/></svg>'

THEME_BOOT = (
    "<script>(function(){try{var t=localStorage.getItem('phun-docs-theme');}catch(e){}"
    "if(t!=='light'&&t!=='dark'){t=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}"
    "var r=document.documentElement;r.setAttribute('data-theme',t);r.classList.add('js');})();</script>"
)


def shell(title, description, body, root, current="", docs_menu=False):
    menu = (
        f'<button class="iconbtn menu-toggle" type="button" aria-label="Contents" aria-expanded="false" '
        f'aria-controls="sidebar" data-tip="Contents">{MENU}</button>' if docs_menu else ""
    )
    docs_current = ' aria-current="page"' if current == "docs" else ""
    full_title = "Phun" if title == "Phun" else f"{title} · Phun"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0f1012" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/site.css">
{THEME_BOOT}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar"><div class="topbar-inner">
{menu}<a class="brand" href="{root}index.html" aria-label="Phun home">{mark_svg()}<span>Phun</span></a>
<a class="navlink" href="{root}install.html"{docs_current}>Docs</a>
<a class="navlink wide" href="{RELEASES}">Download</a>
<a class="iconbtn" href="{GITHUB}" aria-label="Phun on GitHub" data-tip="Phun on GitHub">{GITHUB_ICON}</a>
<button class="iconbtn theme-toggle" type="button" aria-label="Switch theme" data-tip="Switch theme">{SUN}{MOON}</button>
</div></header>
{body}
<footer class="footer"><div class="footer-inner">
<a class="brand" href="{root}index.html">{mark_svg()}<span>Phun</span></a>
<a href="{root}install.html">Documentation</a>
<a href="{RELEASES}">Releases</a>
<a href="{DISCUSSIONS}">Discussions</a>
<a href="{GITHUB}">GitHub</a>
<span>Free, by Cloudcake</span>
</div></footer>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
'''.replace("{root}", root)


# ── Pages ────────────────────────────────────────────────────────────────
def home():
    hero_art()
    pills = "".join(f'<span class="pill">{p}</span>' for p in ("Every application on .test", "Trusted HTTPS", "Databases, cache and mail"))
    features = []
    for stem, slug in pages.HOME_FEATURES:
        title, desc = drawing(stem)
        page = pages.page(slug)
        features.append(
            f'<article class="feature reveal"><div class="text"><span class="tile-icon">{icon(stem)}</span><div>'
            f'<h3>{esc(title)}</h3><p>{esc(desc)}</p><a class="more" href="{slug}.html">{esc(page["title"])} →</a></div></div>'
            f'<div class="art-panel">{art_img(stem, title)}</div></article>'
        )
    topics = []
    for group, slugs in pages.NAV:
        for slug in slugs:
            p = pages.page(slug)
            topics.append(
                f'<a class="topic reveal" href="{slug}.html"><span class="tile-icon">{icon(p["icon"])}</span>'
                f'<span class="topic-text"><b>{esc(p["title"])}{' <span class="badge">Next release</span>' if p.get("next") else ""}</b>'
                f'<span class="topic-sum">{esc(p["summary"])}</span></span></a>'
            )
    body = f'''<main id="main">
<section class="hero ground"><div class="hero-inner">
<div>
<div class="lockup"><div class="app-icon">{app_icon()}<canvas aria-hidden="true"></canvas></div>
<h1 class="settle d1">Phun</h1></div>
<p class="tagline settle d2">Your pocket-sized PHP playground.</p>
<p class="platforms settle d3">For macOS, Linux and Windows.</p>
<div class="pills settle d4">{pills}</div>
<div class="actions settle d5"><a class="btn primary" href="{RELEASES}">{DOWNLOAD_ICON}Download</a>
<a class="btn" href="install.html">{BOOK_ICON}Read the docs</a></div>
</div>
<div class="hero-art">{art_img("hero", "A browser on blog.test over HTTPS, joined to PHP, MySQL and caught mail.")}</div>
</div></section>

<section class="section"><div class="wrap">
<p class="eyebrow">What Phun is</p>
<h2>Your PHP applications, on your own machine</h2>
<p class="lede">{pages.INTRO}</p>
{"".join(features)}
</div></section>

<section class="section"><div class="wrap">
<p class="eyebrow">Documentation</p>
<h2>Everything, step by step</h2>
<p class="lede">From the first download to the <code>phun</code> command. Each page follows what the app does today.</p>
<div class="topics">{"".join(topics)}</div>
</div></section>
</main>'''
    return shell("Phun", "Phun runs your PHP applications on your own machine, each at its own .test address over trusted HTTPS, with databases, cache and mail beside them. For macOS, Linux and Windows.", body, "", "home")


def sidebar(current):
    out = []
    for group, slugs in pages.NAV:
        out.append(f'<p class="group">{esc(group)}</p>')
        for slug in slugs:
            p = pages.page(slug)
            cur = ' aria-current="page"' if slug == current else ""
            out.append(f'<a href="{slug}.html"{cur}>{icon(p["icon"])}{esc(p["title"])}</a>')
    return f'<nav class="sidebar" id="sidebar" aria-label="Documentation">{"".join(out)}</nav><div class="scrim"></div>'


def doc(slug):
    p = pages.page(slug)
    order = [s for _, slugs in pages.NAV for s in slugs]
    i = order.index(slug)
    prev_link = next_link = ""
    if i > 0:
        q = pages.page(order[i - 1])
        prev_link = f'<a class="prev" href="{order[i - 1]}.html"><small>Previous</small><b>{esc(q["title"])}</b></a>'
    if i < len(order) - 1:
        q = pages.page(order[i + 1])
        next_link = f'<a class="next" href="{order[i + 1]}.html"><small>Next</small><b>{esc(q["title"])}</b></a>'
    content = p["body"]()
    content = re.sub(r"\{\{figure:([a-z-]+)(?:\|(.*?))?\}\}", lambda m: figure(m.group(1), m.group(2)), content)
    badge = '<span class="badge">Next release</span>' if p.get("next") else ""
    body = f'''<div class="docs">
{sidebar(slug)}
<main class="doc" id="main">
<div class="doc-head"><span class="tile-icon">{icon(p["icon"])}</span><h1>{esc(p["title"])}{badge}</h1></div>
<p class="lede">{p["lede"]}</p>
{content}
<nav class="pager" aria-label="More pages">{prev_link}{next_link}</nav>
</main>
</div>'''
    return shell(p["title"], p["summary"], body, "", "docs", docs_menu=True)


def favicon():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><rect width="256" height="256" rx="58" fill="#131417"/>'
        f'<path d="{LOGO}" transform="translate(-15 4)" fill="#fff" fill-rule="evenodd"/></svg>\n'
    )


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    for name in ("site.css", "site.js"):
        shutil.copy(os.path.join(HERE, name), os.path.join(OUT, "assets", name))
    files = {"index.html": home(), "favicon.svg": favicon(), ".nojekyll": ""}
    for _, slugs in pages.NAV:
        for slug in slugs:
            files[f"{slug}.html"] = doc(slug)
    files["404.html"] = shell("Not found", "That page is not part of the Phun documentation.", (
        '<main id="main" class="section ground"><div class="wrap"><p class="eyebrow">404</p>'
        '<h2>That page is not here</h2><p class="lede">It may have moved. '
        '<a href="/phun/install.html">Start from the documentation</a> or <a href="/phun/">go home</a>.</p></div></main>'
    ), "/phun/")
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    print(f"docs/: {len(files)} pages and files, {len(ART_DONE) + 1} drawings in two themes")


if __name__ == "__main__":
    main()
