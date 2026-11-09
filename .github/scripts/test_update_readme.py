"""Run with `python3 -m unittest discover -s .github/scripts`."""
import importlib.util
import os
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("update_readme", os.path.join(os.path.dirname(__file__), "update-readme.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ASSETS = ["Phun_0.2.0_amd64.deb", "Phun_0.2.0_x86_64.pkg.tar.zst", "Phun_0.2.0_intel.dmg", "Phun_0.2.0_apple-silicon.dmg", "Phun_0.2.0_windows-x64-setup.exe"]
README = "# Phun\n\nIntro.\n\n<!-- latest-release:start -->\nold\n<!-- latest-release:end -->\n\nMore.\n"


class UpdateReadme(unittest.TestCase):
    def test_plain_versions_only(self):
        self.assertEqual(mod.plain_version("v0.2.0"), "0.2.0")
        self.assertEqual(mod.plain_version("1.10.3"), "1.10.3")
        self.assertIsNone(mod.plain_version("v0.2.0-rc.1"))
        self.assertIsNone(mod.plain_version("latest"))

    def test_block_has_a_header_and_direct_links_per_platform_in_order(self):
        out = mod.rewrite(README, "v0.2.0", "cloudcake/phun", ASSETS)
        self.assertIn("Latest release: **[v0.2.0](https://github.com/cloudcake/phun/releases/tag/v0.2.0)**", out)
        headers = [line for line in out.splitlines() if "<img " in line]
        self.assertEqual(len(headers), 3)
        for header, stem in zip(headers, ("macos", "windows", "linux")):
            self.assertIn(f'src=".github/readme/download/{stem}.svg?v=0.2.0"', header)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/tag/v0.2.0"><img src=".github/readme/download/macos.svg', out)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/tag/v0.2.0"><img src=".github/readme/download/linux.svg', out)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_amd64.deb"><strong>Download the .deb</strong></a>', out)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_x86_64.pkg.tar.zst"><strong>Arch package</strong></a>', out)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_apple-silicon.dmg"><strong>Apple Silicon</strong></a>', out)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_intel.dmg"><strong>Intel</strong></a>', out)
        self.assertIn("Phun_0.2.0_windows-x64-setup.exe", out)
        self.assertLess(out.index("macos.svg"), out.index("windows.svg"))
        self.assertLess(out.index("windows.svg"), out.index("linux.svg"))
        self.assertTrue(out.startswith("# Phun\n\nIntro.\n\n<!-- latest-release:start -->"))
        self.assertTrue(out.endswith("<!-- latest-release:end -->\n\nMore.\n"))
        self.assertNotIn("old", out)

    def test_leaves_out_a_platform_without_an_installer(self):
        out = mod.rewrite(README, "v0.2.0", "cloudcake/phun", ["Phun_0.2.0_amd64.deb"])
        self.assertNotIn("macos.svg", out)
        self.assertNotIn("windows.svg", out)
        self.assertIn("linux.svg?v=0.2.0", out)
        self.assertIn('<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_amd64.deb"><img src=".github/readme/download/linux.svg', out)
        self.assertNotIn("Arch package", out)

    def test_no_markers_means_no_rewrite(self):
        self.assertIsNone(mod.rewrite("# Phun\n", "v0.2.0", "cloudcake/phun", ASSETS))

    def test_cli_skips_pre_releases_and_rewrites_releases(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "README.md")
            with open(path, "w") as fh:
                fh.write(README)
            args = ["--repo", "cloudcake/phun", "--readme", path] + [a for name in ASSETS for a in ("--asset", name)]
            self.assertEqual(mod.main(["--tag", "v0.3.0-rc.1"] + args), 0)
            with open(path) as fh:
                self.assertEqual(fh.read(), README)
            self.assertEqual(mod.main(["--tag", "v0.2.0"] + args), 0)
            with open(path) as fh:
                self.assertIn("Phun_0.2.0_intel.dmg", fh.read())


if __name__ == "__main__":
    unittest.main()
