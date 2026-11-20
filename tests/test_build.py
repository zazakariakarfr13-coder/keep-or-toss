import json
import tempfile
import unittest
from pathlib import Path

from kot import config
from kot.build import build
from kot.schema import QuickFood, Span
from tests.test_render import make_guide
from tests.test_schema import make_food, make_leftout

RICE = make_food(storage={"fridge": Span(3, 4, "days", "Don't skip {temp:40}."), "freezer": Span(1, 2, "months"), "counter": None})
EGGS = make_food(slug="eggs", name="Eggs", category="eggs", question="How long do eggs last?",
                 storage={"fridge": Span(3, 5, "weeks")})


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "_site"
        self.quick = [QuickFood("ketchup", "Ketchup", "condiments", {"fridge": Span(6, 6, "months")}, "USDA FoodKeeper")]
        self.paths = build(self.out, [RICE, EGGS], [make_leftout()], [make_guide()], self.quick)

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_writes_pages(self):
        for p in ["", "food/cooked-rice/", "food/eggs/", "left-out/rice-left-out-overnight/",
                  "guides/best-before-vs-use-by/", "category/leftovers/", "category/eggs/",
                  "about/", "sources/", "privacy/"]:
            self.assertTrue((self.out / p / "index.html").is_file(), p)
            self.assertIn(p, self.paths)
        self.assertTrue((self.out / "404.html").is_file())
        self.assertFalse((self.out / "category/dairy").exists(), "unused category hub must not be built")
        self.assertTrue((self.out / "static/site.css").is_file())

    def test_sitemap_lists_every_page_with_base_url(self):
        sm = (self.out / "sitemap.xml").read_text(encoding="utf-8")
        for p in self.paths:
            self.assertIn(f"<loc>{config.BASE_URL}{p}</loc>", sm)
        self.assertNotIn("404", sm)

    def test_checker_json_matches_data(self):
        data = json.loads((self.out / "checker.json").read_text(encoding="utf-8"))
        rice = next(d for d in data if d["slug"] == "cooked-rice")
        self.assertEqual(rice["name"], "Cooked rice")
        self.assertEqual(rice["places"]["fridge"]["maxHours"], 96)
        self.assertEqual(rice["places"]["fridge"]["basis"], "safety")
        self.assertEqual(rice["places"]["freezer"]["basis"], "quality")
        self.assertIsNone(rice["places"]["counter"])
        self.assertNotIn("pantry", rice["places"])
        self.assertEqual(rice["places"]["fridge"]["note"], "Don't skip 40°F (4°C).")

    def test_checker_json_has_quick_foods_without_pages(self):
        data = json.loads((self.out / "checker.json").read_text(encoding="utf-8"))
        k = next(d for d in data if d["slug"] == "ketchup")
        self.assertFalse(k["page"])
        self.assertIn("FoodKeeper", k["source"])
        self.assertTrue(next(d for d in data if d["slug"] == "cooked-rice")["page"])
        self.assertFalse((self.out / "food/ketchup").exists(), "quick foods must not get pages")

    def test_build_fails_on_invalid_data(self):
        with self.assertRaises(ValueError):
            build(Path(self.tmp.name) / "bad", [make_food(related=["nope"])], [], [])


if __name__ == "__main__":
    unittest.main()
