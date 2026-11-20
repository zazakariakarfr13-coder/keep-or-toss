"""Site-wide settings. Change BASE_URL once when the custom domain is bought."""

SITE_NAME = "Keep or Toss"
BASE_URL = "https://zazakariakarfr13-coder.github.io/keep-or-toss/"
DECODER_URL = "https://zazakariakarfr13-coder.github.io/supermarket-decoder/decoder/"

CATEGORIES = {
    "dairy": "Dairy",
    "eggs": "Eggs",
    "meat": "Meat & poultry",
    "seafood": "Fish & seafood",
    "leftovers": "Leftovers & cooked food",
    "produce": "Fruit & vegetables",
    "bakery": "Bread & bakery",
    "pantry": "Pantry",
    "condiments": "Sauces & condiments",
    "drinks": "Drinks",
}

PLACES = ("fridge", "freezer", "pantry", "counter")

# Pages with a seasonal look: slug -> theme name (body class "theme-<name>" + optional static/art/<slug>.svg on top)
THEMES = {"ramadan-meal-prep": "ramadan"}

# Clickable examples under the home search box (slugs of pages or quick foods)
POPULAR = [
    "cooked-rice", "eggs", "pizza", "raw-chicken", "ground-beef", "deli-meat", "butter", "avocado",
    "strawberries", "bananas", "bacon", "salmon", "cheddar-cheese", "yogurt", "hummus-store-bought",
    "guacamole", "ketchup", "mayonnaise", "sandwich-bread-store-bought", "soup",
]

DISCLAIMER = "General guidance, not a guarantee. When in doubt, throw it out."

ANALYTICS_TOKEN: str | None = None  # Cloudflare Web Analytics beacon token
GSC_TOKEN: str | None = None  # Google Search Console verification meta tag

# Quality gates (starting values; tune with a reason logged in LOG.md)
MAX_GRADE = 8.0
SIMILARITY_MAX = 0.30
MIN_PROSE_WORDS = {"food": 220, "leftout": 120, "guide": 300}
