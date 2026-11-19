from data.sources import FSIS_DATING, UK_DATES
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
]
