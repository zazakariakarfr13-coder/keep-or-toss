# Keep or Toss — project log

## 2026-11-20
- Repo started; engine built task by task (see git log).

## 2026-11-20 — content wave 1
- Demand check: Google autocomplete for "how long does X last", "... in the fridge" and "X left out overnight" across 101 candidate foods in 10 categories. Every candidate returned 18-30 distinct suggestions, so demand is broad; foods are chosen for spread across categories. "Left out overnight" is searched for almost every food, which confirms the left-out page family.
- Sources verified in the browser: FSIS Leftovers (3-4 days, 3-4 months, 2h / 1h above 90°F), FoodSafety.gov Cold Storage Chart, FSIS Shell Eggs chart, FSIS Food Product Dating, GOV.UK date labels, CDC Listeria, USDA FoodKeeper JSON (bot-blocked for scripts; read in browser).
- Conservative rule applied: cooked rice uses FSIS 3-4 days rather than FoodKeeper's 4-6 days, and the page says so. Milk was postponed: FoodKeeper gives only "use-by date" and the chart has no milk row, so it gets a source first.
- Wave 1: 10 foods (cooked rice, cooked chicken, leftover pizza, eggs, hard-boiled eggs, butter, raw chicken, ground beef, deli meat, avocado), 3 left-out pages (rice, pizza, cooked chicken) and the best-before bridge guide. The trap-guard caught 3 pages under 220 words; each got a real extra detail. Thresholds unchanged.
- Site check: 0 problems. Highest pair similarity is below 0.10.
