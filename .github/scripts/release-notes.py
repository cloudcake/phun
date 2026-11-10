#!/usr/bin/env python3
"""Write a release's notes: its changelog section, then the install notes.

The Release workflow runs this before publishing, and the Release notes
workflow runs it to rewrite an existing release's notes. The changes come
from phun-source's CHANGELOG.md: the `## <version>` section when the version
is already released there, otherwise `## Unreleased` (a release builds the
commit before the sync job renames that heading). Wrapped lines are joined,
because GitHub keeps every line break in release notes.

    release-notes.py --changelog CHANGELOG.md --tag v0.3.2 [--signed] > notes.md
"""
import argparse
import re
import sys

HEADING = re.compile(r"^## (?P<title>.+?)\s*$")


def plain_version(tag):
    """`0.3.2` for `v0.3.2`, or the tag without its `v` for anything else."""
    tag = tag.strip()
    return tag[1:] if tag[:1] in ("v", "V") else tag


def section(changelog, version):
    """The body under `## <version>`, else under `## Unreleased`, as lines."""
    lines = changelog.split("\n")
    found = {}
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m:
            continue
        title = m.group("title").split(" - ")[0].strip()
        key = "unreleased" if title.lower() == "unreleased" else title
        if key in found:
            continue
        end = next((j for j in range(i + 1, len(lines)) if HEADING.match(lines[j])), len(lines))
        found[key] = lines[i + 1 : end]
    for key in (version, "unreleased"):
        body = found.get(key, [])
        if any(line.lstrip().startswith("- ") for line in body):
            return body
    return []


def unwrap(body):
    """Join each list item's and paragraph's wrapped lines into one line."""
    out = []
    for line in body:
        stripped = line.strip()
        joinable = out and out[-1] and not out[-1].startswith("#")
        if stripped and joinable and not stripped.startswith(("- ", "#")):
            out[-1] = f"{out[-1]} {stripped}"
        else:
            out.append(stripped if not stripped.startswith("- ") else line.rstrip())
    while out and not out[0]:
        out.pop(0)
    while out and not out[-1]:
        out.pop()
    return out


def install_notes(tag, signed):
    signing = (
        "Each installer has a minisign signature (.minisig) and SHA256SUMS lists their checksums."
        if signed
        else "Updater signing is off."
    )
    return (
        f"Phun {tag}. Mac builds are ad-hoc signed, not notarized; on first launch right-click Phun > Open, "
        "or run `xattr -cr /Applications/Phun.app`. Apple Silicon Macs use the apple-silicon dmg, Intel Macs "
        "the intel dmg. The Windows installer is unsigned, so SmartScreen may warn ('More info' > 'Run anyway'). "
        "On Debian and Ubuntu install the .deb; on Arch run `sudo pacman -U ./Phun_<version>_x86_64.pkg.tar.zst`. "
        f"{signing}"
    )


def notes(changelog, tag, signed):
    changes = unwrap(section(changelog, plain_version(tag)))
    parts = []
    if changes:
        parts.append("## What's changed\n\n" + "\n".join(changes))
    parts.append("## Installing\n\n" + install_notes(tag, signed))
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changelog", required=True, help="Path to phun-source's CHANGELOG.md")
    parser.add_argument("--tag", required=True, help="Release tag, e.g. v0.3.2")
    parser.add_argument("--signed", action="store_true", help="The installers have .minisig signatures")
    args = parser.parse_args(argv)
    try:
        with open(args.changelog, encoding="utf-8") as fh:
            changelog = fh.read()
    except OSError as err:
        print(f"::warning title=No changelog in the release notes::{err}", file=sys.stderr)
        changelog = ""
    out = notes(changelog, args.tag, args.signed)
    if "## What's changed" not in out:
        print(f"::warning title=No changelog in the release notes::CHANGELOG.md has no entries for {args.tag} or under Unreleased.", file=sys.stderr)
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
