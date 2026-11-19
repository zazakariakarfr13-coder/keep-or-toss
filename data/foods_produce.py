from data.sources import FOODKEEPER
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="avocado",
        name="Avocado",
        category="produce",
        question="How long do avocados last?",
        description="A ripe avocado lasts 3 to 4 days in the fridge. Hard avocados ripen on the counter first. "
                    "Here is how to store them, whole or cut.",
        storage={
            "fridge": Span(3, 4, "days", "For a ripe, whole avocado. Ripen hard ones on the counter first."),
            "freezer": None,
        },
        why="Avocados ripen after they are picked. Warmth speeds that up, and the cold of the fridge slows it down. "
            "So use the counter to ripen them and the fridge to hold them once they are ready.",
        spoiled_signs=[
            "The skin has deep dents, or the fruit feels mushy all over.",
            "The flesh is brown or black all through, or has dark streaks.",
            "It smells sour or like chemicals.",
            "You see mold on the skin or inside. Throw it out.",
            "A little brown on a cut surface is just air. Scrape it off and eat the green part.",
        ],
        how_to_store=[
            "To check if it is ripe, press gently near the stem. Ripe fruit gives a little.",
            "Put a hard avocado in a paper bag with a banana or an apple to ripen it faster.",
            "Once it is ripe, move it to the fridge to stop it from going too soft.",
            "For a cut half, keep the pit in, brush the flesh with lemon or lime juice, wrap it tightly and eat it the next day.",
        ],
        common_mistake="Putting hard, unripe avocados in the fridge. The cold stops them from ripening, and many "
                       "never soften well after that. Ripen first on the counter, then chill.",
        freezing="Whole avocados do not freeze well. You can mash the flesh with a little lemon or lime juice "
                 "and freeze it flat in a bag. It turns watery, so use it in smoothies, dips and spreads, "
                 "not in slices on toast.",
        sources=[FOODKEEPER],
        related=[],
    ),
]
