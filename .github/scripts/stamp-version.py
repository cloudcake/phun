#!/usr/bin/env python3
"""Stamp a release tag version into a cloudcake/phun checkout.

Used by the Release workflow after the private source is checked out and
before any OS job builds. Strips a leading 'v' from the tag and requires
a semver. Writes the version into Cargo.toml / Cargo.lock workspace
crates, tauri.conf.json, package.json, package-lock.json, and any other
version constant the GUI or daemon is likely to display.

Does not commit. Prints every file it edits.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
# Exact app versions we are willing to rewrite (not "1.0", not "^0.0.1").
APP_VERSION = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
PACKAGE_SECTIONS = {"package", "workspace.package"}
PATH_DEP_SECTIONS = {
    "dependencies",
    "dev-dependencies",
    "build-dependencies",
    "workspace.dependencies",
}
SKIP_DIR_NAMES = {
    ".git",
    ".phun-releases-tools",
    "node_modules",
    "target",
    "dist",
    "vendor",
}
SOURCE_SUFFIXES = {".rs", ".vue", ".ts", ".tsx", ".js", ".jsx", ".json", ".toml"}
VERSIONISH = re.compile(
    r"(?i)(app[_-]?version|phun[_-]?version|short[_-]?version|"
    r"daemon[_-]?version|display[_-]?version|pkg[_-]?version|"
    r"\bversion\b)"
)
SEMVER_LITERAL = re.compile(
    r"""(['"])((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"""
    r"""(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)\1"""
)
CARGO_PKG_VERSION = re.compile(r'^\s*version\s*=\s*"([^"]+)"\s*(?:#.*)?$')
CARGO_PKG_NAME = re.compile(r'^\s*name\s*=\s*"([^"]+)"\s*(?:#.*)?$')
INLINE_PATH = re.compile(r"""\bpath\s*=""")
INLINE_VERSION = re.compile(
    r"""(\bversion\s*=\s*")((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"""
    r"""(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)(")"""
)
JSON_VERSION = re.compile(
    r"""("version"\s*:\s*")((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"""
    r"""(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)(")"""
)


def die(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def version_from_tag(tag: str) -> str:
    if not tag or tag.strip() != tag or any(c.isspace() for c in tag):
        die(f"tag must be a single token, got {tag!r}")
    version = tag[1:] if tag[:1] in "vV" else tag
    if not version or not SEMVER.fullmatch(version):
        die(f"tag {tag!r} is not a semver (optionally prefixed with 'v')")
    return version


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        yield path


def section_name(header: str) -> str:
    return header.strip()[1:-1].strip()


def is_table_header(stripped: str) -> bool:
    return stripped.startswith("[") and stripped.endswith("]") and not stripped.startswith("[[")


def stamp_cargo_toml(path: Path, version: str) -> bool:
    original = path.read_text()
    lines = original.splitlines(keepends=True)
    out = []
    section = ""
    subsection_has_path = False
    changed = False

    def apply_inline(line: str) -> str:
        nonlocal changed
        if not INLINE_PATH.search(line):
            return line
        new, n = INLINE_VERSION.subn(rf"\g<1>{version}\3", line, count=1)
        if n and new != line:
            changed = True
        return new

    for line in lines:
        stripped = line.strip()
        if is_table_header(stripped):
            section = section_name(stripped)
            subsection_has_path = False
            out.append(line)
            continue

        if section in PACKAGE_SECTIONS:
            match = CARGO_PKG_VERSION.match(stripped)
            if match and APP_VERSION.fullmatch(match.group(1)):
                indent = line[: len(line) - len(line.lstrip())]
                comment = ""
                hash_at = stripped.find(" #")
                if hash_at != -1:
                    comment = stripped[hash_at:]
                newline = "\n" if line.endswith("\n") else ""
                replacement = f'{indent}version = "{version}"{comment}{newline}'
                if replacement != line:
                    changed = True
                out.append(replacement)
                continue

        top = section.split(".", 1)[0] if section else ""
        if section in PATH_DEP_SECTIONS or top in PATH_DEP_SECTIONS:
            if INLINE_PATH.search(stripped):
                subsection_has_path = True
            if "path" in stripped and "=" in stripped and "path" == stripped.split("=", 1)[0].strip():
                subsection_has_path = True
            if INLINE_PATH.search(line) and INLINE_VERSION.search(line):
                out.append(apply_inline(line))
                continue
            if subsection_has_path:
                match = CARGO_PKG_VERSION.match(stripped)
                if match and APP_VERSION.fullmatch(match.group(1)):
                    indent = line[: len(line) - len(line.lstrip())]
                    newline = "\n" if line.endswith("\n") else ""
                    replacement = f'{indent}version = "{version}"{newline}'
                    if replacement != line:
                        changed = True
                    out.append(replacement)
                    continue

        out.append(line)

    if not changed:
        return False
    path.write_text("".join(out))
    return True


def workspace_package_names(root: Path) -> set[str]:
    names: set[str] = set()
    for path in iter_files(root):
        if path.name != "Cargo.toml":
            continue
        section = ""
        pending_name = None
        pending_version = False
        for raw in path.read_text().splitlines():
            stripped = raw.strip()
            if is_table_header(stripped):
                if section in PACKAGE_SECTIONS and pending_name and pending_version:
                    names.add(pending_name)
                section = section_name(stripped)
                pending_name = None
                pending_version = False
                continue
            if section not in PACKAGE_SECTIONS:
                continue
            name_match = CARGO_PKG_NAME.match(stripped)
            if name_match:
                pending_name = name_match.group(1)
            if CARGO_PKG_VERSION.match(stripped) or stripped.startswith("version.workspace"):
                pending_version = True
        if section in PACKAGE_SECTIONS and pending_name and pending_version:
            names.add(pending_name)
    return names


def stamp_cargo_lock(path: Path, version: str, names: set[str]) -> bool:
    if not names:
        return False
    original = path.read_text()
    chunks = re.split(r"(?=^\[\[package\]\])", original, flags=re.M)
    changed = False
    out = []
    for chunk in chunks:
        if not chunk.startswith("[[package]]"):
            out.append(chunk)
            continue
        name_match = re.search(r'(?m)^name\s*=\s*"([^"]+)"\s*$', chunk)
        if not name_match or name_match.group(1) not in names:
            out.append(chunk)
            continue
        if re.search(r'(?m)^source\s*=', chunk):
            out.append(chunk)
            continue
        new, n = re.subn(
            r'(?m)^(version\s*=\s*")([^"]+)(")\s*$',
            rf"\g<1>{version}\3",
            chunk,
            count=1,
        )
        if n and new != chunk:
            changed = True
        out.append(new)
    if not changed:
        return False
    path.write_text("".join(out))
    return True


def stamp_json_app_version(path: Path, version: str, *, first_only: bool) -> bool:
    original = path.read_text()
    if first_only:
        new, n = JSON_VERSION.subn(rf"\g<1>{version}\3", original, count=1)
    else:
        new, n = JSON_VERSION.subn(rf"\g<1>{version}\3", original)
    if not n or new == original:
        return False
    path.write_text(new)
    return True


def stamp_package_lock(path: Path, version: str) -> bool:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        die(f"{path}: invalid JSON: {exc}")
    changed = False
    if isinstance(data.get("version"), str) and APP_VERSION.fullmatch(data["version"]):
        if data["version"] != version:
            data["version"] = version
            changed = True
    packages = data.get("packages")
    if isinstance(packages, dict):
        root_pkg = packages.get("")
        if isinstance(root_pkg, dict) and isinstance(root_pkg.get("version"), str):
            if APP_VERSION.fullmatch(root_pkg["version"]) and root_pkg["version"] != version:
                root_pkg["version"] = version
                changed = True
    if not changed:
        return False
    path.write_text(json.dumps(data, indent=2) + "\n")
    return True


def stamp_source_constants(path: Path, version: str) -> bool:
    original = path.read_text()
    changed = False
    out_lines = []
    for line in original.splitlines(keepends=True):
        if not VERSIONISH.search(line):
            out_lines.append(line)
            continue
        if "CARGO_PKG_VERSION" in line or "workspace = true" in line:
            out_lines.append(line)
            continue
        # Skip dependency pins (Cargo / npm ranges) that are not display constants.
        if re.search(r"^\s*[A-Za-z0-9_-]+\s*=\s*\{\s*version\s*=", line):
            out_lines.append(line)
            continue

        def repl(match: re.Match[str]) -> str:
            nonlocal changed
            quote, current = match.group(1), match.group(2)
            if current == version:
                return match.group(0)
            changed = True
            return f"{quote}{version}{quote}"

        out_lines.append(SEMVER_LITERAL.sub(repl, line))
    if not changed:
        return False
    path.write_text("".join(out_lines))
    return True


def hardcoded_gui_files(root: Path) -> list[str]:
    gui_src = root / "apps" / "phun-gui" / "src"
    if not gui_src.is_dir():
        return []
    found = []
    for path in gui_src.rglob("*"):
        if path.suffix not in {".vue", ".ts", ".tsx", ".js", ".jsx"}:
            continue
        text = path.read_text(errors="replace")
        for line in text.splitlines():
            if not VERSIONISH.search(line):
                continue
            if "getVersion" in line or "import.meta.env" in line:
                continue
            if SEMVER_LITERAL.search(line):
                found.append(str(path.relative_to(root)))
                break
    return sorted(found)


def required_exists(root: Path, rel: str) -> Path:
    path = root / rel
    if not path.is_file():
        die(f"missing required version file: {rel}")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="Release tag, e.g. v0.0.2")
    parser.add_argument(
        "--root",
        default=".",
        help="Path to the phun checkout (default: current directory)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        die(f"phun checkout not found: {root}")

    version = version_from_tag(args.tag)
    print(f"stamping version {version} (from tag {args.tag}) into {root}")

    required_exists(root, "apps/phun-gui/src-tauri/tauri.conf.json")
    required_exists(root, "apps/phun-gui/package.json")
    cargo_tomls = [
        path
        for path in iter_files(root)
        if path.name == "Cargo.toml"
    ]
    if not cargo_tomls:
        die("no Cargo.toml files found in the phun checkout")

    edited: list[str] = []

    names = workspace_package_names(root)
    if not names:
        die("no workspace/crate package names found in Cargo.toml files")
    print("workspace crates: " + ", ".join(sorted(names)))

    for path in cargo_tomls:
        if stamp_cargo_toml(path, version):
            edited.append(str(path.relative_to(root)))

    lock = root / "Cargo.lock"
    if lock.is_file():
        if stamp_cargo_lock(lock, version, names):
            edited.append("Cargo.lock")
    else:
        print("note: Cargo.lock not present; skipping lockfile stamp")

    tauri_conf = root / "apps/phun-gui/src-tauri/tauri.conf.json"
    if stamp_json_app_version(tauri_conf, version, first_only=True):
        edited.append("apps/phun-gui/src-tauri/tauri.conf.json")
    for extra in (
        root / "apps/phun-gui/src-tauri/Tauri.toml",
        root / "apps/phun-gui/src-tauri/tauri.macos.conf.json",
        root / "apps/phun-gui/src-tauri/tauri.linux.conf.json",
    ):
        if extra.is_file():
            if extra.suffix == ".json":
                if stamp_json_app_version(extra, version, first_only=True):
                    edited.append(str(extra.relative_to(root)))
            elif stamp_cargo_toml(extra, version):
                edited.append(str(extra.relative_to(root)))

    package_json = root / "apps/phun-gui/package.json"
    if stamp_json_app_version(package_json, version, first_only=True):
        edited.append("apps/phun-gui/package.json")

    package_lock = root / "apps/phun-gui/package-lock.json"
    if package_lock.is_file() and stamp_package_lock(package_lock, version):
        edited.append("apps/phun-gui/package-lock.json")

    for path in iter_files(root):
        rel = str(path.relative_to(root))
        if rel in edited:
            continue
        if path.suffix not in SOURCE_SUFFIXES:
            continue
        if path.name in {
            "Cargo.toml",
            "Cargo.lock",
            "Cargo.toml.orig",
            "package.json",
            "package-lock.json",
            "tauri.conf.json",
            "rust-toolchain.toml",
        }:
            continue
        if path.name.startswith("tauri.") and path.suffix == ".json":
            continue
        try:
            if stamp_source_constants(path, version):
                edited.append(rel)
        except UnicodeDecodeError:
            continue

    if not edited:
        print("no version fields needed rewriting (already at this version)")
    else:
        print("stamped files:")
        for rel in sorted(edited):
            print(f"  {rel}")

    missing_required = []
    for rel in (
        "apps/phun-gui/src-tauri/tauri.conf.json",
        "apps/phun-gui/package.json",
    ):
        text = (root / rel).read_text()
        if f'"{version}"' not in text:
            missing_required.append(rel)
    cargo_ok = False
    for path in cargo_tomls:
        if f'version = "{version}"' in path.read_text():
            cargo_ok = True
            break
    if not cargo_ok:
        missing_required.append("Cargo.toml (package version)")
    if missing_required:
        die("stamp did not land in: " + ", ".join(missing_required))

    hardcoded = hardcoded_gui_files(root)
    if hardcoded:
        print("hardcoded GUI version literals (follow-up: switch these to getVersion):")
        for rel in hardcoded:
            print(f"  {rel}")
    else:
        print(
            "no hardcoded GUI version literal found under apps/phun-gui/src; "
            "confirm apps/phun-gui/src/views/AboutView.vue uses getVersion / AboutMetadata"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
