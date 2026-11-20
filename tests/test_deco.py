import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("make_ramadan_deco", ROOT / "scripts" / "make_ramadan_deco.py")
deco = importlib.util.module_from_spec(_spec)
sys.modules["make_ramadan_deco"] = deco
_spec.loader.exec_module(deco)


class RamadanDecoTests(unittest.TestCase):
    def test_decoration_is_hidden_and_calm(self):
        svg = deco.svg()
        self.assertIn('aria-hidden="true"', svg)
        self.assertIn("prefers-reduced-motion: no-preference", svg)
        self.assertNotIn("filter=", svg)  # moving parts must not carry SVG filters (Chromium repaint bug)

    def test_three_lanterns_and_some_lights(self):
        svg = deco.svg()
        self.assertEqual(svg.count('class="sway '), 3)
        self.assertGreaterEqual(svg.count('class="tw '), 8)

    def test_committed_file_matches_generator(self):
        committed = (ROOT / "static" / "art" / "ramadan-meal-prep.svg").read_text(encoding="utf-8")
        self.assertEqual(committed, deco.svg())

    def test_lights_sit_on_the_string(self):
        self.assertAlmostEqual(deco.point(-10)[1], 18, places=0)
        self.assertAlmostEqual(deco.point(400)[1], 26, places=0)


if __name__ == "__main__":
    unittest.main()
