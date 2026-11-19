from data.sources import FOODKEEPER, FS_COLD_CHART, FSIS_EGGS, FSIS_LEFTOVERS
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="eggs",
        name="Eggs",
        category="eggs",
        question="How long do eggs last?",
        description="Raw eggs in the shell last 3 to 5 weeks in the fridge. Do not freeze them in the shell. "
                    "Here is how to store eggs and check them.",
        storage={
            "fridge": Span(3, 5, "weeks", "Counted from the day you bring them home. Keep them at {temp:40} or colder."),
            "freezer": None,
            "counter": Span(0, 2, "hours", "For eggs that were already cold in the shop."),
        },
        why="Eggs sold in the US are washed, which removes a thin natural coat on the shell. "
            "Without it, germs can get in more easily, so cold eggs must stay cold.",
        spoiled_signs=[
            "Crack it into a bowl first. A bad egg smells strongly of sulfur, like rotten cabbage.",
            "The white is pink, green or has an odd shine. Toss it.",
            "The shell is cracked or slimy. Do not use cracked eggs from the carton.",
            "The float test only tells you an egg is old, because air builds up inside over time. "
            "An old egg can still be safe, and a fresh one can still be bad, so trust your nose.",
        ],
        how_to_store=[
            "Keep them in the carton they came in. It stops them from soaking up smells and drying out.",
            "Put the carton on a middle shelf, not in the door. The door warms up each time you open the fridge.",
            "Do not wash eggs at home. Water can push germs through the shell.",
            "Bought eggs that were not cold in the shop, like some farm eggs? Ask the farmer how they were kept.",
        ],
        common_mistake="Leaving a carton out on the counter after shopping or baking. A cold egg that warms up "
                       "gets wet on the outside, a bit like a cold glass in summer. That water helps germs move "
                       "through the shell. After 2 hours out of the fridge, it is safest to throw them out.",
        freezing="Do not freeze eggs in the shell, because the inside swells and the shell cracks. "
                 "You can crack them, beat the yolks and whites together, and freeze them in a sealed box "
                 "for up to 12 months. Raw whites alone freeze well too. Thaw them in the fridge and cook them fully.",
        sources=[FSIS_EGGS, FS_COLD_CHART, FOODKEEPER, FSIS_LEFTOVERS],
        related=["hard-boiled-eggs"],
    ),
    Food(
        slug="hard-boiled-eggs",
        name="Hard-boiled eggs",
        category="eggs",
        question="How long do hard-boiled eggs last?",
        description="Hard-boiled eggs last 1 week in the fridge, peeled or not. Do not freeze them. "
                    "Here is how to keep them and spot a bad one.",
        storage={
            "fridge": Span(1, 1, "weeks", "Peeled or in the shell."),
            "freezer": None,
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Boiling washes away the egg's thin outer coat. That makes a cooked egg spoil faster "
            "than a raw one, so it needs the fridge soon after it cools.",
        spoiled_signs=[
            "A sharp sulfur smell when you peel it. A faint smell is normal, a strong one is not.",
            "The white feels slimy or chalky.",
            "You see dark or fuzzy spots.",
            "A green or gray ring around the yolk is fine. It comes from cooking too long, not from germs.",
        ],
        how_to_store=[
            "Cool them in cold water, then put them in the fridge within 2 hours.",
            "Unpeeled eggs keep best. The shell protects the egg inside.",
            "Peeled eggs go in a closed box. A damp paper towel on top keeps them from drying out.",
            "Write the day you cooked them on the box or on the shells with a pencil.",
        ],
        common_mistake="Leaving eggs out at Easter or at a picnic for hours, then putting them back in the fridge. "
                       "Time out of the fridge adds up. If eggs were hidden outside or sat out for more than "
                       "2 hours, use them for decoration only and do not eat them.",
        freezing="Do not freeze whole hard-boiled eggs. The whites turn tough and watery. You can freeze just the "
                 "cooked yolks for a few months to sprinkle on salads later. If you have too many eggs, "
                 "make egg salad and eat it within 3 to 4 days instead.",
        sources=[FSIS_EGGS, FS_COLD_CHART, FSIS_LEFTOVERS],
        related=["eggs"],
    ),
]
