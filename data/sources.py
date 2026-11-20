"""Shared official sources, defined once and reused by every page."""
from kot.schema import Source

FOODKEEPER = Source("USDA / FoodSafety.gov", "FoodKeeper App",
                    "https://www.foodsafety.gov/keep-food-safe/foodkeeper-app")
FS_COLD_CHART = Source("FoodSafety.gov", "Cold Food Storage Chart",
                       "https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts")
FSIS_LEFTOVERS = Source("USDA FSIS", "Leftovers and Food Safety",
                        "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety")
FSIS_EGGS = Source("USDA FSIS", "Shell Eggs from Farm to Table",
                   "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/eggs/shell-eggs-farm-table")
FSIS_DATING = Source("USDA FSIS", "Food Product Dating",
                     "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-product-dating")
FDA_BAD_BUG_BOOK = Source("FDA", "Bad Bug Book (Bacillus cereus)",
                          "https://www.fda.gov/food/foodborne-pathogens/bad-bug-book-second-edition")
CDC_LISTERIA = Source("CDC", "Preventing Listeria Infection",
                      "https://www.cdc.gov/listeria/prevention/index.html")
UK_DATES = Source("GOV.UK", "Best before and use-by dates",
                  "https://www.gov.uk/understanding-food-labelling/best-before-and-use-by-dates")
FSIS_MOLDS = Source("USDA FSIS", "Molds on Food: Are They Dangerous?",
                    "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/molds-food-are-they-dangerous")
FSIS_BACON = Source("USDA FSIS", "Bacon and Food Safety",
                    "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/meat-catfish/bacon-and-food-safety")
FS_TEMPS = Source("FoodSafety.gov", "Safe Minimum Internal Temperatures",
                  "https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures")
