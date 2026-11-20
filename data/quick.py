"""Quick-answer foods: official storage times, searchable and in the checker, no page of their own.

Source: USDA FoodKeeper data (fsis.usda.gov/shared/data/EN/foodkeeper.json, read 2026-11-20).
Where FoodKeeper and the FSIS leftovers rule disagree, the shorter (safer) time is used.
Foods that have a full page are left out here; the page is the answer.

Line format:  Name | category | fridge | freezer | pantry | counter | note
Times: "3-5d" (h d w m y), "o:" prefix = after opening, "no" = not recommended, empty = not listed.
"""
import re

from kot.schema import QuickFood, Span

_UNITS = {"h": "hours", "d": "days", "w": "weeks", "m": "months", "y": "years"}
_TIME = re.compile(r"^(o:)?(\d+)(?:-(\d+))?([hdwmy])$")
PLACES = ("fridge", "freezer", "pantry", "counter")
SOURCE = "USDA FoodKeeper and FSIS food safety guidance"


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower().replace("&", " "))
    return re.sub(r"-+", "-", s).strip("-")


def _span(token: str, note: str) -> Span | None:
    if token == "no":
        return None
    m = _TIME.match(token)
    if not m:
        raise ValueError(f"bad time {token!r}")
    opened, lo, hi, unit = m.groups()
    notes = (["After opening."] if opened else []) + ([note] if note else [])
    return Span(int(lo), int(hi or lo), _UNITS[unit], " ".join(notes))


def parse_line(line: str) -> QuickFood:
    parts = [p.strip() for p in line.split("|")]
    parts += [""] * (7 - len(parts))
    name, cat, *times, note = parts[:7]
    storage, note_used = {}, False
    for place, token in zip(PLACES, times):
        if not token:
            continue
        storage[place] = _span(token, "" if note_used or token == "no" else note)
        note_used = note_used or (token != "no" and bool(note))
    return QuickFood(slug=slugify(name), name=name, category=cat, storage=storage, source=SOURCE)


