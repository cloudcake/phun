"""The README's Download section: a header per platform, and a button per
installer, each its own image so each links straight to its file.

They carry the release's version and installer names, so the release
workflow rebuilds them (`build.py platforms`) right after it rewrites the
README's download block. The version is read from that block. The button
names (`download/<platform>-<slug>.svg`) match update-readme.py's.
"""
import os
import re

from art import AMBER, BG, BLUE, BORDER, CARD, DIM, FG, GOLD, INSET, MUTED, RED, SOFT, TILE, begin, frame, hsl, path, rect, text, width

W, H = 1280, 200
README = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "README.md")

CSS = """
  .sway { transform-box: view-box; transform-origin: 52px 22px; animation: sway 3.2s ease-in-out infinite; }
  @keyframes sway { 0%, 100% { transform: rotate(-6deg); } 50% { transform: rotate(8deg); } }
  .pane { animation: pane 4s ease-in-out infinite; }
  @keyframes pane { 0%, 100% { opacity: .55; } 12%, 30% { opacity: 1; } 45% { opacity: .55; } }
  .waddle { transform-box: view-box; transform-origin: 50px 96px; animation: waddle 1.6s ease-in-out infinite; }
  @keyframes waddle { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
  .lid { transform-box: fill-box; transform-origin: center; animation: lid 4.5s infinite; }
  @keyframes lid { 0%, 92%, 100% { transform: scaleY(1); } 95% { transform: scaleY(.1); } }
  .drop { animation: drop 1.8s ease-in-out infinite; }
  @keyframes drop { 0%, 100% { transform: translateY(-2px); } 50% { transform: translateY(3px); } }
"""


def apple():
    body = ("M50 30C40 24 20 24 15 42C10 60 20 82 32 90C38 95 44 94 50 91C56 94 62 95 68 90"
            "C74 85 80 76 84 66C72 62 68 46 80 38C74 28 60 24 50 30Z")
    leaf = "M52 22C52 12 58 6 66 4C66 14 60 20 52 22Z"
    return (
        f'<circle cx="50" cy="56" r="40" fill="url(#glow)" class="pulse"/>'
        + path(body, SOFT, 3.2, fill=hsl(222, 18, 13))
        + f'<g class="sway">{path(leaf, GREEN_LEAF, 2.6, fill=hsl(142, 30, 16))}</g>'
    )


GREEN_LEAF = hsl(142, 45, 52)


def windows():
    out = []
    panes = ((14, 14), (54, 14), (14, 54), (54, 54))
    for i, (x, y) in enumerate(panes):
        out.append(f'<rect x="{x}" y="{y}" width="34" height="34" rx="4" fill="{BLUE}" class="pane" style="animation-delay: {i * .5:.1f}s"/>')
    return "".join(out)


def penguin():
    body = "M50 8C34 8 27 22 27 38C27 46 22 54 19 64C15 77 22 92 50 92C78 92 85 77 81 64C78 54 73 46 73 38C73 22 66 8 50 8Z"
    belly = "M50 34C38 34 33 50 33 64C33 80 40 88 50 88C60 88 67 80 67 64C67 50 62 34 50 34Z"
    beak = "M42 33C46 29 54 29 58 33C55 38 45 38 42 33Z"
    feet = "M28 90C30 84 42 84 44 92C38 96 30 96 28 90ZM56 92C58 84 70 84 72 90C70 96 62 96 56 92Z"
    return (
        f'<g class="waddle">'
        + path(body, SOFT, 2.6, fill="#15171c")
        + path(belly, None, fill=hsl(220, 14, 92))
        + f'<g class="lid"><ellipse cx="43" cy="24" rx="5" ry="6.5" fill="#fff"/><ellipse cx="57" cy="24" rx="5" ry="6.5" fill="#fff"/>'
        + f'<circle cx="44.5" cy="25.5" r="2.4" fill="#15171c"/><circle cx="55.5" cy="25.5" r="2.4" fill="#15171c"/></g>'
        + path(beak, None, fill=GOLD)
        + path(feet, None, fill=AMBER)
        + "</g>"
    )


PLATFORMS = (
    ("macos", "macOS", "Apple Silicon and Intel", apple,
     (("apple-silicon", "Apple Silicon", "Phun_{v}_apple-silicon.dmg"), ("intel", "Intel", "Phun_{v}_intel.dmg"))),
    ("windows", "Windows", "Windows 10 and 11, x64", windows,
     (("installer", "Installer", "Phun_{v}_windows-x64-setup.exe"),)),
    ("linux", "Linux", "Debian, Ubuntu and Arch, x86_64", penguin,
     (("deb", "Debian package", "Phun_{v}_amd64.deb"), ("arch", "Arch package", "Phun_{v}_x86_64.pkg.tar.zst"))),
)


def header(name, subtitle, icon, files, version):
    begin()
    body = [f'<circle cx="120" cy="100" r="120" fill="url(#glow)"/>']
    body.append(rect(56, 36, 128, 128, r=29, fill=TILE, stroke=BORDER, sw=1.5))
    body.append(f'<g transform="translate(70 50)">{icon()}</g>')
    body.append(text("black", name, 220, 98, 46, FG, tracking=-0.5))
    body.append(text("semibold", subtitle, 220, 134, 20, MUTED))
    tag = f"v{version}"
    tw = width("mono", tag, 13)
    body.append(rect(220, 150, tw + 40, 26, r=8, fill=INSET))
    body.append(f'<circle cx="234" cy="163" r="3.5" fill="{RED}" class="pulse"/>')
    body.append(text("mono", tag, 244, 167.5, 13, SOFT))
    desc = f"Phun {version} for {name}: " + ", ".join(p.format(v=version) for _, _, p in files) + "."
    return frame(W, H, "\n".join(body), title=f"Phun for {name}", desc=desc, css=CSS, fade_from=0.4, corner=(1280 - 22 - 78, 14))


# The README shows two buttons to a row, each 49% of the page's width.
BW, BH = 640, 72


def button(name, label, fname):
    """One installer's download button. Each is its own image, so the README
    links each straight to its file."""
    begin()
    body = [rect(0, 0, BW, BH, r=14, fill=CARD, stroke=None)]
    body.append(rect(14, 14, 44, 44, r=11, fill=RED, stroke=None))
    body.append(f'<g class="drop">{path("M36 26v18m-7-7 7 7 7-7", "#fff", 2.8)}</g>')
    body.append(text("mono", fname, 76, 43.5, 21, FG))
    body.append(text("medium", label, BW - 22 - width("medium", label, 18), 43, 18, MUTED))
    desc = f"Download {fname}, Phun for {name} ({label})."
    return frame(BW, BH, "\n".join(body), title=f"Download {fname}", desc=desc, css=CSS, r=14, mark=False)


def current_version(readme=README):
    with open(readme, encoding="utf-8") as fh:
        m = re.search(r"<!-- latest-release:start -->.*?\[v?(\d+\.\d+\.\d+)\]", fh.read(), re.S)
    if not m:
        raise SystemExit("README.md has no latest release to draw the platform headers from.")
    return m.group(1)


def build_all(write, version=None):
    version = version or os.environ.get("PHUN_VERSION") or current_version()
    for stem, name, sub, icon, files in PLATFORMS:
        write(f"download/{stem}.svg", header(name, sub, icon, files, version))
        for slug, label, pattern in files:
            write(f"download/{stem}-{slug}.svg", button(name, label, pattern.format(v=version)))
