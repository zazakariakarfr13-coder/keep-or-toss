import unittest

from kot.quality import (count_syllables, find_duplicates, kind_of, prose_text,
                         prose_words, reading_grade, similarity)
from tests.test_schema import make_food, make_leftout

TEMPLATE = (
    "{f} keeps well in the fridge when you cool it fast and seal it tight. "
    "Put {f} in a clean box with a lid and push it to the back of the shelf where it stays cold. "
    "If {f} smells sour or looks slimy, throw it out right away and do not taste it to check. "
    "Most people leave {f} on the counter for hours while it cools down after dinner. "
    "That warm time is when germs grow the fastest, so move it to the fridge within two hours. "
    "You can freeze {f} in flat bags so it thaws quickly and evenly later on. "
    "Write the date on the bag with a marker so you know how old it is when you find it. "
    "Thaw {f} in the fridge overnight, not on the counter, and eat it within a day or two. "
    "Heat it until it is steaming hot all the way through before you serve it to anyone. "
    "Never put warm food straight into a full fridge because it warms everything around it. "
    "Split big batches into small boxes so they chill in less time and stay safe for longer. "
    "When you are not sure how old it is, the safe choice is to toss it and cook a fresh batch. "
)

RICE = (
    "Cooked rice can carry tiny spores that live through boiling. When rice sits warm, those spores wake up "
    "and make a toxin that heat cannot destroy. That is why rice needs the fridge sooner than most leftovers. "
    "Spread hot rice on a tray so it cools in minutes, then box it. Reheat only the part you will eat, and only once. "
    "Fried rice made from day-old rice is fine if that rice went into the fridge fast."
)
EGGS = (
    "Raw eggs in the shell last for weeks in the fridge because the shell and its inner skin block most germs. "
    "In the United States eggs are washed before sale, which strips their natural coating, so they must stay cold. "
    "Keep the carton on a middle shelf, not in the door, where the temperature swings every time you open it. "
    "A float test only tells you the egg is old, not that it is safe. Crack it into a bowl and sniff before using."
)


class QualityTests(unittest.TestCase):
    def test_syllables(self):
        self.assertEqual(count_syllables("cat"), 1)
        self.assertEqual(count_syllables("table"), 2)
        self.assertEqual(count_syllables("rice"), 1)
        self.assertEqual(count_syllables("refrigerate"), 4)

    def test_simple_text_low_grade(self):
        self.assertLess(reading_grade("Put it in the fridge. Eat it soon."), 3)

    def test_hard_text_high_grade(self):
        hard = ("Notwithstanding applicable jurisdictional regulatory determinations, manufacturers "
                "must substantiate microbiological stabilization methodologies comprehensively.")
        self.assertGreater(reading_grade(hard), 12)

    def test_empty_text_grade_zero(self):
        self.assertEqual(reading_grade(""), 0.0)

    def test_identical_texts_similarity_1(self):
        self.assertEqual(similarity(RICE, RICE), 1.0)

    def test_one_word_swapped_is_duplicate(self):
        a = make_food(slug="cooked-rice", why=TEMPLATE.format(f="cooked rice"))
        b = make_food(slug="cooked-pasta", why=TEMPLATE.format(f="cooked pasta"))
        pairs = find_duplicates([a, b], 0.30)
        self.assertEqual([(p[0], p[1]) for p in pairs], [("cooked-rice", "cooked-pasta")])

    def test_distinct_texts_pass(self):
        a = make_food(slug="cooked-rice", why=RICE)
        b = make_food(slug="eggs", why=EGGS)
        self.assertEqual(find_duplicates([a, b], 0.30), [])

    def test_prose_text_excludes_name_and_sources(self):
        text = prose_text(make_food(name="Zebra", why="Cool it."))
        self.assertNotIn("Zebra", text)
        self.assertNotIn("FoodKeeper", text)
        self.assertIn("Cool it.", text)

    def test_prose_words_and_kind(self):
        self.assertEqual(prose_words(make_food(why="one two three", spoiled_signs=[], how_to_store=[],
                                               common_mistake="", freezing="")), 3)
        self.assertEqual(kind_of(make_food()), "food")
        self.assertEqual(kind_of(make_leftout()), "leftout")


if __name__ == "__main__":
    unittest.main()
