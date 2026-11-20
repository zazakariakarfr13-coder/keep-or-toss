from data.sources import FOODKEEPER, FS_COLD_CHART, FS_TEMPS, FSIS_DATING, FSIS_LEFTOVERS, UK_DATES
from kot.schema import Guide, Section

GUIDES = [
    Guide(
        slug="best-before-vs-use-by",
        kind="bridge",
        title="Best before vs use by vs sell by: what do the dates on food mean?",
        description="Best before is about taste. Use by is about safety in Europe and the UK. Sell by is for the "
                    "store. Here is what each food date really means.",
        answer="In the US, most dates are about quality, not safety. In the UK and Europe, a use-by date is about "
               "safety, so do not eat food after it. A best-before date is about quality everywhere.",
        sections=[
            Section("What does best before mean?", [
                "A best-before date, or best if used by, tells you when the food tastes and looks its best. "
                "It is not a safety date. Crackers, pasta, rice and canned food are often fine for a long time "
                "after it, as long as the pack is closed and dry.",
                "After the date, check the food. If it smells, looks and tastes normal, it is usually fine to eat.",
            ]),
            Section("What does use by mean?", [
                "In the US, a use-by date is the last day the maker thinks the food is at its best. "
                "It is not a safety date, except on baby formula.",
                "In the UK and the European Union, use by is a safety date. It goes on food that spoils fast, "
                "like fresh meat, fish and ready salads. Eating it after that day could make you ill, "
                "even if it looks and smells fine.",
                "You can cook or freeze the food on or before its use-by date to make it last longer.",
            ]),
            Section("What does sell by mean?", [
                "A sell-by date is for the store. It tells staff how long to keep the item on the shelf. "
                "It is not a safety date, and most food is fine for some time after it if you keep it cold.",
            ]),
            Section("Is there a law about food dates in the US?", [
                "Not for most foods. Federal rules only require a date on baby formula. "
                "Makers choose their own dates and their own words, which is why labels look so different from one pack to the next.",
            ]),
            Section("So how long can you keep a food after its date?", [
                "Once you open a pack, the printed date no longer applies. What counts is how long the food has "
                "been open and how you kept it. That is what every food page on this site tells you.",
            ], bullets=[
                "Opened deli meat: 3 to 5 days, whatever the pack says.",
                "Eggs: 3 to 5 weeks in the fridge from the day you buy them.",
                "Leftovers: 3 to 4 days in the fridge.",
            ]),
        ],
        sources=[FSIS_DATING, UK_DATES],
        related=["deli-meat", "eggs", "cooked-rice"],
    ),
    Guide(
        slug="ramadan-meal-prep",
        kind="seasonal",
        title="Ramadan meal prep: how long iftar and suhoor food lasts",
        description="Cooked iftar food lasts 3 to 4 days in the fridge and 2 to 3 months frozen. Safe batch cooking, "
                    "keeping food warm and freezing for Ramadan.",
        answer="Cooked food keeps 3 to 4 days in the fridge and 2 to 3 months in the freezer. Food left out for more "
               "than 2 hours should be thrown out. If you keep food warm until sunset, keep it at {temp:140} or hotter.",
        sections=[
            Section("Can you cook iftar in the morning?", [
                "Yes, if you cool it and keep it cold, or keep it hot the whole time. The risky part is the hours in "
                "between, when warm food slowly cools down on the stove.",
                "Cook in the morning, split the food into shallow boxes, and put them in the fridge within 2 hours. "
                "Before sunset, reheat each dish until it is steaming hot, to {temp:165}.",
            ]),
            Section("How do you keep food warm until sunset?", [
                "Hot food has to stay at {temp:140} or hotter the whole time. A slow cooker on its warm setting or a "
                "low oven can do this. A pot with the lid on and the heat off cannot. It slowly cools into the range "
                "where germs grow fastest.",
            ], bullets=[
                "Check warm food with a food thermometer now and then.",
                "Heat cold leftovers up fully before you add them to a pot that is keeping warm.",
            ]),
            Section("Can you eat iftar leftovers at suhoor?", [
                "Yes. Put leftovers in the fridge within 2 hours of iftar, not when you go to bed. At suhoor, reheat "
                "only what you will eat until it is steaming hot.",
                "Count the days from when the food was cooked, not from iftar. A dish cooked on Monday morning should "
                "be eaten or frozen by Thursday.",
            ]),
            Section("How long does harira or lentil soup last?", [
                "Like other soups and stews, harira and lentil soup last 3 to 4 days in the fridge and 2 to 3 months "
                "in the freezer. Lentils and chickpeas thicken the soup as it sits, so add a splash of water when you "
                "reheat it.",
            ]),
            Section("Can you freeze samosas, briouats and spring rolls?", [
                "Yes. Freeze them uncooked in one layer on a tray, then move them to a freezer bag once they are hard. "
                "Fry or bake them straight from frozen, and make sure meat fillings are cooked all the way through.",
                "Fried or baked ones can be frozen too. The USDA guide for cooked dishes is 2 to 3 months in the "
                "freezer for the best taste. Reheat them in the oven so they turn crisp again.",
            ]),
            Section("A simple freezer plan for the month", [
                "A few hours of cooking before Ramadan saves time on every long fasting day.",
            ], bullets=[
                "Cook and freeze soup bases, sauces and fillings in family-size portions.",
                "Label every bag with what is inside and the date.",
                "Each night, move the next day's food from the freezer to the fridge so it thaws safely.",
                "Keep dates sealed in the pantry, fridge or freezer so they last the whole month.",
            ]),
        ],
        sources=[FSIS_LEFTOVERS, FS_COLD_CHART, FS_TEMPS, FOODKEEPER],
        related=["dates", "soup", "cooked-rice", "cooked-chicken"],
    ),
]
