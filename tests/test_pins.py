import importlib.util
import sys
import unittest
from pathlib import Path

import data
from kot import config
from kot.render import url_for

_spec = importlib.util.spec_from_file_location("make_pins", Path(__file__).resolve().parent.parent / "scripts" / "make_pins.py")
make_pins = importlib.util.module_from_spec(_spec)
sys.modules["make_pins"] = make_pins  # dataclasses look their module up here
_spec.loader.exec_module(make_pins)


class PinTests(unittest.TestCase):
    def test_pin_link_has_utm_tags(self):
        self.assertEqual(make_pins.pin_link("food/eggs/"),
                         f"{config.BASE_URL}food/eggs/?utm_source=pinterest&utm_medium=social&utm_campaign=launch")

    def test_every_pin_points_to_a_real_page_not_the_homepage(self):
        pages = ({url_for("food", f.slug) for f in data.ALL_FOODS}
                 | {url_for("leftout", lo.slug) for lo in data.ALL_LEFTOUT}
                 | {url_for("guide", g.slug) for g in data.ALL_GUIDES})
        for p in make_pins.PINS:
            self.assertNotEqual(p.path, "", p.slug)
            self.assertIn(p.path, pages, p.slug)

    def test_page_art_is_transparent_and_calm(self):
        for slug in make_pins.PAGE_ART:
            svg = make_pins.page_svg(slug)
            self.assertTrue(svg.startswith("<svg"))
            self.assertIn('class="page-art"', svg)
            self.assertIn("prefers-reduced-motion: no-preference", svg)
            self.assertNotIn("<rect width=\"1000\"", svg)   # no full background block
            self.assertIn("stk", svg)                          # stickers

    def test_every_pin_has_art_and_copy(self):
        for p in make_pins.PINS:
            self.assertIn(p.slug, make_pins.ARTS)
            title, desc = make_pins.COPY[p.slug]
            self.assertLessEqual(len(title), 100)
            self.assertLessEqual(len(desc), 500)


if __name__ == "__main__":
    unittest.main()
