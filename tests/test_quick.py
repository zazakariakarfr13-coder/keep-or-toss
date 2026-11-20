import unittest

import data
from data.quick import parse_line, slugify
from kot.schema import Span, validate_all


class QuickParseTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Half-and-half (cream)"), "half-and-half-cream")
        self.assertEqual(slugify("Brie & goat cheese"), "brie-goat-cheese")

    def test_parse_full_line(self):
        q = parse_line("Ketchup|condiments|o:6m||1y||Safe in the cupboard after opening; the fridge keeps the taste.")
        self.assertEqual(q.slug, "ketchup")
        self.assertEqual(q.category, "condiments")
        self.assertEqual(q.storage["fridge"].unit, "months")
        self.assertEqual((q.storage["fridge"].min, q.storage["fridge"].max), (6, 6))
        self.assertIn("After opening.", q.storage["fridge"].note)
        self.assertIn("Safe in the cupboard", q.storage["fridge"].note)
        self.assertEqual(q.storage["pantry"].unit, "years")
        self.assertNotIn("freezer", q.storage)
        self.assertIn("USDA FoodKeeper", q.source)

    def test_no_means_not_recommended(self):
        q = parse_line("Cucumbers|produce|4-6d|no|||")
        self.assertIsNone(q.storage["freezer"])
        self.assertEqual(q.storage["fridge"], Span(4, 6, "days"))

    def test_counter_hours(self):
        q = parse_line("Pumpkin pie|bakery|o:3-4d|1-2m||2h|")
        self.assertEqual(q.storage["counter"], Span(2, 2, "hours"))

    def test_bad_unit_fails(self):
        with self.assertRaises(ValueError):
            parse_line("X|pantry|3-4q||||")


class QuickDataTests(unittest.TestCase):
    def test_about_300_foods(self):
        self.assertGreaterEqual(len(data.ALL_QUICK), 300)

    def test_all_data_validates_together(self):
        validate_all(data.ALL_FOODS, data.ALL_LEFTOUT, data.ALL_GUIDES, data.ALL_QUICK)

    def test_popular_examples_exist(self):
        from kot import config
        slugs = {f.slug for f in data.ALL_FOODS} | {q.slug for q in data.ALL_QUICK}
        self.assertTrue(set(config.POPULAR) <= slugs, set(config.POPULAR) - slugs)

    def test_no_quick_food_shadows_a_page(self):
        pages = {f.slug for f in data.ALL_FOODS}
        self.assertFalse(pages & {q.slug for q in data.ALL_QUICK})


if __name__ == "__main__":
    unittest.main()
