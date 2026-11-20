from data.sources import FOODKEEPER, FSIS_MOLDS
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
    Food(
        slug="strawberries",
        name="Strawberries",
        category="produce",
        question="How long do strawberries last?",
        description="Fresh strawberries last 2 to 3 days in the fridge and 8 to 12 months in the freezer. "
                    "Moldy berries go in the trash. Here is how to make them last.",
        storage={
            "fridge": Span(2, 3, "days"),
            "freezer": Span(8, 12, "months"),
        },
        why="Strawberries are soft and full of water, and they do not ripen any more once picked. "
            "One moldy berry can spread mold to its neighbors in a day.",
        spoiled_signs=[
            "White, gray or green fuzz. Throw out that berry and any berries that were touching it.",
            "Soft, wet or brown spots, or berries leaking juice.",
            "A sour or wine-like smell.",
            "Dull, shriveled berries are old but not unsafe. Use them in smoothies or jam.",
        ],
        how_to_store=[
            "Sort them as soon as you get home. Pick out any moldy or crushed berries.",
            "Do not wash them until you are about to eat them. Water speeds up mold.",
            "Keep them dry in a box lined with a paper towel, with the lid a little open.",
            "Rinse them under running water right before eating, then pat them dry.",
        ],
        common_mistake="Washing the whole box as soon as you get home. The berries stay damp in the fridge, and mold "
                       "loves damp fruit. Wash only what you will eat now. The USDA also says soft fruit with mold "
                       "should not be cut and saved, because the mold spreads below the surface.",
        freezing="Strawberries freeze for 8 to 12 months. Wash them, dry them well, pull off the green tops, and freeze "
                 "them in one layer on a tray. Once they are hard, pour them into a bag. They will be soft when "
                 "thawed, so use them for smoothies, sauces, baking and jam.",
        sources=[FOODKEEPER, FSIS_MOLDS],
        related=["avocado"],
    ),
]
