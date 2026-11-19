"""Shared official sources, defined once and reused by every page."""
from kot.schema import Source

FOODKEEPER = Source("USDA / FoodSafety.gov", "FoodKeeper App",
                    "https://www.foodsafety.gov/keep-food-safe/foodkeeper-app")
FSIS_LEFTOVERS = Source("USDA FSIS", "Leftovers and Food Safety",
                        "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety")
FDA_BAD_BUG_BOOK = Source("FDA", "Bad Bug Book (Bacillus cereus)",
                          "https://www.fda.gov/food/foodborne-pathogens/bad-bug-book-second-edition")
