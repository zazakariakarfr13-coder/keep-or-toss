"""Every page's data, collected from the per-category modules."""
from data import foods_dairy, foods_eggs, foods_leftovers, foods_meat, foods_produce, guides, leftout

ALL_FOODS = [
    *foods_leftovers.FOODS,
    *foods_eggs.FOODS,
    *foods_dairy.FOODS,
    *foods_meat.FOODS,
    *foods_produce.FOODS,
]
ALL_LEFTOUT = [*leftout.LEFTOUT]
ALL_GUIDES = [*guides.GUIDES]