LINES = """
Buttermilk|dairy|1-2w|3m|||
Cheddar cheese|dairy|o:3-4w|6m|||Opened block. Unopened: 6 months.
Swiss cheese|dairy|o:3-4w|6m|||Opened block. Unopened: 6 months.
Parmesan cheese (block)|dairy|o:3-4w|6m|||Unopened: 6 months.
Gouda cheese|dairy|o:3-4w|6m|||Hard cheese. Unopened: 6 months.
Grated Parmesan|dairy|12m|no|||
Shredded cheese|dairy|1m|3-4m|||
Mozzarella (shredded)|dairy|1m|3-4m|||
American cheese slices|dairy|3-4w|no|||
Brie|dairy|1-2w|6m|||
Goat cheese|dairy|1-2w|6m|||
Camembert|dairy|1-2w|6m|||
Cottage cheese|dairy|o:1w|no|||Unopened: 2 weeks.
Cream cheese|dairy|2w|no|||
Ricotta|dairy|o:1w|no|||Unopened: 2 weeks.
Cheese curds|dairy|2w|4m|||
Heavy cream|dairy|10d|3-4m|||
Whipping cream (ultra-pasteurized)|dairy|o:1w|no|||Unopened: 1 month.
Half-and-half|dairy|3-4d|4m|||
Light cream|dairy|1w|3-4m|||
Whipped cream (homemade)|dairy|1d|1-2m|||
Whipped cream (aerosol can)|dairy|3-4w|no|||
Whipped topping (tub)|dairy|2w|14m|||
Sour cream dip|dairy|2w|no|||
Liquid coffee creamer|dairy|3w||||
Powdered coffee creamer|dairy|||o:2-3m||
Eggnog (store-bought)|dairy|3-5d|6m|||
Kefir|dairy|o:1-2d|no|||Unopened: 1 week.
Margarine|dairy|6m|12m|||
Yogurt|dairy|1-2w|1-2m|||
Lactose-free milk|dairy|o:1w|no|||
Ultra-pasteurized milk|dairy|o:7-10d||||Unopened: 1 to 3 months in the fridge.
Shelf-stable milk (UHT)|dairy|o:5-7d||6-12m||Pantry time is for an unopened carton.
Evaporated or condensed milk (canned)|dairy|o:4-5d||12m||Pantry time is for an unopened can.
Powdered milk|dairy|||o:3m||Unopened: 3 to 5 years.
Pudding (ready-made)|dairy|o:2d|no|||
Ghee|dairy|1-2y||6-8m||
Vegan cheese|dairy|o:3-7d||||
Quark|dairy|7-10d||||
Raw egg whites|eggs|2-4d|12m|||
Raw egg yolks|eggs|2-4d|no|||Yolks do not freeze well on their own.
Liquid egg substitute|eggs|o:3d|no|||Unopened: 1 week.
Quiche|eggs|3-5d|2-3m||2h|
Egg dishes (frittata, casserole)|eggs|3-4d|2-3m|||
Egg salad|eggs|3-4d|no|||
Steak (raw)|meat|3-5d|4-12m||no|
Beef roast (raw)|meat|3-5d|4-12m||no|
Beef stew meat (raw)|meat|3-5d|4-12m||no|
Brisket (raw)|meat|3-5d|4-12m||no|
Short ribs (raw)|meat|3-5d|4-12m||no|
Lamb chops (raw)|meat|3-5d|4-12m||no|
Leg of lamb (raw)|meat|3-5d|4-12m||no|
Lamb stew meat (raw)|meat|3-5d|4-12m||no|
Ground lamb (raw)|meat|1-2d|3-4m||no|
Veal roast (raw)|meat|3-5d|4-12m||no|
Ground veal (raw)|meat|1-2d|3-4m||no|
Pork chops (raw)|meat|3-5d|4-12m||no|
Pork roast (raw)|meat|3-5d|4-12m||no|
Pork tenderloin (raw)|meat|3-5d|4-12m||no|
Pork ribs (raw)|meat|3-5d|4-12m||no|
Pork shoulder (raw)|meat|3-5d|4-12m||no|
Ground pork (raw)|meat|1-2d|3-4m||no|
Goat meat (raw)|meat|3-5d|4-12m||no|
Ground goat (raw)|meat|1-2d|3-4m||no|
Venison (raw)|meat|3-5d|4-12m||no|
Bison steak (raw)|meat|3-5d|6-9m||no|
Ground bison (raw)|meat|1-2d|3-4m||no|
Rabbit (raw)|meat|2d|9m||no|
Liver and other organ meats|meat|1-2d|3-4m||no|
Uncured bacon (raw)|meat|4-7d|3-4w||no|
Turkey bacon|meat|o:7d|2-4m||no|Unopened: 2 weeks.
Corned beef (in pouch)|meat|5-7d|1m||no|
Ham (fully cooked, whole)|meat|1w|1-2m||2h|
Ham slices or spiral ham|meat|3-4d|1-2m||2h|
Hot dogs|meat|o:1w|1-2m||2h|Unopened: 2 weeks.
Sausage (raw)|meat|1-2d|1-2m||no|
Cooked sausage links|meat|1w|1-2m||2h|Smoked links and kielbasa.
Kielbasa|meat|1w|1-2m||2h|
Pepperoni (sliced)|meat|2-3w|1-2m|||
Salami (packaged)|meat|o:3-5d|1-2m||2h|Unopened: 2 weeks.
Deli turkey (packaged)|meat|o:3-5d|1-2m||2h|Unopened: 2 weeks.
Deli ham (packaged)|meat|o:3-5d|1-2m||2h|Unopened: 2 weeks.
Store-bought jerky|meat|o:2-3m||12m||Pantry time is for an unopened bag.
Homemade jerky|meat|1-2m||1-2m||
Canned meat|meat|o:3-4d||5y||Pantry time is for an unopened can.
Fresh chorizo (raw)|meat|1-2d|1-2m||no|
Bratwurst (raw)|meat|2-3d|2-3m||no|
Whole turkey (raw)|meat|1-2d|12m||no|
Turkey breast (raw)|meat|1-2d|9m||no|
Ground turkey (raw)|meat|1-2d|3-4m||no|
Ground chicken (raw)|meat|1-2d|3-4m||no|
Duck (raw)|meat|1-2d|6m||no|
Cornish hens (raw)|meat|1-2d|12m||no|
Giblets (raw)|meat|1-2d|3-4m||no|
Chicken nuggets (cooked)|meat|3-4d|1-3m||2h|
Fried chicken|meat|3-4d|4m||2h|
Canned chicken|meat|o:3-4d||5y||Pantry time is for an unopened can.
Pate|meat|1-2d|1-2m||2h|
Cod (raw)|seafood|1-2d|6-8m||no|
Haddock (raw)|seafood|1-2d|6-8m||no|
Halibut (raw)|seafood|1-2d|6-8m||no|
Flounder (raw)|seafood|1-2d|6-8m||no|
Sole (raw)|seafood|1-2d|6-8m||no|
Pollock (raw)|seafood|1-2d|4-8m||no|
Tuna steak (raw)|seafood|1-2d|2-3m||no|
Catfish (raw)|seafood|1-2d|2-3m||no|
Mackerel (raw)|seafood|1-2d|2-3m||no|
Cooked fish|seafood|3-4d|1-2m||2h|
Shrimp (raw)|seafood|1-3d|6-18m||no|
Scallops (raw)|seafood|1-3d|6-18m||no|
Squid (raw)|seafood|1-3d|6-18m||no|
Crayfish (raw)|seafood|1-3d|6-18m||no|
Shucked oysters, clams or mussels|seafood|3-10d|3-4m||no|
Live clams, mussels or oysters|seafood|1-2d|2-3m||no|
Fresh crab meat|seafood|1-3d|2-4m||no|
Pasteurized crab meat|seafood|o:3-5d|4-10m|||
Crab legs|seafood|2-4d|9-12m||no|
Live lobster|seafood|1d|no||no|Cook it the day you buy it.
Cooked shrimp|seafood|3-4d|1-3m||2h|
Cooked shellfish|seafood|3-4d|1-3m||2h|
Smoked salmon (sealed pack)|seafood|3-4w|6-12m|||Cold-smoked, vacuum-packed and unopened.
Hot-smoked fish (sealed pack)|seafood|2w|6-12m|||Unopened vacuum pack.
Tuna salad|seafood|3-4d|no||2h|
Shrimp salad|seafood|3-4d|no||2h|
Anchovies (canned)|seafood|o:3-4d|2m|5y||Pantry time is for an unopened can.
Caviar|seafood|o:2d|no|||
Soup|leftovers|3-4d|2-3m||2h|
Stew|leftovers|3-4d|2-3m||2h|
Chili|leftovers|3-4d|2-3m||2h|
Casserole|leftovers|3-4d|2-3m||2h|
Cooked pasta|leftovers|3-4d|1-2m||2h|USDA FoodKeeper allows up to 5 days; we use the safer leftovers rule.
Lasagna|leftovers|3-4d|2-3m||2h|
Mac and cheese|leftovers|3-4d|1-2m||2h|
Mashed potatoes|leftovers|3-4d|1-2m||2h|
Baked potatoes (cooked)|leftovers|3-4d|1-2m||2h|
Cooked vegetables|leftovers|3-4d|1-2m||2h|
Fried rice|leftovers|3-4d|1-2m||2h|
Cooked quinoa|leftovers|3-4d|6-12m||2h|USDA FoodKeeper allows up to 7 days; we use the safer leftovers rule.
Leftover turkey|leftovers|3-4d|3-4m||2h|
Leftover steak|leftovers|3-4d|2-3m||2h|
Leftover pork|leftovers|3-4d|2-3m||2h|
Meatballs (cooked)|leftovers|3-4d|2-3m||2h|
Tacos and burritos|leftovers|3-4d|2-3m||2h|
Takeout meals|leftovers|3-4d|2-3m||2h|
Stuffing (cooked)|leftovers|3-4d|1-2m||2h|
Gravy (homemade)|leftovers|1-2d|2-3m||2h|
Homemade broth|leftovers|3-4d|2-3m||2h|
Vegetable soup (homemade)|leftovers|3-4d|3m||2h|
Potato salad|leftovers|3-4d|no||2h|
Pasta salad|leftovers|3-4d|no||2h|
Macaroni salad|leftovers|3-4d|no||2h|
Chicken salad|leftovers|3-4d|no||2h|
Ham salad|leftovers|3-4d|no||2h|
Coleslaw (homemade)|leftovers|3-5d|no||2h|
Guacamole|leftovers|3-4d|3-4m||2h|
Hummus (store-bought)|leftovers|o:7d|no|||Unopened: 3 months in the fridge.
Hummus (homemade)|leftovers|7d|no||2h|
Fresh salsa|leftovers|4-7d|||2h|
Cut fruit|leftovers|4d|no||2h|
Olives from the olive bar|leftovers|2w|no|||
Refried beans (opened can)|leftovers|2-3d||||
Kugel (homemade)|leftovers|3-4d|1m||2h|
Apples|produce|4-6w|8m|3w||Pantry means a cool spot on the counter.
Apricots|produce|2-5d|no|||
Bananas|produce|3d|2-3m|||Fridge time is for ripe bananas. The skin goes dark, the fruit stays fine.
Cherries|produce|2-3d|8-12m|||
Strawberries|produce|2-3d|8-12m|||
Raspberries|produce|2-3d|8-12m|||
Blackberries|produce|3-6d|12m|||
Blueberries|produce|1-2w|8-12m|||
Cranberries (fresh)|produce|2m|12m|||
Lemons|produce|10-21d||10d||Pantry means on the counter.
Limes|produce|10-21d||10d||Pantry means on the counter.
Oranges|produce|10-21d||10d||Pantry means on the counter.
Grapefruit|produce|10-21d||10d||Pantry means on the counter.
Clementines|produce|10-21d||10d||Pantry means on the counter.
Tangerines|produce|10-21d||10d||Pantry means on the counter.
Fresh coconut|produce|2-3w||1w||
Dates|produce|12m|1-2y|2m||
Grapes|produce|1w|1m|1d||
Guava|produce|2-4d|no|||
Kiwi|produce|3-6d|no|||
Whole melon|produce|2w|1m|||Watermelon, cantaloupe or honeydew, uncut.
Cut melon|produce|2-4d|1m||2h|Watermelon, cantaloupe or honeydew.
Mango|produce|1w|6-8m|3-5d||
Papaya|produce|1w|6-8m|3-5d||
Passion fruit|produce|1w|6-8m|3-5d||
Peaches|produce|3-5d|2m|||
Nectarines|produce|3-5d|2m|||
Plums|produce|3-5d|2m|||
Pears|produce|3-5d|2m|||
Pineapple|produce|5-7d|10-12m|||
Plantains|produce|3-5d|10-12m|||
Pomegranate|produce|1-3m|10-12m|2-5d||
Kumquats|produce|3w|no|||
Star fruit|produce|1-2w|10-12m|1w||
Prickly pear|produce|1-2w|10-12m|2-5d||
Dragon fruit|produce|2-3w|10-12m|2-5d||
Applesauce (homemade)|produce|3w|8-12m|||
Artichokes|produce|1-2w|no|1-2d||
Asparagus|produce|3-4d|5m|||
Green beans|produce|3-5d|8m|||
Snap peas|produce|3-5d|8m|||
Snow peas|produce|3-5d|8m|||
Lima beans (fresh)|produce|3-5d|8m|||
Beets|produce|1-2w|6-8m|1d||
Bok choy|produce|2-3d|10-12m|||
Broccoli|produce|3-5d|10-12m|||
Brussels sprouts|produce|3-5d|10-12m|||
Cabbage|produce|1-2w|10-12m|||
Carrots|produce|2-3w|10-12m|||
Baby carrots|produce|4w|3m|4d||
Parsnips|produce|2-3w|10-12m|||
Cauliflower|produce|3-5d|10-12m|||
Celery|produce|1-2w|10-12m|||
Corn on the cob|produce|1-2d|8m|||
Cucumbers|produce|4-6d|no|||
Eggplant|produce|4-7d|6-8m|1d||
Garlic|produce||1m|1m||A whole bulb in a cool, dry spot.
Ginger root|produce|2-3w|6m|2-5d||
Collard greens|produce|1-4d|10-12m|||
Kale|produce|3-5d|8-12m|||
Swiss chard|produce|1-2w||||
Leeks|produce|1-2w|10-12m|||
Iceberg lettuce|produce|1-2w|no|||
Romaine lettuce|produce|1-2w|no|||
Leaf lettuce|produce|3-7d|no|||
Spinach|produce|3-7d|no|||
Bagged salad greens|produce|3-5d|no|||Once the bag is opened: 2 days.
Arugula|produce|3-7d||||
Radicchio|produce|2-3w||||
Mushrooms|produce|3-7d|10-12m|||
Okra|produce|2-3d|10-12m|1d||
Onions|produce|2m|10-12m|1m||Whole onions. Pantry means a cool, dry, dark spot.
Green onions|produce|1w|10-12m|||
Bell peppers|produce|4-14d|6-8m|||
Hot peppers|produce|1w|9m|||
Potatoes|produce|1-2w|10-12m|1-2m||Pantry means a cool, dark spot.
Sweet potatoes|produce|||2-3w||Keep them in a cool, dry spot.
Pumpkins|produce|||2-3m||Whole pumpkins.
Radishes|produce|10-14d|no|||
Rhubarb|produce|3-7d||||
Rutabagas|produce|2-3w|8-10m|1w||
Turnips|produce|2w|8-10m|||
Zucchini|produce|4-5d|10-12m|||
Summer squash|produce|4-5d|10-12m|||
Winter squash|produce|1-3m|10-12m|2-6w||Butternut, acorn and similar.
Spaghetti squash|produce|||2m||Whole. Cut: 4 to 5 days in the fridge.
Cherry tomatoes|produce|5d||10d||
Yuca (cassava)|produce|3d|1-2m|7d||
Celery root|produce|1w||||
Kohlrabi|produce|1w|8-12m|||
Jicama|produce|2-3w||||
Bean sprouts|produce|5-10d||||
Edamame (fresh)|produce|4-5d||||
Fresh basil|produce|10d||5d||
Fresh cilantro|produce|2-3w||1-2w||
Fresh mint|produce|2-3w||1-2w||
Fresh parsley|produce|2-3d|3-4m|||
Fresh rosemary|produce|2-3w||1-2w||
Fresh thyme|produce|2-3w||1-2w||
Fresh chives|produce|2-3w||1-2w||
Fresh oregano|produce|2-3w||1-2w||
Lemongrass|produce|7-9d|6m|||
Kimchi|produce|6-12m||||
Sandwich bread (store-bought)|bakery|2-3w|3-5m|14-18d||
Whole wheat bread|bakery||3m|3-5d||
Homemade bread|bakery||3m|3-5d||
Flour tortillas|bakery|o:3m|6m|3m||
Corn tortillas|bakery|60-90d||25-45d||
Bagels|bakery||3m|1-2d||Fresh-baked.
Muffins|bakery||2-3m|3-7d||
Cake (store-bought)|bakery|7-10d|6m|3-7d||
Cheesecake|bakery|5-7d|3-6m|||
Soft cookies|bakery||8-12m|2-3m||
Crispy cookies|bakery||8-12m|4-6m||
Cream pie|bakery|3-4d|no|||Banana cream, coconut cream and similar.
Fruit pie|bakery|1w|8m|1-2d||Apple, cherry, blueberry and similar.
Pumpkin pie|bakery|3-4d|1-2m||2h|
Pecan pie|bakery|3-4d|1-2m||2h|
Doughnuts|bakery||no|1-2d||
Eclairs|bakery|2-3d|3m|||
Cinnamon rolls|bakery||3m|1-3d||
Macarons|bakery||3m|1-2d||
Frosting (opened)|bakery|o:2-3w||10-12m||Pantry time is for an unopened tub.
Baking powder|pantry|||o:3-6m||
Baking soda|pantry|||o:6m||
Pancake mix|pantry|||9m||
Cake mix|pantry|||12-18m||
Baking chocolate|pantry|||o:1y||
Cocoa powder|pantry|||o:1y||
Cornmeal|pantry|||6-12m||
Cornstarch|pantry|||18m||
White flour|pantry|||o:6-8m||
Whole wheat flour|pantry|o:6-8m||3-6m||
Gelatin|pantry|||o:3-4m||Flavored gelatin mix.
Olive oil|pantry|o:4m||o:3-5m||Unopened: 6 to 12 months.
Vegetable oil|pantry|o:4m||o:3-5m||Unopened: 6 to 12 months.
Canola oil|pantry|||1y||
Coconut oil|pantry|||3y||
Sesame oil|pantry|||o:6m||
Avocado oil|pantry|||o:6m||
Shortening|pantry|||o:6-12m||
Ground spices|pantry|||2-3y||
Whole spices|pantry|||3-4y||
Dried herbs|pantry|||1-2y||
Cinnamon|pantry|||3-4y||
Cumin|pantry|||3-4y||
Black pepper|pantry|||2y||
Garlic powder|pantry|||3-4y||
Onion powder|pantry|||3-4y||
Chili powder|pantry|||2y||
White sugar|pantry|||18-24m||
Brown sugar|pantry|||18-24m||
Powdered sugar|pantry|||18-24m||
Vanilla extract|pantry|||o:12m||
Yeast|pantry|o:4m||2y||Pantry time is for unopened packets.
Dried beans|pantry|||1y||
Lentils|pantry|||1y||
Split peas|pantry|||1y||
Dry pasta|pantry|||o:1y||
Egg noodles (dry)|pantry|||o:1-2m||
White rice (uncooked)|pantry|6m||o:1y||
Brown rice (uncooked)|pantry|6m||o:1y||
Quinoa (uncooked)|pantry|||2-3y||
Oats|pantry|||o:4m||
Barley|pantry|||o:6m||
Bulgur|pantry|||6-12m||
Grits|pantry|||12m||
Breakfast cereal|pantry|||o:2-3m||
Oatmeal|pantry|||o:6-12m||
Crackers|pantry|||o:1m||
Dried fruit|pantry|6m||o:1m||Raisins, apricots, mango and similar.
Marshmallows|pantry|||o:1m||
Mixed nuts (jar)|pantry|||o:2-9m||
Almonds|pantry|8m|10m|4m||Shelled.
Cashews|pantry|6m|12m|2-4w||
Walnuts|pantry|9-12m|24m|2-4w||
Pecans|pantry|9m|24m|2-4w||Shelled.
Pistachios|pantry|12m|24m|3w||
Peanuts|pantry|12m|24m|4w||Shelled.
Macadamia nuts|pantry|12m|24m|2-4w||
Pine nuts|pantry|3m|9m|2-3w||
Peanut butter|pantry|o:3-4m||o:2-3m||Unopened: 6 to 9 months in the pantry.
Natural peanut butter|pantry|o:3-4m||||Keep it in the fridge once opened.
Honey|pantry|||2y||
Maple or pancake syrup|pantry|o:6m||1y||Pantry time is for an unopened bottle.
Molasses|pantry|||o:6m||
Chocolate syrup|pantry|o:6m||2y||Pantry time is for an unopened bottle.
Popcorn kernels|pantry|||o:1y||
Microwave popcorn|pantry|||6-12m||
Potato chips|pantry|||o:1-2w||
Pretzels|pantry|||o:3w||
Instant mashed potatoes|pantry|||o:6-12m||
Pudding mix|pantry|||o:3-4m||
Bouillon cubes|pantry|||1y||
Canned soup, beans and vegetables|pantry|o:3-4d||2-5y||Pantry time is for unopened cans.
Canned fruit and tomatoes|pantry|o:5-7d||12-18m||Pantry time is for unopened cans.
Applesauce (jar)|pantry|o:7-10d||12-18m||Pantry time is for an unopened jar.
Canned coconut milk|pantry|o:4d|3m|2-5y||Pantry time is for an unopened can.
Tomato paste|pantry|o:5d|2-3m|27m||Pantry time is for an unopened can.
Sun-dried tomatoes (jar)|pantry|o:3-6m||1y||
Chia seeds|pantry|||18m||
Flaxseed (whole)|pantry|||2y||
Ground flaxseed|pantry|12m|12m|||
Sunflower seeds|pantry|||o:3-4m||Roasted, shelled.
Pumpkin seeds|pantry|||6m||
Granola|pantry|||6-9m||
Granola bars|pantry|||6-12m||
Breadcrumbs|pantry|||6m||
Barbecue sauce|condiments|o:4m||1y||Pantry time is for an unopened bottle.
Chutney|condiments|o:1-2m||1y||
Horseradish|condiments|o:3-4m||||
Jam and jelly|condiments|o:6-12m||6-18m||Pantry time is for an unopened jar.
Ketchup|condiments|o:6m||1y||Opened ketchup is safe in the cupboard; the fridge keeps its taste.
Cocktail sauce|condiments|o:6m||1y||
Marinades|condiments|o:6m||1y||
Mayonnaise|condiments|o:2m||3-6m||Pantry time is for an unopened jar.
Mustard|condiments|o:1y||1-2y||
Olives (jar)|condiments|o:2w||12-18m||
Pickles|condiments|o:1-3m||1y||
Relish|condiments|9m||||
Pesto (jar)|condiments|o:3d|1m|||
Bottled salad dressing|condiments|o:1-3m||10-12m||Pantry time is for an unopened bottle.
Ranch and creamy dressings|condiments|o:3-4w|no|6m||
Vinaigrette|condiments|o:4w|no|6m||
Homemade salad dressing|condiments|2w||||
Salsa (jar)|condiments|o:1m||1y||
Soy sauce|condiments|o:1m||3y||Pantry time is for an unopened bottle.
Teriyaki sauce|condiments|o:1m||3y||
Hoisin sauce|condiments|o:3-6m||18-24m||
Oyster sauce|condiments|o:3-6m||18-24m||
Black bean sauce|condiments|o:3-6m||18-24m||
Hot sauce|condiments|||6m||
Worcestershire sauce|condiments|||1y||
Vinegar|condiments|||2y||
Tahini|condiments|o:3w||1y||
Thai curry paste|condiments|o:5d||2y||
Cranberry sauce (canned)|condiments|o:1-2w||2y||
Cranberry sauce (homemade)|condiments|7-10d||||
Pasta sauce (jar)|condiments|o:4d||18m||Pantry time is for an unopened jar.
Tomato sauce (opened)|condiments|o:4d||||
Gravy (jar)|condiments|o:1-2d||2-5y||
Homemade aioli|condiments|3-4d|||2h|
Bacon grease|condiments|6m|12m|||
Lemon juice (bottled)|condiments|o:2m||12-18m||
Lime juice (bottled)|condiments|o:2m||12-18m||
Orange juice (carton)|drinks|o:7-10d|8-12m|||
Fresh-squeezed orange juice|drinks|2-3d||||
Fruit juice (carton)|drinks|o:8-12d||||
Fresh-squeezed apple juice|drinks|6d|12m|||
Fresh-squeezed lemon juice|drinks|6d|12m|||
Apple cider (fresh)|drinks|2-3w||||
Soda (opened)|drinks|o:2-3d||||
Almond milk|drinks|o:7-10d||||
Soy milk|drinks|o:7-10d||||
Rice milk|drinks|o:7-10d||||
Coconut milk (carton)|drinks|o:7-10d||||
Coconut water|drinks|o:1-2d|12m|||
Red wine (opened)|drinks|o:1-3d||||
White wine (opened)|drinks|o:1-3d||||
Nutrition shakes|drinks|o:2d||2-5y||Pantry time is for unopened cans.
Ground coffee|drinks||6-12m|o:2w||
Instant coffee|drinks|||o:2-3m||
Tea bags|drinks|||o:6-12m||
Loose-leaf tea|drinks|||o:6-12m||
"""

QUICK = [parse_line(l) for l in LINES.strip().splitlines() if l.strip()]
