from data.sources import FOODKEEPER
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="butter",
        name="Butter",
        category="dairy",
        question="How long does butter last?",
        description="Butter lasts 1 to 2 months in the fridge, 6 to 9 months in the freezer, "
                    "and 1 to 2 days on the counter. Here is how to keep it fresh.",
        storage={
            "fridge": Span(1, 2, "months", "Counted from the day you bought it."),
            "freezer": Span(6, 9, "months"),
            "counter": Span(1, 2, "days", "In a covered dish, away from the stove and the sun."),
        },
        why="Butter is mostly fat with very little water, so germs grow slowly in it. "
            "The real problem is that the fat slowly goes rancid and picks up fridge smells.",
        spoiled_signs=[
            "It smells sour, cheesy or like old paint. That is rancid fat.",
            "The outside is darker yellow than the inside. You can scrape off a thin dark layer.",
            "You see mold. Throw the whole stick out.",
            "It tastes bitter or soapy, even when it smells fine.",
        ],
        how_to_store=[
            "Keep it wrapped in its paper or foil, or in a closed butter dish.",
            "Keep it away from onions, fish and other strong smells. Butter soaks them up.",
            "Leave out only what you will use in a day or two. Keep the rest in the fridge.",
            "Salted butter lasts a bit longer on the counter than unsalted, because salt slows spoiling.",
        ],
        common_mistake="Keeping a soft butter dish next to the stove or in a sunny window. Heat makes butter "
                       "melt and go rancid in hours, not days. A cool, dark spot on the counter is fine. A warm "
                       "kitchen in summer is not, so use the fridge when the room gets hot.",
        freezing="Butter freezes very well. Keep it in its wrapper and add a freezer bag or foil on top. "
                 "It keeps its best taste for 6 to 9 months. Thaw it in the fridge overnight, or grate "
                 "frozen butter straight into pastry and biscuit dough.",
        sources=[FOODKEEPER],
        related=[],
    ),
]
