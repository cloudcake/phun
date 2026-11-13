"""Run with `python3 -m unittest discover -s .github/scripts`."""
import contextlib
import importlib.util
import io
import os
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "release_changelog", os.path.join(os.path.dirname(__file__), "release-changelog.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

HEAD = "# Changelog\n\nIntro that mentions `## Unreleased`.\n\n"
OLD = "## 0.5.0 - 2026-11-12\n\n### Fixed\n\n- An old fix.\n"


def changelog(unreleased: str) -> str:
    return HEAD + "## Unreleased\n\n" + unreleased + "\n" + OLD


BUILT = changelog(
    "### Features\n\n"
    "- Discard changes: tick the files to\n  throw away.\n"
    "- Switch branches.\n\n"
    "### Fixed\n\n"
    "- The Console shows output again.\n"
)


class ReleaseChangelogTests(unittest.TestCase):
    def release(self, main: str, built: str = BUILT) -> str | None:
        return mod.release(main, built, "0.5.1", "2026-11-13")

    def test_unchanged_main_releases_everything(self) -> None:
        self.assertEqual(
            self.release(BUILT),
            HEAD
            + "## Unreleased\n\n"
            + "## 0.5.1 - 2026-11-13\n\n"
            + "### Features\n\n"
            + "- Discard changes: tick the files to\n  throw away.\n"
            + "- Switch branches.\n\n"
            + "### Fixed\n\n"
            + "- The Console shows output again.\n\n"
            + OLD,
        )

    def test_an_entry_added_after_the_build_stays_unreleased(self) -> None:
        main = changelog(
            "### Features\n\n"
            "- Discard changes: tick the files to\n  throw away.\n"
            "- Switch branches.\n"
            "- Technical Debt can fix what it finds,\n  one item or all at once.\n\n"
            "### Fixed\n\n"
            "- The Console shows output again.\n"
        )
        out = self.release(main)
        unreleased, released = out.split("## 0.5.1 - 2026-11-13")
        self.assertIn("## Unreleased\n\n### Features\n\n- Technical Debt can fix what it finds,\n  one item or all at once.\n\n", unreleased)
        self.assertNotIn("Switch branches", unreleased)
        self.assertNotIn("### Fixed", unreleased)
        self.assertNotIn("Technical Debt", released)
        self.assertIn("- Switch branches.\n", released)
        self.assertIn("- The Console shows output again.\n", released)
        self.assertTrue(released.rstrip().endswith("- An old fix."))

    def test_a_group_added_after_the_build_stays_unreleased(self) -> None:
        main = changelog(
            "### Features\n\n"
            "- Discard changes: tick the files to\n  throw away.\n"
            "- Switch branches.\n\n"
            "### Fixed\n\n"
            "- The Console shows output again.\n\n"
            "### Changed\n\n"
            "- Tabs are back to medium weight.\n"
        )
        unreleased, released = self.release(main).split("## 0.5.1 - 2026-11-13")
        self.assertEqual(
            unreleased,
            HEAD + "## Unreleased\n\n### Changed\n\n- Tabs are back to medium weight.\n\n",
        )
        self.assertNotIn("### Changed", released)

    def test_rewrapped_entries_still_match(self) -> None:
        main = changelog(
            "### Features\n\n"
            "- Discard changes: tick the\n  files to throw away.\n"
            "- Switch branches.\n\n"
            "### Fixed\n\n"
            "- The Console shows output again.\n"
        )
        unreleased, _ = self.release(main).split("## 0.5.1 - 2026-11-13")
        self.assertEqual(unreleased, HEAD + "## Unreleased\n\n")

    def test_the_same_text_in_another_group_stays_unreleased(self) -> None:
        main = changelog(
            "### Features\n\n"
            "- Discard changes: tick the files to\n  throw away.\n"
            "- Switch branches.\n\n"
            "### Fixed\n\n"
            "- The Console shows output again.\n"
            "- Switch branches.\n"
        )
        unreleased, _ = self.release(main).split("## 0.5.1 - 2026-11-13")
        self.assertEqual(unreleased, HEAD + "## Unreleased\n\n### Fixed\n\n- Switch branches.\n\n")

    def test_an_entry_main_reworded_extended_or_moved_is_not_released_again(self) -> None:
        for main in (
            changelog(
                "### Features\n\n"
                "- Discard changes: tick the files you want to\n  throw away.\n"
                "- Switch branches.\n\n"
                "### Fixed\n\n"
                "- The Console shows output again.\n"
            ),
            changelog(
                "### Features\n\n"
                "- Discard changes: tick the files to\n  throw away, or discard everything since the last commit.\n"
                "- Switch branches.\n\n"
                "### Fixed\n\n"
                "- The Console shows output again.\n"
            ),
            changelog(
                "### Features\n\n"
                "- Switch branches.\n\n"
                "### Fixed\n\n"
                "- The Console shows output again.\n\n"
                "### Changed\n\n"
                "- Discard changes: tick the files to\n  throw away.\n"
            ),
        ):
            unreleased, released = self.release(main).split("## 0.5.1 - 2026-11-13")
            self.assertEqual(unreleased, HEAD + "## Unreleased\n\n")
            self.assertIn("- Discard changes: tick the files to\n  throw away.\n", released)
            self.assertEqual(len(mod.edited_since(main, BUILT)), 1)

    def test_a_new_entry_unlike_any_shipped_one_stays_unreleased(self) -> None:
        main = changelog(
            "### Features\n\n"
            "- Switch branches.\n"
            "- Technical Debt can fix what it finds.\n\n"
            "### Fixed\n\n"
            "- The Console shows output again.\n"
        )
        unreleased, _ = self.release(main).split("## 0.5.1 - 2026-11-13")
        self.assertIn("- Technical Debt can fix what it finds.\n", unreleased)
        self.assertEqual(mod.edited_since(main, BUILT), [])

    def test_an_entry_with_a_second_paragraph_moves_whole(self) -> None:
        built = changelog("### Features\n\n- Big feature.\n\n  Its second paragraph.\n")
        main = changelog("### Features\n\n- Big feature.\n\n  Its second paragraph.\n- New one.\n")
        unreleased, released = self.release(main, built).split("## 0.5.1 - 2026-11-13")
        self.assertEqual(unreleased, HEAD + "## Unreleased\n\n### Features\n\n- New one.\n\n")
        self.assertIn("- Big feature.\n\n  Its second paragraph.\n", released)

    def test_the_command_warns_about_an_edited_entry(self) -> None:
        main = changelog("### Features\n\n- Discard changes: tick the files you want to\n  throw away.\n- Switch branches.\n\n### Fixed\n\n- The Console shows output again.\n")
        with tempfile.TemporaryDirectory() as tmp:
            built_path = os.path.join(tmp, "built.md")
            main_path = os.path.join(tmp, "CHANGELOG.md")
            with open(built_path, "w", encoding="utf-8") as f:
                f.write(BUILT)
            with open(main_path, "w", encoding="utf-8") as f:
                f.write(main)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                mod.main(["--version", "0.5.1", "--built", built_path, "--changelog", main_path, "--date", "2026-11-13"])
            self.assertIn("::warning title=Changelog entry edited after the build::", out.getvalue())

    def test_an_entry_removed_from_main_after_the_build_still_ships(self) -> None:
        main = changelog("### Features\n\n- Switch branches.\n")
        _, released = self.release(main).split("## 0.5.1 - 2026-11-13")
        self.assertIn("- Discard changes: tick the files to\n  throw away.\n", released)
        self.assertIn("- The Console shows output again.\n", released)

    def test_nothing_to_do(self) -> None:
        listed = HEAD + "## Unreleased\n\n## 0.5.1 - 2026-11-13\n\n### Fixed\n\n- A fix.\n\n" + OLD
        self.assertIsNone(self.release(listed))
        self.assertIsNone(self.release(BUILT, changelog("")))
        self.assertIsNone(self.release(HEAD + OLD))

    def test_the_command_edits_the_changelog_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            built = os.path.join(tmp, "built.md")
            main = os.path.join(tmp, "CHANGELOG.md")
            with open(built, "w", encoding="utf-8") as f:
                f.write(BUILT)
            with open(main, "w", encoding="utf-8") as f:
                f.write(BUILT)
            self.assertEqual(
                mod.main(["--version", "0.5.1", "--built", built, "--changelog", main, "--date", "2026-11-13"]),
                0,
            )
            with open(main, encoding="utf-8") as f:
                self.assertIn("## Unreleased\n\n## 0.5.1 - 2026-11-13\n\n### Features", f.read())


if __name__ == "__main__":
    unittest.main()
