from data.sources import FOODKEEPER, FSIS_LEFTOVERS, FSIS_MOLDS
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="ketchup",
        name="Ketchup",
        category="condiments",
        question="How long does ketchup last?",
        description="Opened ketchup lasts 6 months in the fridge, and store-bought ketchup is safe in the cupboard too. "
                    "An unopened bottle lasts about a year.",
        storage={
            "fridge": Span(6, 6, "months", "After opening. This is for best taste."),
            "pantry": Span(1, 1, "years", "Unopened bottle."),
        },
        why="Store-bought ketchup is full of vinegar, sugar and salt, so germs struggle to grow in it. "
            "The label says to refrigerate after opening to keep its flavor and color, not for safety.",
        spoiled_signs=[
            "Mold on the cap or inside the neck of the bottle. Throw the bottle out.",
            "It smells sour or yeasty, or it fizzes when you open it.",
            "A watery layer on top is normal. Just shake it back together.",
            "Dark brown color and a dull taste mean old ketchup. It is safe but not nice.",
        ],
        how_to_store=[
            "Keep opened ketchup in the fridge if you use it slowly. It stays bright and fresh for 6 months.",
            "A diner-style bottle on the table is fine if you finish it within a few weeks.",
            "Wipe the cap and spout now and then. Dried ketchup there is where mold starts.",
            "Homemade ketchup has no preservatives, so always keep it in the fridge and make small batches.",
        ],
        common_mistake="Topping up a half-empty bottle with a new one. The old ketchup at the bottom never gets used, "
                       "and the mix spoils sooner than either bottle would on its own. Finish one bottle before you "
                       "open the next.",
        freezing="You can freeze ketchup, but it rarely makes sense. If you made a big batch at home, freeze it in an "
                 "ice cube tray, then move the cubes to a bag. Use them in sauces and stews within a few months. "
                 "The texture gets thinner after thawing.",
        sources=[FOODKEEPER, FSIS_MOLDS],
        related=["mayonnaise"],
    ),
    Food(
        slug="mayonnaise",
        name="Mayonnaise",
        category="condiments",
        question="How long does mayonnaise last?",
        description="Opened mayonnaise lasts 2 months in the fridge. Keep foods made with mayo, like potato salad, "
                    "out of the fridge for 2 hours at most.",
        storage={
            "fridge": Span(2, 2, "months", "After opening."),
            "freezer": None,
            "pantry": Span(3, 6, "months", "Unopened jar only."),
        },
        why="Jarred mayo is made with pasteurized eggs and acid, which keeps it stable. "
            "The risk comes from what you mix it with: chicken, eggs, pasta and potatoes spoil fast.",
        spoiled_signs=[
            "It smells sour, like old vinegar, or just smells wrong.",
            "The color turns yellow-brown or gray.",
            "Oil has separated into a layer and will not stir back in.",
            "You see any mold. Throw out the whole jar, not just the top.",
        ],
        how_to_store=[
            "Put the jar back in the fridge right after you use it.",
            "Use a clean knife or spoon every time. Crumbs and bits of food bring germs into the jar.",
            "Keep the lid on tight, and write the opening date on it.",
            "Squeeze bottles follow the same rules as jars: into the fridge once opened, and use within 2 months.",
            "Homemade mayo is made with raw egg. Keep it cold, make small batches, and treat it like fresh egg.",
        ],
        common_mistake="Blaming the mayo when potato salad or chicken salad makes people sick. The usual cause is the "
                       "salad sitting out at a picnic. Salads made with mayo last 3 to 4 days in the fridge, and only "
                       "2 hours out of it, or 1 hour when it is above {temp:90}.",
        freezing="Do not freeze mayonnaise. The oil and egg separate when it thaws, and it turns grainy and oily. "
                 "Salads made with mayo do not freeze well either. Make only as much as you can eat in 3 to 4 days.",
        sources=[FOODKEEPER, FSIS_LEFTOVERS, FSIS_MOLDS],
        related=["ketchup", "cooked-pasta"],
    ),
]
