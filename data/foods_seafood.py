from data.sources import FOODKEEPER, FS_COLD_CHART, FS_TEMPS, FSIS_LEFTOVERS
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="salmon",
        name="Salmon",
        category="seafood",
        question="How long does raw salmon last?",
        description="Raw salmon lasts 1 to 2 days in the fridge and 2 to 3 months in the freezer. "
                    "Here is how to store fresh salmon and tell if it has gone bad.",
        storage={
            "fridge": Span(1, 2, "days", "Raw. Cooked salmon lasts 3 to 4 days."),
            "freezer": Span(2, 3, "months"),
            "counter": None,
        },
        why="Salmon is an oily fish. Its fat turns stale fast, and germs on raw fish grow even in a cold fridge. "
            "That gives fresh salmon one of the shortest fridge times in your kitchen.",
        spoiled_signs=[
            "A strong, sour or ammonia smell. Fresh salmon smells mild, like clean sea water.",
            "The flesh looks dull or gray instead of bright pink or orange.",
            "It feels slimy, or it stays dented when you press it.",
            "Milky goo on the surface, or dry brown edges.",
        ],
        how_to_store=[
            "Keep it in its pack or a sealed box on the bottom shelf, the coldest part of most fridges.",
            "Put the box in a dish so fish juice cannot drip onto other food.",
            "Cook it or freeze it within 2 days of buying, even if the date on the pack is later.",
            "Cook it to {temp:145}, or until the flesh flakes easily with a fork.",
        ],
        common_mistake="Thawing frozen salmon on the counter or in warm water. The thin edges warm up and start to spoil "
                       "while the thick middle is still frozen. Thaw it in the fridge overnight. In a hurry, seal it in "
                       "a bag and sink it in cold water, changing the water every 30 minutes.",
        freezing="Salmon freezes well for 2 to 3 months. Wrap each fillet tightly, then put it in a freezer bag with "
                 "the air pressed out. Oily fish dries and tastes fishy if it stays frozen much longer, so write "
                 "the date on the bag. Cook it straight from frozen if you like; just add a few minutes.",
        sources=[FS_COLD_CHART, FOODKEEPER, FS_TEMPS],
        related=["cooked-shrimp"],
    ),
    Food(
        slug="cooked-shrimp",
        name="Cooked shrimp",
        category="seafood",
        question="How long does cooked shrimp last?",
        description="Cooked shrimp lasts 3 to 4 days in the fridge and 1 to 3 months in the freezer. "
                    "Raw shrimp keeps only 1 to 3 days. Here is how to keep shrimp safe.",
        storage={
            "fridge": Span(3, 4, "days", "Cooked. Raw shrimp: 1 to 3 days."),
            "freezer": Span(1, 3, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Shellfish spoils quickly once it warms up, and a shrimp ring at a party sits out for hours. "
            "Cooked shrimp is safe for a few days in the fridge, but only if it stays cold.",
        spoiled_signs=[
            "A sour, fishy or ammonia smell. Good cooked shrimp smells almost like nothing.",
            "A slimy coat that stays when you rinse it.",
            "Gray or yellow patches on the pink and white flesh.",
            "A mushy bite. Fresh cooked shrimp feels firm and springy.",
        ],
        how_to_store=[
            "Put leftover shrimp in a shallow sealed box and get it into the fridge within 2 hours.",
            "At a party, set the shrimp tray on a bowl of ice and swap it out after 2 hours.",
            "Store raw and cooked shrimp in separate boxes so raw juice never touches cooked shrimp.",
            "When you cook raw shrimp, cook it until it turns pearly and opaque all the way through.",
        ],
        common_mistake="Buying a frozen cooked shrimp ring, thawing it on the counter, and then leaving it out for the "
                       "whole party. Thaw it in the fridge the day before. Bring out half, keep the rest cold, and "
                       "refill the platter instead of leaving one big tray out.",
        freezing="Cooked shrimp freezes for 1 to 3 months. Peel it, dry it with a paper towel, and freeze it flat in a "
                 "bag so the pieces do not stick together. It gets a little rubbery when thawed, so it works best in "
                 "hot dishes like pasta, fried rice and soup.",
        sources=[FOODKEEPER, FS_COLD_CHART, FS_TEMPS, FSIS_LEFTOVERS],
        related=["salmon", "cooked-pasta"],
    ),
]
