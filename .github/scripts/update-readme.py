#!/usr/bin/env python3
"""Point the README's download block at a release's installers.

The Release workflow runs this after publishing. Everything between the
`<!-- latest-release:start -->` and `<!-- latest-release:end -->` markers in
README.md is replaced with the version and a direct link to each installer,
so the README always offers the newest build. Pre-release tags (anything
that is not a plain X.Y.Z) leave the README alone.

    update-readme.py --tag v0.2.0 --repo cloudcake/phun \
        --asset Phun_0.2.0_amd64.deb --asset Phun_0.2.0_apple-silicon.dmg ...
"""
import argparse
import re
import sys

START = "<!-- latest-release:start -->"
END = "<!-- latest-release:end -->"

# Which system each installer is for, by the end of its file name, in the
# order the table lists them.
SYSTEMS = (
    ("_apple-silicon.dmg", "macOS, Apple Silicon"),
    ("_intel.dmg", "macOS, Intel"),
    ("-setup.exe", "Windows 10 and 11, x64"),
    ("_amd64.deb", "Linux, x86_64 (Debian, Ubuntu)"),
)


def plain_version(tag):
    """`0.2.0` for `v0.2.0`, or None for a pre-release or a malformed tag."""
    m = re.fullmatch(r"[vV]?(\d+\.\d+\.\d+)", tag.strip())
    return m.group(1) if m else None


def block(tag, repo, assets):
    """The markdown that goes between the markers."""
    base = f"https://github.com/{repo}/releases"
    lines = [
        START,
        f"Latest release: **[{tag}]({base}/tag/{tag})**",
        "",
        "| System | Installer |",
        "| --- | --- |",
    ]
    for suffix, system in SYSTEMS:
        for name in sorted(assets):
            if name.endswith(suffix):
                lines.append(f"| {system} | [{name}]({base}/download/{tag}/{name}) |")
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
    if not any(name.endswith(s) for name in args.asset for s, _ in SYSTEMS):
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
