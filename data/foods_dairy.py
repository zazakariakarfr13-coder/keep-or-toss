from data.sources import FOODKEEPER, FSIS_MOLDS
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
    Food(
        slug="yogurt",
        name="Yogurt",
        category="dairy",
        question="How long does yogurt last?",
        description="Yogurt lasts 1 to 2 weeks in the fridge and 1 to 2 months in the freezer. "
                    "Moldy yogurt goes in the trash. Here is how to tell if it has gone bad.",
        storage={
            "fridge": Span(1, 2, "weeks"),
            "freezer": Span(1, 2, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Yogurt is full of good live cultures, and its sour taste comes from acid. That keeps it fresh for a "
            "while, but molds and yeasts can still grow, and they spread below the surface.",
        spoiled_signs=[
            "Any mold, even one small spot. Throw out the whole tub. Do not scoop it off.",
            "It smells yeasty or like old cheese instead of clean and tangy.",
            "The lid bulges, or the yogurt fizzes.",
            "A little clear liquid on top is normal. That is whey, and you can stir it back in.",
        ],
        how_to_store=[
            "Keep it on a fridge shelf, not in the door, where the temperature jumps around.",
            "Use a clean spoon every time. A licked spoon brings mouth germs into the tub.",
            "Put the lid back on right away so it does not soak up fridge smells.",
            "Take yogurt cups to work or school in a lunch box with an ice pack.",
        ],
        common_mistake="Scraping a moldy spot off the top and eating the rest. Yogurt is soft and wet, so the mold's "
                       "roots and the germs that grow with it spread down into the tub where you cannot see them. "
                       "The USDA says moldy yogurt should be thrown out.",
        freezing="Yogurt freezes for 1 to 2 months. The live cultures survive, but the texture turns grainy when it "
                 "thaws, so frozen yogurt works best in smoothies, baking and sauces. For a snack, freeze spoonfuls "
                 "on a tray to make little yogurt drops.",
        sources=[FOODKEEPER, FSIS_MOLDS],
        related=["cheddar-cheese", "butter"],
    ),
    Food(
        slug="cheddar-cheese",
        name="Cheddar cheese",
        category="dairy",
        question="How long does cheddar cheese last?",
        description="An opened block of cheddar lasts 3 to 4 weeks in the fridge, and an unopened block about "
                    "6 months. A small mold spot on hard cheese can be cut off.",
        storage={
            "fridge": Span(3, 4, "weeks", "Opened block. Unopened: about 6 months."),
            "freezer": Span(6, 6, "months"),
            "counter": Span(0, 2, "hours", "Cheese boards and lunch boxes: 2 hours, then back in the fridge."),
        },
        why="Hard cheese like cheddar has little water and a lot of salt, so germs grow very slowly in it. "
            "That is why it lasts weeks after opening, while soft cheese lasts days.",
        spoiled_signs=[
            "Fuzzy mold spots. On a hard block, cut them off (see below). On shredded or sliced cheddar, throw it out.",
            "A sour, ammonia or rotten smell, stronger than its normal sharp smell.",
            "A slimy surface.",
            "White crystals that crunch are fine. They form as cheddar ages.",
        ],
        how_to_store=[
            "Wrap the cut side in wax paper or baking paper, then put it in a loose bag or box.",
            "Keep it in the cheese or vegetable drawer, where it stays cold and moist.",
            "Change the wrap after each use. Old plastic wrap traps wet spots where mold starts.",
            "Shredded and sliced cheddar spoil faster than a block, so use them first.",
        ],
        common_mistake="Throwing out a whole block for one small spot of mold. The USDA says hard cheese can be saved: "
                       "cut off at least 1 inch around and below the spot, and keep the knife out of the mold. Then "
                       "wrap the rest in fresh paper. This only works for hard cheese, not soft cheese.",
        freezing="Cheddar freezes for about 6 months, but it turns crumbly. Grate it first, freeze it flat in a bag, "
                 "and use it straight from the freezer in cooking: pasta bakes, omelets, soups and toasties. "
                 "Do not count on it for neat slices on a cheese board.",
        sources=[FOODKEEPER, FSIS_MOLDS],
        related=["yogurt", "butter"],
    ),
]
