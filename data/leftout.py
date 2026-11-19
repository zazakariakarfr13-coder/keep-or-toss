from data.sources import FDA_BAD_BUG_BOOK, FSIS_LEFTOVERS
from kot.schema import LeftOut

LEFTOUT = [
    LeftOut(
        slug="rice-left-out-overnight",
        food="cooked-rice",
        question="Rice left out overnight: is it safe to eat?",
        verdict="toss",
        verdict_line="Throw it out. Cooked rice that sat out all night is not safe, even if you reheat it.",
        risk="Raw rice often carries spores of a germ called Bacillus cereus. Cooking does not kill the spores. "
             "As the rice cools slowly on the stove or the table, they wake up, grow, and make a toxin. "
             "That toxin can survive boiling, so heating the rice again will not make it safe. "
             "It can cause vomiting within a few hours. The rice usually looks and smells normal, "
             "so you cannot tell by checking it.",
        next_time=[
            "Spread leftover rice on a tray or in a wide box so it cools in minutes.",
            "Get it into the fridge within 2 hours of cooking, or 1 hour on a hot day.",
            "Make only as much rice as you will eat, or plan to freeze the extra right away.",
            "Leaving rice in a rice cooker on keep-warm is fine. Turning it off and leaving it to cool overnight is not.",
        ],
        sources=[FSIS_LEFTOVERS, FDA_BAD_BUG_BOOK],
        related=["cooked-rice", "pizza-left-out-overnight"],
        description="Cooked rice left out overnight should be thrown out, even if you reheat it. "
                    "Here is why rice is riskier than most leftovers.",
    ),
    LeftOut(
        slug="pizza-left-out-overnight",
        food="pizza",
        question="Pizza left out overnight: is it safe to eat?",
        verdict="toss",
        verdict_line="Throw it out. Pizza that sat out more than 2 hours is not safe, even if it looks fine.",
        risk="Pizza is covered in foods that spoil: cheese, meat and tomato sauce. Between {temp:40} and {temp:140}, "
             "germs on these toppings can double in number about every 20 minutes. "
             "After a night on the counter, there can be enough of them to make you sick, "
             "and some make toxins that heat does not destroy. A closed box does not help. "
             "It keeps the pizza at room temperature just as well as an open one.",
        next_time=[
            "Put leftover slices in the fridge within 2 hours of delivery.",
            "At a party, keep pizza out for 2 hours at most, then put the rest away.",
            "Take the slices out of the box first so they cool faster and take less space.",
        ],
        sources=[FSIS_LEFTOVERS],
        related=["pizza", "rice-left-out-overnight"],
        description="Pizza left out overnight should be thrown out. Cheese, meat and sauce are not safe after "
                    "more than 2 hours at room temperature.",
    ),
    LeftOut(
        slug="cooked-chicken-left-out-overnight",
        food="cooked-chicken",
        question="Cooked chicken left out overnight: is it safe to eat?",
        verdict="toss",
        verdict_line="Throw it out. Cooked chicken that sat out more than 2 hours should not be eaten, even if you reheat it.",
        risk="Cooking kills the germs that were on the raw chicken. But new germs land on it as soon as it cools, "
             "from the air, the plate and your hands. At room temperature they grow fast. "
             "Some, like Staphylococcus, leave behind toxins that reheating cannot remove. "
             "Chicken can smell fine and still make you sick, so the time out of the fridge is what matters.",
        next_time=[
            "Put cooked chicken in the fridge within 2 hours, or within 1 hour if the room is above {temp:90}.",
            "Slice or pull the meat off a whole bird so it cools faster.",
            "A covered pot is not a fridge. Covering the chicken does not slow germs down.",
        ],
        sources=[FSIS_LEFTOVERS],
        related=["cooked-chicken", "rice-left-out-overnight"],
        description="Cooked chicken left out overnight should be thrown out, even if you reheat it. "
                    "Here is what happens to chicken at room temperature.",
    ),
]
