# Keep or Toss — project log

## 2026-11-20
- Repo started; engine built task by task (see git log).

## 2026-11-20 — content wave 1
- Demand check: Google autocomplete for "how long does X last", "... in the fridge" and "X left out overnight" across 101 candidate foods in 10 categories. Every candidate returned 18-30 distinct suggestions, so demand is broad; foods are chosen for spread across categories. "Left out overnight" is searched for almost every food, which confirms the left-out page family.
- Sources verified in the browser: FSIS Leftovers (3-4 days, 3-4 months, 2h / 1h above 90°F), FoodSafety.gov Cold Storage Chart, FSIS Shell Eggs chart, FSIS Food Product Dating, GOV.UK date labels, CDC Listeria, USDA FoodKeeper JSON (bot-blocked for scripts; read in browser).
- Conservative rule applied: cooked rice uses FSIS 3-4 days rather than FoodKeeper's 4-6 days, and the page says so. Milk was postponed: FoodKeeper gives only "use-by date" and the chart has no milk row, so it gets a source first.
- Wave 1: 10 foods (cooked rice, cooked chicken, leftover pizza, eggs, hard-boiled eggs, butter, raw chicken, ground beef, deli meat, avocado), 3 left-out pages (rice, pizza, cooked chicken) and the best-before bridge guide. The trap-guard caught 3 pages under 220 words; each got a real extra detail. Thresholds unchanged.
- Site check: 0 problems. Highest pair similarity is below 0.10.

## 2026-11-20 — 438 searchable foods
- Owner approved wave 1 ("it looks good") and asked for ~300 foods in the search, plus clickable examples.
- Owner chose: every food searchable with an instant answer, while full pages keep growing (so there is no mass of thin pages).
- Added 428 quick-answer foods from the USDA FoodKeeper dataset (read in the browser; curated into plain names) in `data/quick.py`. They have no page of their own: they appear in the search and the checker, with "Source: USDA FoodKeeper and FSIS food safety guidance". Where FoodKeeper and the FSIS leftovers rule disagree (cooked pasta, quinoa, salads), the shorter time is used and noted. Conflicting or unclear rows are left out (canned tuna, tomatoes, prosciutto, string cheese, oat milk, which is not in FoodKeeper).
- Home: "Find a food" search (ranked, top 40), 20 clickable example foods, and results that fill in the checker without a page reload.

## 2026-11-20 — content wave 2 (10 guides)
- Salmon, cooked shrimp, bacon, yogurt, cheddar cheese, strawberries, ketchup, mayonnaise, soup, cooked pasta. New categories: Fish & seafood, Sauces & condiments.
- Sources verified in the browser: FoodSafety.gov Cold Storage Chart (fatty fish 1-3 d, shrimp 3-5 d, bacon 1 wk / 1 mo, soups 3-4 d / 2-3 mo), FSIS Molds on Food (hard cheese: cut 1 inch around; soft fruit, yogurt and cooked pasta: discard), FSIS Bacon and Food Safety (7 days; cooked leftover 4-5 days), FoodSafety.gov safe minimum temperatures (fish 145°F; shrimp pearly and opaque).
- Conservative picks: salmon 1-2 d (FoodKeeper) rather than chart 1-3 d; raw shrimp 1-3 d rather than 3-5 d; bacon freezer 1 mo (chart) rather than 4 mo (FSIS bacon page), stated on the page; cooked pasta 3-4 d (FSIS) rather than 3-5 d (FoodKeeper). Two unsourced homemade times were removed from the drafts.
- The trap-guard caught mayonnaise at 216 words; it got a real detail (squeeze bottles). Grades are 3.1-4.5. No page pair is above 0.10 similarity.
- Now 20 full guides plus 418 quick answers (438 foods). The quick "Salmon (raw)" and "Bacon (raw)" were replaced by the guides.
