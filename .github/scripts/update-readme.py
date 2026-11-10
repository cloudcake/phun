#!/usr/bin/env python3
"""Point the README's download block at a release's installers.

The Release workflow runs this after publishing. Everything between the
`<!-- latest-release:start -->` and `<!-- latest-release:end -->` markers in
README.md is replaced with the version and a card image per installer (its
platform's icon, name and version with a full-length download button) that
links straight to it, so the README always offers the newest build. The
cards carry the version too; the workflow redraws them with `.github/readme/build.py
platforms` afterwards. Pre-release tags (anything
that is not a plain X.Y.Z) leave the README alone.

    update-readme.py --tag v0.2.0 --repo cloudcake/phun \
        --asset Phun_0.2.0_amd64.deb --asset Phun_0.2.0_apple-silicon.dmg ...
"""
import argparse
import re
import sys

START = "<!-- latest-release:start -->"
END = "<!-- latest-release:end -->"

# Each platform's installers, by the end of the installer's file name, in the
# order the README lists them. Each has its own card image,
# `download/<platform>-<slug>.svg`, drawn by .github/readme/platforms.py with
# the same slugs.
PLATFORMS = (
    ("macos", "macOS", (("_apple-silicon.dmg", "apple-silicon", "Apple Silicon"), ("_intel.dmg", "intel", "Intel"))),
    ("windows", "Windows", (("-setup.exe", "installer", "Installer"),)),
    ("linux", "Linux", (("_amd64.deb", "deb", "Debian package"), ("_x86_64.pkg.tar.zst", "arch", "Arch package"))),
)
# Bump when the images are redrawn: GitHub caches the images by URL for
# minutes, so a new drawing needs a new URL to show at once.
ART_REVISION = 6
SUFFIXES = tuple(suffix for _, _, files in PLATFORMS for suffix, _, _ in files)


def plain_version(tag):
    """`0.2.0` for `v0.2.0`, or None for a pre-release or a malformed tag."""
    m = re.fullmatch(r"[vV]?(\d+\.\d+\.\d+)", tag.strip())
    return m.group(1) if m else None


def block(tag, repo, assets):
    """The markdown that goes between the markers."""
    base = f"https://github.com/{repo}/releases"
    version = plain_version(tag) or tag
    lines = [START, f"Latest release: **[{tag}]({base}/tag/{tag})**", ""]
    for stem, name, files in PLATFORMS:
        for suffix, slug, label in files:
            for asset in sorted(assets):
                if asset.endswith(suffix):
                    url = f"{base}/download/{tag}/{asset}"
                    src = f".github/readme/download/{stem}-{slug}.svg?v={version}.{ART_REVISION}"
                    lines.append(f'<a href="{url}"><img src="{src}" alt="Download Phun {version} for {name}, {label}: {asset}" width="100%"></a>')
                    lines.append("")
    lines.append(END)
    return "\n".join(lines)


def rewrite(readme, tag, repo, assets):
    """`readme` with its download block replaced, or None when it has no markers."""
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        return None
    return pattern.sub(lambda _m: block(tag, repo, assets), readme, count=1)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tag", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--asset", action="append", default=[])
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args(argv)
    if plain_version(args.tag) is None:
        print(f"{args.tag} is a pre-release; the README keeps its current release.")
        return 0
    if not any(name.endswith(s) for name in args.asset for s in SUFFIXES):
        print("no known installers were given; the README is left as it is.", file=sys.stderr)
        return 1
    with open(args.readme, encoding="utf-8") as fh:
        text = fh.read()
    updated = rewrite(text, args.tag, args.repo, args.asset)
    if updated is None:
        print(f"{args.readme} has no {START} block.", file=sys.stderr)
        return 1
    if updated != text:
        with open(args.readme, "w", encoding="utf-8") as fh:
            fh.write(updated)
        print(f"{args.readme} now offers {args.tag}.")
    else:
        print(f"{args.readme} already offers {args.tag}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
