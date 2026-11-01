#!/usr/bin/env python3
"""Fixture tests for stamp-version.py. Run from the repo root:

    python3 .github/scripts/test-stamp-version.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "stamp-version.py"


def stamp(root: Path, tag: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--tag", tag, "--root", str(root)],
        text=True,
        capture_output=True,
    )


class StampVersionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "apps/phun-gui/src-tauri").mkdir(parents=True)
        (self.root / "apps/phun-gui/src/views").mkdir(parents=True)
        (self.root / "crates/phun-core").mkdir(parents=True)
        (self.root / "bin/phun").mkdir(parents=True)
        (self.root / "Cargo.toml").write_text(
            "[workspace]\n"
            'members = ["crates/phun-core", "bin/phun", "apps/phun-gui/src-tauri"]\n'
            "\n"
            "[workspace.package]\n"
            'version = "0.0.1"\n'
            "\n"
            "[workspace.dependencies]\n"
            'phun-core = { path = "crates/phun-core", version = "0.0.1" }\n'
            'serde = { version = "1.0" }\n'
        )
        (self.root / "crates/phun-core/Cargo.toml").write_text(
            "[package]\n"
            'name = "phun-core"\n'
            'version = "0.0.1"\n'
            "\n"
            "[dependencies]\n"
            'tiny-crate = "0.0.1"\n'
        )
        (self.root / "bin/phun/Cargo.toml").write_text(
            "[package]\n"
            'name = "phun"\n'
            'version = "0.0.1"\n'
            "\n"
            "[dependencies]\n"
            'phun-core = { path = "../../crates/phun-core", version = "0.0.1" }\n'
        )
        (self.root / "apps/phun-gui/src-tauri/Cargo.toml").write_text(
            "[package]\n"
            'name = "phun-gui"\n'
            'version = "0.0.1"\n'
        )
        (self.root / "Cargo.lock").write_text(
            "version = 4\n"
            "\n"
            "[[package]]\n"
            'name = "phun"\n'
            'version = "0.0.1"\n'
            "\n"
            "[[package]]\n"
            'name = "phun-core"\n'
            'version = "0.0.1"\n'
            "\n"
            "[[package]]\n"
            'name = "phun-gui"\n'
            'version = "0.0.1"\n'
            "\n"
            "[[package]]\n"
            'name = "tiny-crate"\n'
            'version = "0.0.1"\n'
            'source = "registry+https://github.com/rust-lang/crates.io-index"\n'
        )
        (self.root / "apps/phun-gui/src-tauri/tauri.conf.json").write_text(
            "{\n"
            '  "productName": "Phun",\n'
            '  "version": "0.0.1",\n'
            '  "identifier": "app.phun.desktop"\n'
            "}\n"
        )
        (self.root / "apps/phun-gui/package.json").write_text(
            "{\n"
            '  "name": "phun-gui",\n'
            '  "version": "0.0.1",\n'
            '  "dependencies": {\n'
            '    "left-pad": "0.0.1"\n'
            "  }\n"
            "}\n"
        )
        (self.root / "apps/phun-gui/package-lock.json").write_text(
            json.dumps(
                {
                    "name": "phun-gui",
                    "version": "0.0.1",
                    "lockfileVersion": 3,
                    "packages": {
                        "": {"name": "phun-gui", "version": "0.0.1"},
                        "node_modules/left-pad": {"version": "0.0.1"},
                    },
                },
                indent=2,
            )
            + "\n"
        )
        (self.root / "bin/phun/src").mkdir(parents=True)
        (self.root / "bin/phun/src/main.rs").write_text(
            'const APP_VERSION: &str = "0.0.1";\n'
            'fn other() { let _ = "0.0.1"; }\n'
        )
        (self.root / "apps/phun-gui/src/views/AboutView.vue").write_text(
            "<script setup>\n"
            "const version = '0.0.1'\n"
            "</script>\n"
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_releases_the_changelog_unreleased_section(self) -> None:
        changelog = self.root / "CHANGELOG.md"
        changelog.write_text(
            "# Changelog\n\nIntro.\n\n## Unreleased\n\n### Improved\n\n- A new thing.\n\n"
            "## 0.0.1 - 2026-01-01\n\n### New\n\n- First.\n"
        )
        result = stamp(self.root, "v0.0.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        text = changelog.read_text()
        self.assertIn("## Unreleased\n\n## 0.0.2 - ", text)
        self.assertIn("## 0.0.2 - 20", text)
        self.assertIn("### Improved\n\n- A new thing.", text)
        self.assertIn("## 0.0.1 - 2026-01-01", text)
        self.assertEqual(text.count("## Unreleased"), 1)
        self.assertIn("CHANGELOG.md", result.stdout)

    def test_changelog_untouched_when_unreleased_is_empty_or_version_exists(self) -> None:
        changelog = self.root / "CHANGELOG.md"
        empty = "# Changelog\n\n## Unreleased\n\n## 0.0.1 - 2026-01-01\n\n- First.\n"
        changelog.write_text(empty)
        self.assertEqual(stamp(self.root, "v0.0.2").returncode, 0)
        self.assertEqual(changelog.read_text(), empty)
        listed = "# Changelog\n\n## Unreleased\n\n- Pending.\n\n## 0.0.2 - 2026-02-02\n\n- Done.\n"
        changelog.write_text(listed)
        self.assertEqual(stamp(self.root, "v0.0.2").returncode, 0)
        self.assertEqual(changelog.read_text(), listed)

    def test_rejects_non_semver(self) -> None:
        result = stamp(self.root, "latest")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a semver", result.stderr)

    def test_stamps_from_v_tag(self) -> None:
        result = stamp(self.root, "v0.0.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("stamped files:", result.stdout)
        for rel in (
            "Cargo.toml",
            "Cargo.lock",
            "crates/phun-core/Cargo.toml",
            "bin/phun/Cargo.toml",
            "apps/phun-gui/src-tauri/Cargo.toml",
            "apps/phun-gui/src-tauri/tauri.conf.json",
            "apps/phun-gui/package.json",
            "apps/phun-gui/package-lock.json",
            "bin/phun/src/main.rs",
            "apps/phun-gui/src/views/AboutView.vue",
        ):
            self.assertIn(rel, result.stdout)

        workspace = (self.root / "Cargo.toml").read_text()
        self.assertIn('version = "0.0.2"', workspace)
        self.assertIn('phun-core = { path = "crates/phun-core", version = "0.0.2" }', workspace)
        self.assertIn('serde = { version = "1.0" }', workspace)

        core = (self.root / "crates/phun-core/Cargo.toml").read_text()
        self.assertIn('version = "0.0.2"', core)
        self.assertIn('tiny-crate = "0.0.1"', core)

        lock = (self.root / "Cargo.lock").read_text()
        self.assertIn('name = "phun"\nversion = "0.0.2"', lock)
        self.assertIn('name = "tiny-crate"\nversion = "0.0.1"', lock)

        tauri = json.loads((self.root / "apps/phun-gui/src-tauri/tauri.conf.json").read_text())
        self.assertEqual(tauri["version"], "0.0.2")

        package = json.loads((self.root / "apps/phun-gui/package.json").read_text())
        self.assertEqual(package["version"], "0.0.2")
        self.assertEqual(package["dependencies"]["left-pad"], "0.0.1")

        lock_js = json.loads((self.root / "apps/phun-gui/package-lock.json").read_text())
        self.assertEqual(lock_js["version"], "0.0.2")
        self.assertEqual(lock_js["packages"][""]["version"], "0.0.2")
        self.assertEqual(lock_js["packages"]["node_modules/left-pad"]["version"], "0.0.1")

        rust = (self.root / "bin/phun/src/main.rs").read_text()
        self.assertIn('const APP_VERSION: &str = "0.0.2";', rust)
        self.assertIn('let _ = "0.0.1";', rust)

        about = (self.root / "apps/phun-gui/src/views/AboutView.vue").read_text()
        self.assertIn("const version = '0.0.2'", about)
        self.assertIn("hardcoded GUI version literals", result.stdout)
        self.assertIn("apps/phun-gui/src/views/AboutView.vue", result.stdout)

    def test_prerelease_tag(self) -> None:
        result = stamp(self.root, "v2.1.0-rc.1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('version = "2.1.0-rc.1"', (self.root / "Cargo.toml").read_text())

    def test_missing_tauri_conf_fails(self) -> None:
        (self.root / "apps/phun-gui/src-tauri/tauri.conf.json").unlink()
        result = stamp(self.root, "v0.0.2")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tauri.conf.json", result.stderr)

    def test_already_stamped_is_ok(self) -> None:
        first = stamp(self.root, "v0.0.2")
        self.assertEqual(first.returncode, 0, first.stderr)
        second = stamp(self.root, "v0.0.2")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("no version fields needed rewriting", second.stdout)

    def test_get_version_about_is_not_flagged(self) -> None:
        (self.root / "apps/phun-gui/src/views/AboutView.vue").write_text(
            "<script setup>\n"
            "import { getVersion } from '@tauri-apps/api/app'\n"
            "const version = await getVersion()\n"
            "</script>\n"
        )
        result = stamp(self.root, "v0.0.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no hardcoded GUI version literal found", result.stdout)
        self.assertIn("AboutView.vue uses getVersion", result.stdout)


if __name__ == "__main__":
    unittest.main()
