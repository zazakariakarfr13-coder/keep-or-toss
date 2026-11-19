from data.sources import FDA_BAD_BUG_BOOK, FOODKEEPER, FSIS_LEFTOVERS
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="cooked-rice",
        name="Cooked rice",
        category="leftovers",
        question="How long does cooked rice last?",
        description="Cooked rice lasts 3 to 4 days in the fridge and 3 to 4 months in the freezer. "
                    "Here is how to tell if it has gone bad.",
        storage={
            "fridge": Span(3, 4, "days", "Keep your fridge at {temp:40} or colder."),
            "freezer": Span(3, 4, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Rice can carry tiny spores that live through cooking. If the rice sits warm, they can make a "
            "poison that reheating will not kill. So cool it fast and do not keep it too long.",
        spoiled_signs=[
            "It smells sour or odd.",
            "It feels slimy or sticky in a new way.",
            "You see mold: fuzzy spots of green, black, white or pink.",
            "It has been in the fridge for more than 4 days, even if it looks fine. "
            "The germs that matter most do not change how rice looks or smells.",
        ],
        how_to_store=[
            "Get it into the fridge within 2 hours of cooking.",
            "Spread hot rice on a tray or in a wide, shallow box so it cools fast. A deep pot stays warm in the middle for hours.",
            "Use a box with a tight lid, and write the date on it.",
            "Reheat it until it is steaming hot all the way through, to {temp:165}.",
        ],
        common_mistake="Leaving the pot of rice on the stove to cool down overnight. It feels safe because the rice "
                       "was cooked, but the spores wake up as it cools slowly. Reheating the next day will not fix it, "
                       "so rice left out all night should go in the trash.",
        freezing="Rice freezes well. Pack it flat in freezer bags, press out the air, and add the date. Use it within "
                 "3 to 4 months for the best taste. It stays safe longer if it stays frozen, but it gets dry. "
                 "Thaw it in the fridge or heat it straight from frozen with a splash of water. "
                 "The USDA FoodKeeper app lists up to 6 days in the fridge for cooked rice. We use the 3 to 4 day "
                 "rule for all leftovers from the USDA, because it is the safer of the two.",
        sources=[FSIS_LEFTOVERS, FOODKEEPER, FDA_BAD_BUG_BOOK],
        related=[],
    ),
]
