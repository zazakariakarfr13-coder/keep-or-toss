from data.sources import CDC_LISTERIA, FOODKEEPER, FS_COLD_CHART, FSIS_BACON, FSIS_LEFTOVERS
from kot.schema import Food, Span

FOODS = [
    Food(
        slug="raw-chicken",
        name="Raw chicken",
        category="meat",
        question="How long does raw chicken last?",
        description="Raw chicken lasts only 1 to 2 days in the fridge and up to 9 months in the freezer. "
                    "Never thaw it on the counter. Here is how to handle it.",
        storage={
            "fridge": Span(1, 2, "days", "Pieces or a whole bird. Keep it at {temp:40} or colder."),
            "freezer": Span(9, 9, "months", "Pieces. A whole bird keeps its quality for up to 1 year."),
            "counter": None,
        },
        why="Raw chicken often carries germs like Salmonella. Cold slows them down but does not stop them, "
            "so raw chicken has one of the shortest fridge times of any food.",
        spoiled_signs=[
            "It smells sour or like eggs. Fresh chicken has almost no smell.",
            "It feels sticky or slimy, even after you rinse your fingers.",
            "The meat looks gray or green instead of pink.",
            "The pack is puffed up with air.",
        ],
        how_to_store=[
            "Put it in the fridge or freezer as soon as you get home.",
            "Keep it on the bottom shelf, in a dish or bag, so juices cannot drip onto other food.",
            "Cook or freeze it within 2 days, even if the date on the pack is later.",
            "Thaw it in the fridge, in cold water you change every 30 minutes, or in the microwave.",
        ],
        common_mistake="Thawing frozen chicken on the counter all day. The outside warms up long before the "
                       "middle thaws, and germs grow on the warm outside. Thaw it in the fridge overnight instead. "
                       "A pack of pieces usually needs about a day.",
        freezing="Raw chicken freezes very well. Wrap it tightly or use freezer bags with the air pressed out, "
                 "and write the date on it. Pieces keep their best quality for about 9 months, and a whole bird "
                 "for about a year. It stays safe while frozen, but it may dry out after that.",
        sources=[FS_COLD_CHART, FOODKEEPER, FSIS_LEFTOVERS],
        related=["cooked-chicken", "ground-beef"],
    ),
    Food(
        slug="ground-beef",
        name="Ground beef",
        category="meat",
        question="How long does ground beef last?",
        description="Raw ground beef lasts 1 to 2 days in the fridge and 3 to 4 months in the freezer. "
                    "Here is how to tell if it has gone bad.",
        storage={
            "fridge": Span(1, 2, "days", "Raw. Cooked ground beef lasts 3 to 4 days."),
            "freezer": Span(3, 4, "months"),
            "counter": None,
        },
        why="Grinding spreads germs from the surface of the meat all through it. "
            "That is why ground meat spoils much faster than a whole steak.",
        spoiled_signs=[
            "It smells sour or rotten. Fresh beef smells mild and meaty.",
            "It feels slimy or sticky.",
            "The whole pack has turned gray or brown, inside and out.",
            "A gray center with a red outside is normal. The middle just did not get air, so it is not a sign of spoilage.",
        ],
        how_to_store=[
            "Get it into the fridge within 2 hours of buying it, or 1 hour on a hot day.",
            "Keep it on the lowest shelf in a dish or bag, away from food you eat raw.",
            "Cook or freeze it within 2 days.",
            "Cook it until the middle reaches {temp:160}. Color alone does not tell you it is done.",
            "Once cooked, like taco meat or meat sauce, it lasts 3 to 4 days in the fridge, the same as other leftovers.",
        ],
        common_mistake="Trusting the color. People often throw out good beef because the middle is gray, and keep "
                       "bad beef because the outside is still red. Go by the date you bought it, the smell and the feel.",
        freezing="Flatten raw ground beef in a freezer bag before you freeze it. It freezes and thaws fast, and "
                 "it stacks well. Use it within 3 to 4 months for the best taste. Thaw it in the fridge, and cook "
                 "it within 1 to 2 days after it thaws.",
        sources=[FS_COLD_CHART, FOODKEEPER, FSIS_LEFTOVERS],
        related=["raw-chicken"],
    ),
    Food(
        slug="deli-meat",
        name="Deli meat",
        category="meat",
        question="How long does deli meat last?",
        description="Opened or deli-sliced lunch meat lasts 3 to 5 days in the fridge and 1 to 2 months in the freezer. "
                    "Here is why the clock starts when you open it.",
        storage={
            "fridge": Span(3, 5, "days", "Once opened, or if sliced at the deli counter. Sealed packs: up to 2 weeks."),
            "freezer": Span(1, 2, "months"),
            "counter": Span(0, 2, "hours", "Only 1 hour if the room is above {temp:90}."),
        },
        why="Deli meat can carry Listeria, a germ that keeps growing slowly even in a cold fridge. "
            "So deli meat has a short fridge time once the pack is open.",
        spoiled_signs=[
            "It feels slimy or leaves a film on your fingers.",
            "It smells sour or odd.",
            "The edges look shiny, dull or a different color.",
            "Listeria does not change the look or smell, so stick to the 3 to 5 day limit even if it seems fine.",
        ],
        how_to_store=[
            "Write the day you opened it on the pack.",
            "A sealed pack from the store keeps up to 2 weeks in the fridge. The 3 to 5 days start when you open it.",
            "Close the pack tightly, or move the slices to a sealed bag or box.",
            "Keep it in the coldest part of the fridge, not in the door.",
            "If you are pregnant, over 65, or have a weak immune system, heat deli meat until it is steaming hot, to {temp:165}.",
        ],
        common_mistake="Reading the date on the pack after it has been opened. That date is for a sealed pack. "
                       "Once you open it, you have 3 to 5 days, no matter what the label says.",
        freezing="You can freeze deli meat for 1 to 2 months. It may turn a bit watery when it thaws, so it works "
                 "best in hot dishes like melts, omelets and pasta. Freeze it in small portions with paper "
                 "between the slices, so you can take out only what you need.",
        sources=[FS_COLD_CHART, FOODKEEPER, CDC_LISTERIA],
        related=["raw-chicken"],
    ),
    Food(
        slug="bacon",
        name="Bacon",
        category="meat",
        question="How long does bacon last?",
        description="Raw bacon lasts 7 days in the fridge once you bring it home, and cooked bacon lasts 4 to 5 days. "
                    "Here is how to store bacon and tell if it has gone bad.",
        storage={
            "fridge": Span(7, 7, "days", "Raw bacon. Leftover cooked bacon: 4 to 5 days."),
            "freezer": Span(1, 1, "months"),
            "counter": None,
        },
        why="Bacon is cured with salt and smoke, which slows spoiling but does not stop it. "
            "Raw bacon is still raw pork, so it needs the fridge and full cooking.",
        spoiled_signs=[
            "A sour or rotten smell instead of a smoky, salty one.",
            "The meat turns gray, green or brown, or the fat turns yellow.",
            "A slimy or sticky film on the slices.",
            "Mold of any color. Throw out the whole pack.",
        ],
        how_to_store=[
            "Pick up bacon last at the store and put it in the fridge as soon as you get home.",
            "Once the pack is open, wrap the rest tightly or move it to a sealed bag.",
            "Use raw bacon within 7 days, or freeze it.",
            "Cool cooked bacon, wrap it in a paper towel inside a box, and eat it within 4 to 5 days.",
        ],
        common_mistake="Freezing a whole pack, then hacking at a frozen block for two slices. Roll each slice up, or lay "
                       "slices flat on a tray with paper between them, and freeze them before bagging. You can then "
                       "take out exactly what you need.",
        freezing="Raw bacon is best used within 1 month of freezing. The USDA bacon guide allows up to 4 months for "
                 "quality, but salty, fatty meat picks up off flavors in the freezer, so we use the shorter time from "
                 "the USDA storage chart. Thaw it in the fridge, or cook thin slices straight from frozen.",
        sources=[FSIS_BACON, FS_COLD_CHART, FOODKEEPER],
        related=["ground-beef", "raw-chicken"],
    ),
]
