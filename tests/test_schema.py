import unittest

from kot.schema import Food, LeftOut, Source, Span, validate_all


def make_food(**over):
    base = dict(
        slug="cooked-rice",
        name="Cooked rice",
        category="leftovers",
        question="How long does cooked rice last?",
        storage={"fridge": Span(3, 4, "days"), "freezer": Span(1, 2, "months")},
        why="Rice can carry spores that survive cooking.",
        spoiled_signs=["It smells sour."],
        how_to_store=["Cool it fast and put it in the fridge."],
        common_mistake="Leaving the pot on the stove overnight.",
        freezing="Freeze flat in bags.",
        sources=[Source("USDA", "FoodKeeper", "https://www.foodsafety.gov/keep-food-safe/foodkeeper-app")],
        related=[],
        description="How long cooked rice lasts in the fridge and freezer.",
    )
    base.update(over)
    return Food(**base)


def make_leftout(**over):
    base = dict(
        slug="rice-left-out-overnight",
        food="cooked-rice",
        question="Rice left out overnight: keep or toss?",
        verdict="toss",
        verdict_line="Toss it.",
        risk="Spores can grow toxins.",
        next_time=["Fridge it within 2 hours."],
        sources=[Source("USDA", "Leftovers", "https://www.fsis.usda.gov/")],
        related=[],
        description="Is rice left out overnight safe?",
    )
    base.update(over)
    return LeftOut(**base)


class SchemaTests(unittest.TestCase):
    def test_valid_food_passes(self):
        validate_all([make_food()], [], [])

    def test_duplicate_slug_fails(self):
        with self.assertRaisesRegex(ValueError, "cooked-rice"):
            validate_all([make_food(), make_food()], [], [])

    def test_duplicate_slug_across_lists_fails(self):
        with self.assertRaisesRegex(ValueError, "cooked-rice"):
            validate_all([make_food()], [make_leftout(slug="cooked-rice")], [])

    def test_unknown_related_slug_fails(self):
        with self.assertRaisesRegex(ValueError, "nope"):
            validate_all([make_food(related=["nope"])], [], [])

    def test_leftout_unknown_food_fails(self):
        with self.assertRaisesRegex(ValueError, "nope"):
            validate_all([make_food()], [make_leftout(food="nope")], [])

    def test_unknown_category_fails(self):
        with self.assertRaisesRegex(ValueError, "snacks"):
            validate_all([make_food(category="snacks")], [], [])

    def test_food_needs_a_source(self):
        with self.assertRaisesRegex(ValueError, "source"):
            validate_all([make_food(sources=[])], [], [])

    def test_bad_slug_fails(self):
        with self.assertRaisesRegex(ValueError, "Cooked Rice"):
            validate_all([make_food(slug="Cooked Rice")], [], [])

    def test_span_min_le_max(self):
        with self.assertRaises(ValueError):
            Span(5, 3, "days")

    def test_place_none_means_not_recommended(self):
        validate_all([make_food(storage={"fridge": Span(1, 2, "days"), "counter": None})], [], [])

    def test_unknown_place_fails(self):
        with self.assertRaisesRegex(ValueError, "garage"):
            validate_all([make_food(storage={"garage": Span(1, 2, "days")})], [], [])

    def test_max_hours(self):
        self.assertEqual(Span(3, 4, "days").max_hours(), 96)
        self.assertEqual(Span(1, 2, "months").max_hours(), 1440)
        self.assertEqual(Span(0, 2, "hours").max_hours(), 2)


if __name__ == "__main__":
    unittest.main()
