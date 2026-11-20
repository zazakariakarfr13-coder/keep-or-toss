from data.sources import FDA_BAD_BUG_BOOK, FOODKEEPER, FS_COLD_CHART, FSIS_LEFTOVERS, FSIS_MOLDS
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
        related=["cooked-chicken", "pizza"],
    ),
    Food(
        slug="cooked-chicken",
        name="Cooked chicken",
        category="leftovers",
        question="How long does cooked chicken last?",
        description="Cooked chicken lasts 3 to 4 days in the fridge and 3 to 4 months in the freezer. "
                    "Here is how to store leftovers and rotisserie chicken safely.",
        storage={
            "fridge": Span(3, 4, "days", "Leftovers, rotisserie chicken and chicken dishes."),
            "freezer": Span(3, 4, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Cooking kills most germs, but new ones land on the chicken as soon as it cools. "
            "Some of them grow even in the fridge, so the clock starts the day you cook it.",
        spoiled_signs=[
            "It smells sour, like eggs, or just wrong.",
            "The surface feels slimy or sticky.",
            "It has gray or green patches, or any mold.",
            "It has been in the fridge for more than 4 days. Many germs that cause food poisoning give no smell at all.",
        ],
        how_to_store=[
            "Get it into the fridge within 2 hours of cooking or buying it hot.",
            "Pull the meat off a whole bird and store it in shallow boxes. It cools faster that way.",
            "Write the date on the box.",
            "Reheat it until it is steaming hot all the way through, to {temp:165}.",
        ],
        common_mistake="Keeping a store rotisserie chicken in its warm plastic dome on the counter all evening. "
                       "It feels like it is staying hot, but it cools into the danger zone within an hour or two. "
                       "Eat what you want, then put the rest in the fridge right away.",
        freezing="Cooked chicken freezes well. Take it off the bone, pack it in freezer bags with a little broth "
                 "or sauce so it stays moist, and press out the air. Use it within 3 to 4 months. "
                 "It is great straight from the freezer in soups, wraps and fried rice.",
        sources=[FSIS_LEFTOVERS, FS_COLD_CHART, FOODKEEPER],
        related=["raw-chicken", "cooked-rice"],
    ),
    Food(
        slug="pizza",
        name="Leftover pizza",
        category="leftovers",
        question="How long does leftover pizza last?",
        description="Leftover pizza lasts 3 to 4 days in the fridge and 1 to 2 months in the freezer. "
                    "Pizza left out overnight should be thrown out. Here is why.",
        storage={
            "fridge": Span(3, 4, "days"),
            "freezer": Span(1, 2, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Pizza has cheese, meat and sauce on it, and all of them spoil. "
            "A slice is only as safe as the most fragile thing on top.",
        spoiled_signs=[
            "The cheese or crust shows any mold. Throw out the whole slice, not just the spot.",
            "It smells sour or off.",
            "The toppings feel slimy.",
            "The crust is hard as a rock. That one is not a safety issue, just a dry slice.",
        ],
        how_to_store=[
            "Take the slices out of the cardboard box. The box lets air in and the pizza dries out.",
            "Stack slices with paper between them in a sealed bag or box.",
            "Get the pizza into the fridge within 2 hours of delivery.",
            "Reheat slices in a hot pan or the oven for a crisp crust. The microwave makes it soft.",
            "Ordered extra on purpose? Freeze those slices on the first day, not the fourth. They will taste much better.",
        ],
        common_mistake="Leaving the box on the table after a party and eating a cold slice for breakfast. "
                       "Cold pizza is fine. Pizza that spent the night at room temperature is not, because the "
                       "cheese and meat sat for hours in the temperature range where germs grow fastest.",
        freezing="Wrap each slice in foil or plastic, then put them all in a freezer bag. They keep their taste "
                 "for 1 to 2 months. Bake them straight from frozen in a hot oven for about 10 minutes, "
                 "no thawing needed.",
        sources=[FS_COLD_CHART, FOODKEEPER, FSIS_LEFTOVERS],
        related=["cooked-chicken", "cooked-rice"],
    ),
    Food(
        slug="soup",
        name="Soup",
        category="leftovers",
        question="How long does soup last in the fridge?",
        description="Homemade soup and stew last 3 to 4 days in the fridge and 2 to 3 months in the freezer. "
                    "Here is how to cool a big pot safely.",
        storage={
            "fridge": Span(3, 4, "days", "Soups and stews, with or without meat."),
            "freezer": Span(2, 3, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="A big pot of soup holds its heat for hours. While it cools slowly, it passes through the warm range "
            "where germs grow fastest. The cooling is the risky part, not the fridge.",
        spoiled_signs=[
            "A sour smell, or a taste that is sharper than it should be.",
            "Bubbles or fizz when the soup is cold. That means something is growing in it.",
            "Mold on the top or around the edge of the box.",
            "A slimy layer, or a cloudy look in a soup that was clear.",
        ],
        how_to_store=[
            "Split a big pot into small, shallow boxes so each one cools fast.",
            "Put them in the fridge within 2 hours of cooking. Warm boxes are fine in the fridge.",
            "Reheat only the bowl you will eat, and bring it to a full boil or {temp:165}.",
            "Soups with cream or seafood are the most fragile, so eat those first.",
        ],
        common_mistake="Leaving the whole pot on the stove overnight to cool, then putting it in the fridge in the "
                       "morning. By then it has spent hours in the danger zone. Boiling it again kills germs but not "
                       "some of the toxins they leave behind, so a pot left out overnight should be thrown out.",
        freezing="Soup freezes very well for 2 to 3 months. Leave a little space at the top of each box, because it "
                 "swells as it freezes. Soups with pasta or potatoes go soft, so freeze the soup without them and "
                 "add them fresh when you reheat. Cream soups may split; stir them hard as they warm.",
        sources=[FS_COLD_CHART, FSIS_LEFTOVERS],
        related=["cooked-pasta", "cooked-rice"],
    ),
    Food(
        slug="cooked-pasta",
        name="Cooked pasta",
        category="leftovers",
        question="How long does cooked pasta last?",
        description="Cooked pasta lasts 3 to 4 days in the fridge and 1 to 2 months in the freezer. "
                    "Moldy pasta goes in the trash. Here is how to store it so it does not clump.",
        storage={
            "fridge": Span(3, 4, "days", "Plain or with sauce."),
            "freezer": Span(1, 2, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Cooked pasta is soft, wet and starchy, which suits germs and mold. "
            "The USDA FoodKeeper app allows up to 5 days, but we use the safer 3 to 4 day rule for all leftovers.",
        spoiled_signs=[
            "Slimy strands, or a film that will not rinse off.",
            "A sour or musty smell.",
            "Any mold. The USDA says moldy cooked pasta should be thrown out, not picked over.",
            "Dry, hard ends are just dried out. They are safe, but you can trim them.",
        ],
        how_to_store=[
            "Let it cool for a few minutes, then put it in a shallow sealed box within 2 hours.",
            "Toss plain pasta with a little oil so it does not stick into one block.",
            "Store pasta and sauce together or apart; both last 3 to 4 days.",
            "Reheat it with a splash of water in a pan or the microwave until it is steaming hot.",
        ],
        common_mistake="Cooking a whole bag of pasta on Sunday for the week. By Friday it is past its safe time. "
                       "Cook enough for 3 days, and freeze any extra right away instead of keeping it in the fridge "
                       "until it is too late.",
        freezing="Cooked pasta freezes for 1 to 2 months. Cook it a minute less than usual so it does not go mushy, "
                 "cool it, toss it with a little oil, and freeze it in portions. Baked pasta dishes like lasagna "
                 "freeze better than plain noodles. Reheat it straight from frozen in sauce or boiling water.",
        sources=[FOODKEEPER, FSIS_LEFTOVERS, FSIS_MOLDS],
        related=["soup", "cooked-rice", "cooked-shrimp"],
    ),
]
