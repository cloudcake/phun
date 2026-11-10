"""Run with `python3 -m unittest discover -s .github/scripts`."""
import importlib.util
import os
import unittest

spec = importlib.util.spec_from_file_location("release_notes", os.path.join(os.path.dirname(__file__), "release-notes.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CHANGELOG = """# Changelog

Intro text that mentions `## Unreleased`.

## Unreleased

### Added

- A new thing that wraps
  onto a second line.

## 0.3.1 - 2026-11-10

### Fixed

- A fix that wraps
  over two lines.
- Another fix.

## 0.3.0 - 2026-11-09

### Added

- The first thing.
"""


class ReleaseNotes(unittest.TestCase):
    def test_picks_the_section(self):
        cases = [
            ("released version", "v0.3.1", ["- A fix that wraps over two lines.", "- Another fix."], "A new thing"),
            ("older version", "v0.3.0", ["- The first thing."], "Another fix"),
            ("not yet renamed, so Unreleased", "v0.3.2", ["- A new thing that wraps onto a second line."], "Another fix"),
            ("pre-release tag", "v0.3.2-rc.1", ["- A new thing that wraps onto a second line."], "The first thing"),
        ]
        for label, tag, present, absent in cases:
            with self.subTest(label):
                out = mod.notes(CHANGELOG, tag, signed=False)
                self.assertTrue(out.startswith("## What's changed\n\n"), out)
                for line in present:
                    self.assertIn(f"\n{line}\n", out)
                self.assertNotIn(absent, out)
                self.assertIn(f"## Installing\n\nPhun {tag}. Mac builds", out)

    def test_keeps_the_subheadings(self):
        out = mod.notes(CHANGELOG, "v0.3.1", signed=False)
        self.assertIn("## What's changed\n\n### Fixed\n\n- A fix", out)

    def test_install_notes_only_without_entries(self):
        cases = [
            ("no changelog", ""),
            ("empty Unreleased", "## Unreleased\n\n## 0.1.0 - 2026-01-01\n\n- Old.\n"),
        ]
        for label, changelog in cases:
            with self.subTest(label):
                out = mod.notes(changelog, "v0.3.2", signed=False)
                self.assertTrue(out.startswith("## Installing\n\n"), out)
                self.assertNotIn("What's changed", out)

    def test_signing_sentence(self):
        cases = [(True, "Each installer has a minisign signature"), (False, "Updater signing is off.")]
        for signed, sentence in cases:
            with self.subTest(signed=signed):
                self.assertIn(sentence, mod.notes(CHANGELOG, "v0.3.1", signed=signed))


if __name__ == "__main__":
    unittest.main()
