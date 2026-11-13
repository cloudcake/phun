#!/usr/bin/env python3
"""Release the changelog on main for a version built from an older commit.

The Release workflow pins cloudcake/phun-source to one commit, builds it, and
then writes the bookkeeping back to main. main may have moved on while the
release was building, and its Unreleased section may hold entries for commits
the release does not contain. Rewriting main's Unreleased heading as the
version (or rebasing that rewrite from the built commit) would file those
entries under a version that does not have them.

This takes the built commit's CHANGELOG.md and main's, and gives the version
exactly the entries the built commit had under Unreleased, in the words it
shipped with. Entries added on main since stay under Unreleased. An entry is
one `- ` bullet with its indented continuation lines, matched by its text with
whitespace collapsed within its `###` group; an entry main reworded, extended
or moved after the build is matched by likeness instead (see `matched`), left
out of Unreleased, and reported as a workflow warning.

Usage:
    release-changelog.py --version 0.5.1 --built built-CHANGELOG.md \
        --changelog CHANGELOG.md [--date YYYY-MM-DD]

Edits --changelog in place. Exits 0 and changes nothing when the built commit
had no entries or the version is already listed.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^## (?P<title>.+?)\s*$")
GROUP = re.compile(r"^### (?P<title>.+?)\s*$")


def unreleased_span(lines: list[str]) -> tuple[int, int] | None:
    """The line index of `## Unreleased` and of the next `## ` heading (or the
    end), or None when there is no Unreleased heading."""
    start = None
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m:
            continue
        if start is not None:
            return start, i
        if m.group("title").strip().lower() == "unreleased":
            start = i
    if start is None:
        return None
    return start, len(lines)


def has_version(lines: list[str], version: str) -> bool:
    for line in lines:
        m = HEADING.match(line)
        if m and m.group("title").split(" - ")[0].strip() == version:
            return True
    return False


def entry_key(group: str, block: list[str]) -> tuple[str, str]:
    return group.strip().lower(), " ".join(" ".join(block).split())


def entries(body: list[str]) -> list[tuple[str, list[str]]]:
    """Each bullet in `body` with its `###` group: (group, lines)."""
    out: list[tuple[str, list[str]]] = []
    group = ""
    block: list[str] | None = None
    for line in body:
        m = GROUP.match(line)
        if m:
            if block is not None:
                out.append((group, trimmed(block)))
                block = None
            group = m.group("title")
            continue
        if line.startswith("- "):
            if block is not None:
                out.append((group, trimmed(block)))
            block = [line]
        elif block is not None and (not line.strip() or line.startswith((" ", "\t"))):
            block.append(line)
        elif block is not None:
            out.append((group, trimmed(block)))
            block = None
    if block is not None:
        out.append((group, trimmed(block)))
    return out


def without(body: list[str], shipped: set[tuple[str, str]]) -> list[str]:
    """`body` with the bullets in `shipped` removed, then any `###` group left
    with no bullets, and runs of blank lines squeezed to one."""
    kept: list[str] = []
    group = ""
    block: list[str] | None = None

    def flush() -> None:
        nonlocal block
        if block is not None:
            body_lines = trimmed(block)
            tail = block[len(body_lines):]
            if entry_key(group, body_lines) not in shipped:
                kept.extend(body_lines)
            kept.extend(tail)
        block = None

    for line in body:
        m = GROUP.match(line)
        if m:
            flush()
            group = m.group("title")
            kept.append(line)
            continue
        if line.startswith("- "):
            flush()
            block = [line]
        elif block is not None and (not line.strip() or line.startswith((" ", "\t"))):
            block.append(line)
        else:
            flush()
            kept.append(line)
    flush()

    out: list[str] = []
    i = 0
    while i < len(kept):
        line = kept[i]
        if GROUP.match(line):
            j = i + 1
            while j < len(kept) and not GROUP.match(kept[j]):
                j += 1
            if any(item.strip() for item in kept[i + 1 : j]):
                out.extend(kept[i:j])
            i = j
            continue
        out.append(line)
        i += 1

    squeezed: list[str] = []
    for line in out:
        if not line.strip() and squeezed and not squeezed[-1].strip():
            continue
        squeezed.append(line)
    while squeezed and not squeezed[0].strip():
        squeezed.pop(0)
    while squeezed and not squeezed[-1].strip():
        squeezed.pop()
    return squeezed


SIMILAR = 0.6


def text_of(block: list[str]) -> str:
    return " ".join(" ".join(block).split())


def matched(
    shipped: list[tuple[str, list[str]]], pending: list[tuple[str, list[str]]]
) -> tuple[set[tuple[str, str]], list[tuple[str, str]]]:
    """Which of main's Unreleased entries (`pending`) the built commit shipped,
    as keys, and the shipped entries main edited since, as (built text, main
    text) pairs.

    An exact match (same text, same group) is the same entry. A shipped entry
    with no exact match is paired with the unpaired main entry most like it,
    in any group, when main's text starts with it or they are at least
    SIMILAR alike: main reworded, extended or moved it after the build, so it
    shipped and must not stay under Unreleased. A shipped entry with no such
    pair was removed on main; it still shipped, and nothing stays behind."""
    pending_keys = {entry_key(group, block) for group, block in pending}
    keys: set[tuple[str, str]] = set()
    edited: list[tuple[str, str]] = []
    loose: list[tuple[str, list[str]]] = []
    for group, block in shipped:
        key = entry_key(group, block)
        if key in pending_keys and key not in keys:
            keys.add(key)
        else:
            loose.append((group, block))
    for _, block in loose:
        built = text_of(block)
        best: tuple[float, tuple[str, str], str] | None = None
        for group, candidate in pending:
            key = entry_key(group, candidate)
            if key in keys:
                continue
            text = text_of(candidate)
            score = 1.0 if text.startswith(built.rstrip(".")) else difflib.SequenceMatcher(None, built, text).ratio()
            if score >= SIMILAR and (best is None or score > best[0]):
                best = (score, key, text)
        if best is not None:
            keys.add(best[1])
            edited.append((built, best[2]))
    return keys, edited


def trimmed(body: list[str]) -> list[str]:
    start = 0
    end = len(body)
    while start < end and not body[start].strip():
        start += 1
    while end > start and not body[end - 1].strip():
        end -= 1
    return body[start:end]


def edited_since(main_text: str, built_text: str) -> list[tuple[str, str]]:
    """The built commit's Unreleased entries main has edited since, as
    (built text, main text) pairs."""
    main = main_text.split("\n")
    built = built_text.split("\n")
    built_span = unreleased_span(built)
    main_span = unreleased_span(main)
    if built_span is None or main_span is None:
        return []
    shipped = entries(built[built_span[0] + 1 : built_span[1]])
    return matched(shipped, entries(main[main_span[0] + 1 : main_span[1]]))[1]


def release(main_text: str, built_text: str, version: str, today: str) -> str | None:
    """main's changelog with the built commit's Unreleased entries released as
    `version`, or None when there is nothing to release or it is listed."""
    main = main_text.split("\n")
    built = built_text.split("\n")
    if has_version(main, version):
        return None
    built_span = unreleased_span(built)
    main_span = unreleased_span(main)
    if built_span is None or main_span is None:
        return None
    shipped_body = trimmed(built[built_span[0] + 1 : built_span[1]])
    shipped = entries(shipped_body)
    if not shipped:
        return None
    start, end = main_span
    keys, _ = matched(shipped, entries(main[start + 1 : end]))
    left = without(main[start + 1 : end], keys)
    unreleased = ["## Unreleased", ""] + (left + [""] if left else [])
    released = [f"## {version} - {today}", ""] + shipped_body + [""]
    return "\n".join(main[:start] + unreleased + released + main[end:])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", required=True, help="The released version, e.g. 0.5.1")
    parser.add_argument("--built", required=True, help="CHANGELOG.md as it was in the built commit")
    parser.add_argument("--changelog", required=True, help="main's CHANGELOG.md, edited in place")
    parser.add_argument("--date", default=_dt.date.today().isoformat(), help="Release date (default: today)")
    args = parser.parse_args(argv)

    changelog = Path(args.changelog)
    main_text = changelog.read_text(encoding="utf-8")
    built_text = Path(args.built).read_text(encoding="utf-8")
    for built, now in edited_since(main_text, built_text):
        print(
            f"::warning title=Changelog entry edited after the build::{args.version} lists the "
            f"wording it shipped with ({built!r}); main has since changed it to {now!r}. "
            "It is no longer listed under Unreleased."
        )
    text = release(main_text, built_text, args.version, args.date)
    if text is None:
        print(f"note: nothing to release for {args.version} (no built entries, or it is already listed)")
        return 0
    changelog.write_text(text, encoding="utf-8")
    print(f"released the built commit's Unreleased entries as {args.version} - {args.date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
