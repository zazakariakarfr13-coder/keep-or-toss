# Keep or Toss Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and launch the Keep or Toss food-storage website: about 80 answer-first pages plus the "Is it still OK?" checker. It is generated from one data source, guarded against thin and duplicate pages, and hosted free on GitHub Pages.

**Architecture:** Food facts and per-page prose live in Python data modules under `data/`. The `kot` package validates them, renders static HTML, and runs the quality gates: reading level, similarity, and answer-first. GitHub Actions runs the tests, builds `_site/`, runs `scripts/check_site.py` against it, and deploys. The checker is plain JavaScript that reads `checker.json`, which is exported at build time.

**Tech Stack:** Python 3.12, standard library only for build and tests (`unittest`, `html.parser`, `json`, `pathlib`). Pillow is used locally only, for share and pin images, which are committed. Plain HTML, CSS and JS; JS tests use `node --test` (Node 26, portable install). GitHub Pages via Actions.

**Spec:** `docs/superpowers/specs/2026-11-20-keep-or-toss-design.md`

## Global Constraints

- Budget $0: no paid service, plan or dependency. pytest is not installed, so use `unittest`. Nothing is pip-installed for CI.
- Repo `keep-or-toss` on account `zazakariakarfr13-coder`. The name is final and never renamed. `BASE_URL = "https://zazakariakarfr13-coder.github.io/keep-or-toss/"` is defined once in `kot/config.py`, so adding the custom domain later means a one-line change.
- Answer first: on every food and left-out page, the answer box is the first element in `<main>` after the `<h1>`.
- Reading level: prose is at US grade 8 or below (Flesch–Kincaid).
- Trap-guard: no near-identical pages; each page has a minimum amount of its own prose.
- Storage times come from USDA FoodKeeper, FoodSafety.gov, USDA FSIS and FDA, cited on each page. Where sources disagree, use the more conservative figure. The note "General guidance, not a guarantee. When in doubt, throw it out." appears on every food, left-out and guide page.
- Freezer times are labelled "quality", not "safety".
- Temperatures are shown in °F with °C: `40°F (4°C)`.
- Verdict colours always come with an icon and a word (✓ KEEP, ⏱ USE TODAY, ✕ TOSS).
- Never push to GitHub, schedule pins, or create accounts without the owner's explicit approval. Never put paid PDFs in this repo.
- Commands on this PC: `py -3` for Python, `C:\Program Files\Git\cmd\git.exe` for git, `C:\Program Files\GitHub CLI\gh.exe` for gh. Node may need PATH refreshed from the User/Machine env vars.

## Review Focus

1. **Last day of a range** (cooked rice opened 4 days ago when the fridge range is 3–4 days): the verdict must be USE TODAY, not KEEP. → Task 6 test `boundary day is use-today`.
2. **Freezer past its quality time:** the verdict must be KEEP with the note "safe while frozen; taste and texture fade", never TOSS. → Task 6 test `freezer past max keeps with quality note`.
3. **A place a food has no time for** (a counter time for raw chicken): the checker must not offer that place, and the data must say "not recommended" rather than inventing a time. → Task 1 test `test_place_none_means_not_recommended`, Task 6 test `places only lists stored places`.
4. **A date in the future or empty input:** show "Pick when it was opened or cooked", never a verdict. → Task 6 test `future or missing date gives no verdict`.
5. **A `related` link or `food` reference that points to a missing slug:** the build must fail with the slug named, not publish a broken link. → Task 1 test `test_unknown_related_slug_fails`.

---

## File Structure

```
keep-or-toss/
  kot/__init__.py
  kot/config.py          BASE_URL, SITE_NAME, CATEGORIES, DISCLAIMER, ANALYTICS_TOKEN=None, thresholds
  kot/schema.py          dataclasses + validate_all()
  kot/quality.py         reading_grade(), prose_words(), similarity(), find_duplicates()
  kot/render.py          page HTML (food, left-out, guide, hub, home, static pages)
  kot/build.py           build(out_dir) -> list[str] of written page paths; CLI
  data/__init__.py       ALL_FOODS, ALL_LEFTOUT, ALL_GUIDES (collects the modules below)
  data/foods_<category>.py   one module per category, list FOODS
  data/leftout.py        list LEFTOUT
  data/guides.py         list GUIDES (country, emergency, bridge)
  static/site.css  static/checker.js  static/favicon.svg  static/img/share/*.png
  scripts/check_site.py  scripts/make_images.py
  tests/test_schema.py tests/test_quality.py tests/test_render.py tests/test_build.py tests/test_check_site.py
  tests/js/checker.test.mjs
  .github/workflows/pages.yml
  LOG.md  README.md  .gitignore (_site/)
```

Run the Python tests with `py -3 -m unittest discover -s tests -v` from the repo root.

---

### Task 1: Repo, config and data schema

**Files:** Create `kot/__init__.py`, `kot/config.py`, `kot/schema.py`, `data/__init__.py` (empty lists for now), `tests/test_schema.py`, `.gitignore`, `README.md`, `LOG.md`.

**Interfaces — Produces:**
- `config.CATEGORIES: dict[str, str]`, mapping slug to display name: `dairy` Dairy, `eggs` Eggs, `meat` Meat & poultry, `seafood` Fish & seafood, `leftovers` Leftovers & cooked food, `produce` Fruit & vegetables, `bakery` Bread & bakery, `pantry` Pantry, `condiments` Sauces & condiments, `drinks` Drinks.
- `config.PLACES = ("fridge", "freezer", "pantry", "counter")`
- `config.ANALYTICS_TOKEN: str | None = None`, `config.GSC_TOKEN: str | None = None` (the Search Console meta tag is rendered only when set), `config.DISCLAIMER = "General guidance, not a guarantee. When in doubt, throw it out."`
- `@dataclass Span(min: float, max: float, unit: Literal["hours","days","weeks","months"], note: str = "")`, plus `Span.max_hours() -> float` (day=24, week=168, month=720).
- `@dataclass Source(publisher: str, title: str, url: str)`
- `@dataclass Food(slug, name, category, question, storage: dict[str, Span | None], why: str, spoiled_signs: list[str], how_to_store: list[str], common_mistake: str, freezing: str, sources: list[Source], related: list[str], description: str)`. A `storage` place set to `None` means "not recommended". A place that is absent is not shown.
- `@dataclass LeftOut(slug, food: str, question, verdict: Literal["toss","keep","depends"], verdict_line: str, risk: str, next_time: list[str], sources, related, description)`
- `@dataclass Section(heading: str, paragraphs: list[str], bullets: list[str] = [])`
- `@dataclass Guide(slug, kind: Literal["country","emergency","bridge"], title, description, answer: str, sections: list[Section], sources, related)`
- `validate_all(foods, leftout, guides) -> None` raises `ValueError` naming the slug and the problem.

- [ ] **Step 1: Initialise the repo.** In `ADP Launch\keep-or-toss`, run `git init -b main`. Add `.gitignore` with `_site/` and `__pycache__/`.
- [ ] **Step 2: Write the failing tests** in `tests/test_schema.py`, using a `make_food(**over)` helper that returns a valid `Food`:
  - `test_valid_food_passes`: `validate_all([make_food()], [], [])` raises nothing.
  - `test_duplicate_slug_fails`: two foods with slug `cooked-rice` raise `ValueError` containing `"cooked-rice"`, across all three lists.
  - `test_unknown_related_slug_fails`: `related=["nope"]` raises an error containing `"nope"`.
  - `test_leftout_unknown_food_fails`: `LeftOut(food="nope")` raises.
  - `test_unknown_category_fails`
  - `test_food_needs_a_source`: `sources=[]` raises.
  - `test_span_min_le_max`: `Span(5, 3, "days")` raises.
  - `test_place_none_means_not_recommended`: `storage={"fridge": Span(1,2,"days"), "counter": None}` is valid.
  - `test_max_hours`: `Span(3,4,"days").max_hours() == 96`, and `Span(1,2,"months").max_hours() == 1440`.
- [ ] **Step 3:** Run `py -3 -m unittest tests.test_schema -v`. Expected: errors (module not found).
- [ ] **Step 4:** Implement `config.py` and `schema.py` per the interfaces. Slugs must match `^[a-z0-9-]+$`.
- [ ] **Step 5:** Run the tests again. Expected: 9 pass.
- [ ] **Step 6:** Commit: `git add -A; git commit -m "Add config and validated data schema"`.

### Task 2: Quality gates (reading level and trap-guard)

**Files:** Create `kot/quality.py`, `tests/test_quality.py`.

**Interfaces — Produces:**
- `count_syllables(word: str) -> int`: vowel groups (`aeiouy`), minus 1 for a final silent `e` (not `le`), minimum 1.
- `reading_grade(text: str) -> float`: `0.39*(words/sentences) + 11.8*(syllables/words) - 15.59`. Sentences split on `.!?`. Returns `0.0` for empty text.
- `prose_text(item) -> str`: joins only the page's own prose fields. For Food: `why`, `spoiled_signs`, `how_to_store`, `common_mistake`, `freezing`. For LeftOut: `verdict_line`, `risk`, `next_time`. For Guide: `answer` plus section paragraphs and bullets.
- `prose_words(item) -> int`: the word count of `prose_text(item)`.
- `kind_of(item) -> Literal["food","leftout","guide"]`
- `similarity(a: str, b: str, k: int = 5) -> float`: Jaccard similarity of lowercase k-word shingles.
- `find_duplicates(items, threshold: float) -> list[tuple[str, str, float]]`: pairs of slugs above the threshold.
- In `config.py`: `MAX_GRADE = 8.0`, `SIMILARITY_MAX = 0.30`, `MIN_PROSE_WORDS = {"food": 220, "leftout": 120, "guide": 300}`. These are starting values. Tune them in Task 9 so that honest pages pass and copy-paste pages fail, and record any change in `LOG.md`.

- [ ] **Step 1: Write the failing tests:**
  - `test_syllables`: `cat`=1, `table`=2, `rice`=1, `refrigerate`=5.
  - `test_simple_text_low_grade`: `reading_grade("Put it in the fridge. Eat it soon.") < 3`.
  - `test_hard_text_high_grade`: a dense regulatory sentence scores > 12.
  - `test_identical_texts_similarity_1`
  - `test_one_word_swapped_is_duplicate`: two 220-word prose texts that differ only in the food name are found by `find_duplicates(..., 0.30)`.
  - `test_distinct_texts_pass`: the real-looking rice and eggs prose fixtures are not flagged.
  - `test_prose_text_excludes_name_and_sources`
- [ ] **Step 2:** Run `py -3 -m unittest tests.test_quality -v`. Expected: fail.
- [ ] **Step 3:** Implement `quality.py`.
- [ ] **Step 4:** Run the tests. Expected: 7 pass.
- [ ] **Step 5:** Commit: `"Add reading-level and duplicate-page gates"`.

### Task 3: Page rendering (answer-first templates)

**Files:** Create `kot/render.py`, `tests/test_render.py`.

**Interfaces:**
- Consumes the Task 1 dataclasses and `config`.
- Produces:
  - `url_for(kind: str, slug: str = "") -> str`, a site-relative path with a trailing slash: `food/cooked-rice/`, `left-out/rice-overnight/`, `guides/power-outage/`, `category/dairy/`, `""` (home), `about/`, `sources/`, `privacy/`.
  - `rel(from_path: str, to_path: str) -> str`, a relative link between two site paths (every link on the site is relative, so it works on github.io and on the future domain).
  - `render_food(food, ctx) -> str`, `render_leftout(lo, ctx) -> str`, `render_guide(g, ctx) -> str`, `render_hub(category, foods, ctx) -> str`, `render_home(ctx) -> str`, `render_static(kind: Literal["about","sources","privacy"], ctx) -> str`, `render_404(ctx) -> str`.
  - `ctx` is a `dict` built by Task 4 with keys `foods_by_slug`, `leftout_by_slug`, `guides_by_slug`, `all_sources`.
- Page shell (every page): `<!doctype html>`, `lang="en"`, title `"{question} | Keep or Toss"`, meta description, canonical `BASE_URL + path`, Open Graph title, description and image (`static/img/share/{slug}.png`, falling back to `default.png`), a link to `site.css`, a header with logo and site search (a text input that filters the hub list on home; no server), a breadcrumb, `<main>`, and a footer with About, Sources, Privacy and the Decoder link. The Cloudflare beacon script is included only when `ANALYTICS_TOKEN` is set.
- Food page body, in order, as the spec §5b sketch shows: `<h1>` with the question; then `<section class="answer">` with one row per place present in `storage`. Each row shows the place icon, the place name, and the span text (`"3–4 days"`, or `"Not recommended"` for `None`); the freezer row has the label `"best quality"`. Then the `why` line; then a button linking to `rel(path, "") + "?food={slug}#check"`. Then sections with question headings: "How can you tell it has gone bad?", "How should you store it?", "What mistake do most people make?", "Can you freeze it?". Then sources, the disclaimer, related links (foods and left-out pages that reference this food), and the aside "Reading labels? Try the free Ingredient Decoder" linking to `https://zazakariakarfr13-coder.github.io/supermarket-decoder/decoder/`.
- Structured data: a JSON-LD `FAQPage` holding the four section questions and their text, plus `BreadcrumbList`.

- [ ] **Step 1: Write the failing tests.** Parse the output with `html.parser`.
  - `test_food_answer_is_first_in_main`: the first element child of `<main>` after the `h1` has class `answer`.
  - `test_food_answer_shows_each_place`: fridge `3–4 days`, freezer `best quality`, counter `Not recommended`.
  - `test_temperatures_have_both_units`: rendered `40°F (4°C)` from a note containing `{temp:40}`. Add the helper `fmt_temp(f: int) -> str` and expand `{temp:N}` in all prose.
  - `test_canonical_and_title`
  - `test_disclaimer_present` on food, left-out and guide pages.
  - `test_relative_links_only`: no `href` starts with `/` or with `BASE_URL`, except the canonical, og: tags and external links.
  - `test_rel`: `rel("food/cooked-rice/", "category/leftovers/") == "../../category/leftovers/"` and `rel("", "food/x/") == "food/x/"`.
  - `test_leftout_verdict_first`: the first element after `h1` is `.answer` and contains the verdict word.
  - `test_no_analytics_without_token`
- [ ] **Step 2:** Run `py -3 -m unittest tests.test_render -v`. Expected: fail.
- [ ] **Step 3:** Implement `render.py` with f-strings. Escape all data with `html.escape`.
- [ ] **Step 4:** Run the tests. Expected: all pass.
- [ ] **Step 5:** Commit: `"Add answer-first page templates"`.

### Task 4: Build command, sitemap and checker data

**Files:** Create `kot/build.py`, `tests/test_build.py`, `data/__init__.py` (collect modules), and one sample food in `data/foods_leftovers.py` (cooked rice, fully written and sourced; this becomes real content).

**Interfaces — Produces:**
- `build(out_dir: Path, foods=None, leftout=None, guides=None) -> list[str]`. When no lists are passed, it uses `data.ALL_*`. It validates, renders every page into `out_dir/<path>/index.html`, copies `static/` to `out_dir/static/`, and writes `sitemap.xml` (every page, with `lastmod` set to the build date), `404.html` and `checker.json`. It returns the written site paths.
- `checker.json` holds a list of `{"slug","name","category","places":{place: {"min","max","unit","maxHours","basis":"safety"|"quality","note"}|null}}`. Basis is `quality` for the freezer and `safety` for everything else.
- CLI: `py -3 -m kot.build [out_dir]` (default `_site`). It prints the page count and exits non-zero on a validation error.

- [ ] **Step 1: Write the failing tests** (using a temp dir and two fixture foods):
  - `test_build_writes_pages`: `food/<slug>/index.html` exists for each food, plus home, the hubs of used categories only, about, sources, privacy and 404.
  - `test_sitemap_lists_every_page_with_base_url`
  - `test_checker_json_matches_data`: `maxHours` equals `Span.max_hours()`, freezer basis is `quality`, and a `None` place stays `null`.
  - `test_build_fails_on_invalid_data`
- [ ] **Step 2:** Run. Expected: fail.
- [ ] **Step 3:** Implement `build.py`.
- [ ] **Step 4:** Run the whole suite: `py -3 -m unittest discover -s tests -v`. Expected: all pass. Then run `py -3 -m kot.build` and expect `Built N pages`.
- [ ] **Step 5:** Commit: `"Add site build, sitemap and checker data"`.

### Task 5: Look and feel

**Files:** Create `static/site.css`, `static/favicon.svg`, an inline SVG logo in the `render.py` header, and the place icons (fridge, freezer, pantry, counter) as inline SVG.

- Palette tokens on `:root`, with a dark override under `@media (prefers-color-scheme: dark)`. The identity is fridge blue/mint, distinct from the Decoder's cream and green. Verdict tokens: keep green, use-today amber, toss red. Each must reach a contrast of at least 4.5:1 against its background in both themes.
- Mobile-first, with a 16px side gutter and no horizontal scroll at 375px. The answer box is large type (place and time at least 20px). The checker block has the anchor `id="check"`.
- System font stack (free, fast). No web-font download.

- [ ] **Step 1:** Write the CSS and icons, then rebuild with `py -3 -m kot.build`.
- [ ] **Step 2: Verify in the browser.** Serve `_site` with `py -3 -m http.server 8765 -d _site` (add it to `.claude/launch.json` as `keep-or-toss` and start it with `preview_start`). Check cooked rice at the mobile preset (375×812), in light and dark. Pass means the h1 and the whole answer box are visible without scrolling, with no horizontal scroll (`document.documentElement.scrollWidth <= 375`). Take screenshots as proof.
- [ ] **Step 3:** Commit: `"Add Keep or Toss visual identity"`.

### Task 6: "Is it still OK?" checker

**Files:** Create `static/checker.js` (an ES module), `tests/js/checker.test.mjs`. Modify `render.py` so the checker block (food select, place select, date input or "how many days ago", and a result area with `aria-live="polite"`) appears on home and on every food page, pre-filled from `?food=`.

**Interfaces — Produces (exported from `checker.js`):**
- `placesFor(food) -> string[]`: places whose value is not null.
- `verdict(food, place, ageHours) -> {verdict: "keep"|"use-today"|"toss"|null, reason: string}`, with these rules in order:
  1. `ageHours` missing, NaN or below 0 → `null` with reason `"Pick when it was opened or cooked."`
  2. The place is null or missing for the food → `"toss"` with reason `"Not recommended: store it in the fridge instead."` (if it has a fridge time) or `"Not recommended."`.
  3. Freezer: if `ageHours <= maxHours`, then `keep`. Otherwise `keep` with the reason containing `"safe while frozen; taste and texture fade"`.
  4. Places with `maxHours <= 24`: `use-today` while `ageHours <= maxHours` (reason: eat it or refrigerate it now); otherwise `toss`.
  5. Other places: `keep` if `ageHours <= maxHours - 24`; `use-today` if `ageHours <= maxHours`; otherwise `toss`.
- The result shows the icon, the word, the reason, and a link to the food page. The checker loads `checker.json` with `fetch` relative to the page.

- [ ] **Step 1: Write the failing tests** with `node:test` and `node:assert`, using fixture cooked rice (fridge 3–4 days, so 96h; freezer 1–2 months; counter 0–2 hours):
  - `day 1 fridge is keep`: 24h → keep.
  - `boundary day is use-today`: 80h → use-today, 96h → use-today.
  - `past max is toss`: 97h → toss.
  - `freezer past max keeps with quality note`: 2000h → keep, and the reason includes `taste and texture fade`.
  - `counter within 2h is use-today, after is toss`: 1h → use-today, 3h → toss.
  - `future or missing date gives no verdict`: -5 → null, NaN → null.
  - `places only lists stored places`: a fixture with `counter: null` → `placesFor` excludes counter, and `verdict(...,"counter",1)` → toss with "Not recommended".
- [ ] **Step 2:** Run `node --test tests/js/`. Expected: fail.
- [ ] **Step 3:** Implement `checker.js`, plus the form wiring (a pure `verdict`, with DOM code kept separate in `initChecker(root)`).
- [ ] **Step 4:** Run `node --test tests/js/`. Expected: 7 pass. Rebuild, then in the browser pick cooked rice, fridge, 5 days ago, and expect a ✕ TOSS result linking to the page. Check that it can be operated by keyboard only (Tab, arrows, Enter).
- [ ] **Step 5:** Commit: `"Add Is it still OK? checker"`.

### Task 7: Site check (blocks publishing)

**Files:** Create `scripts/check_site.py`, `tests/test_check_site.py`.

**Interfaces — Produces:** `check(site_dir: Path, items) -> list[str]`, which returns problem messages (an empty list means pass). The CLI `py -3 scripts/check_site.py _site` exits 1 if there are any problems.

Checks:
1. Every local `href`/`src` resolves to a file. Every `#anchor` exists.
2. Every page has a non-empty `<title>`, a meta description of 50–160 characters, a canonical and an `og:image`.
3. Every `<img>` has an `alt`, and every SVG icon carries `aria-hidden` or a `<title>`.
4. Food and left-out pages: `.answer` is the first element after `h1` in `main`.
5. `reading_grade(prose_text(item)) <= MAX_GRADE` for every item.
6. `prose_words(item) >= MIN_PROSE_WORDS[kind_of(item)]`.
7. `find_duplicates(all items, SIMILARITY_MAX)` is empty.
8. Every page in `_site` is in `sitemap.xml` and vice versa (404 excluded).

- [ ] **Step 1: Write the failing tests.** Build a temp site from fixtures, then break one thing per test: a broken link, a missing description, the answer not first, a grade 12 text, a thin page, a near-copy page, a page missing from the sitemap. Each test asserts that the message names the page and the problem. Add one test where a clean fixture site returns `[]`.
- [ ] **Step 2:** Run. Expected: fail.
- [ ] **Step 3:** Implement. Reuse `kot.quality`.
- [ ] **Step 4:** Run the whole suite. Expected: all pass.
- [ ] **Step 5:** Commit: `"Add site check with trap-guard and answer-first rules"`.

### Task 8: Deploy pipeline (no push yet)

**Files:** Create `.github/workflows/pages.yml`. Modify `README.md` (how to build, test and add a food).

- The workflow is based on the Decoder's `pages.yml` (same action versions, `concurrency: pages`), but its steps are: checkout, setup-python 3.12, `python -m unittest discover -s tests`, setup-node 26, `node --test tests/js/`, `python -m kot.build _site`, `python scripts/check_site.py _site`, configure-pages, upload `_site`, deploy.

- [ ] **Step 1:** Write the workflow. Run the same commands locally in that order, and expect each one to exit 0.
- [ ] **Step 2:** Commit: `"Add Pages deploy workflow"`.
- [ ] **Step 3: Owner gate.** Ask the owner for approval to create the public repo `keep-or-toss` and push. Do not proceed without a yes. If yes: `gh repo create zazakariakarfr13-coder/keep-or-toss --public --source . --push`, then set Pages source to "GitHub Actions" (`gh api -X POST repos/zazakariakarfr13-coder/keep-or-toss/pages -f build_type=workflow`). Watch the run with `gh run watch`; it must succeed. Open the live URL. Nothing is announced yet, because the site only has a few pages.

### Task 9: First content wave + owner review gate

**Files:** Create the `data/foods_*.py` modules, the first 10 entries of `data/leftout.py`, and `LOG.md` entries.

- [ ] **Step 1: Demand check.** In the built-in browser, for each candidate food, record Google's autocomplete for `how long does <food> last` and the "People also ask" questions in `LOG.md`. Pick the 60 foods with the clearest demand, across all categories (at least 4 per category).
- [ ] **Step 2: Sources.** For each food, look up the times on FoodSafety.gov/FoodKeeper (and on FSIS or FDA where relevant). Record the URL in `sources`. Where sources disagree, use the shorter time and mention it in `why` or a note.
- [ ] **Step 3: Write the first 10 foods**, mixed across categories, plus 3 left-out pages and the bridge guide ("Best before vs use by vs sell by"), all following the spec §5b writing rules. Run `py -3 -m kot.build` and `py -3 scripts/check_site.py _site`, and fix until there are 0 problems. If an honest, distinct page fails the similarity or minimum-words gate, adjust the threshold only with a reason logged in `LOG.md`.
- [ ] **Step 4: Owner review gate.** Show the owner the 10 food pages, the 3 left-out pages and the bridge page in the browser (screenshots), and make the changes they ask for. Do not write the remaining pages until the owner approves the voice and format.
- [ ] **Step 5:** Commit: `"Content wave 1: 10 foods, 3 left-out pages, bridge guide"`.

### Task 10: Remaining launch content

- [ ] **Step 1:** Write the remaining ~50 foods (to reach about 60), in batches of 10. After each batch, rebuild and run the check to 0 problems, then commit (`"Content: <categories> batch"`).
- [ ] **Step 2:** Write the left-out pages up to 10–15 total. Each verdict comes from FSIS's 2-hour rule (1 hour above `{temp:90}`) and the food-specific risk.
- [ ] **Step 3:** Write the 5 country-difference guides (eggs, butter, ketchup, bread, milk/UHT; swap in any topic with stronger demand from the Task 9 log) and the power-outage guide (USDA: fridge safe for 4 hours unopened; full freezer 48 hours, half full 24 hours; a list of foods to toss and keep).
- [ ] **Step 4:** Write `about` (who runs it, why, the sources policy), `sources` (built automatically from all cited sources) and `privacy` (no cookies; Cloudflare's cookie-free counts once enabled; the checker sends nothing anywhere).
- [ ] **Step 5:** Run the check to 0 problems, then commit.

### Task 11: Share and Pinterest images

**Files:** Create `scripts/make_images.py` (Pillow, run locally) and its output `static/img/share/<slug>.png` (1200×630) and `pins/<slug>.png` (1000×1500, not deployed: add `pins/` to the build's copy exclusions, or keep it outside `static/`).

- The image design is the answer box as a picture: the question, then the fridge, freezer and pantry rows with icons, in the Keep or Toss colours with the logo. Text is at least 48px on pins.
- `py -3 scripts/make_images.py` regenerates all images and skips any whose data hasn't changed (a hash of the storage and question goes in the filename sidecar `.hash`).
- `pins/pins.csv` columns: `slug, title, description, link`. The link is the exact page URL plus `?utm_source=pinterest&utm_medium=social&utm_campaign=launch`, never the homepage.

- [ ] **Step 1:** Write a unittest that `pin_link("cooked-rice")` is the food page URL with those UTM tags.
- [ ] **Step 2:** Implement the script. Run it, then view 3 pins and 3 share images for legibility.
- [ ] **Step 3:** Commit: `"Add share and Pinterest images"`.

### Task 12: Clarity tests (spec §12)

- [ ] **Step 1: Automatic** (tests 1–4): the check passes with 0 problems. Paste the output into `LOG.md`.
- [ ] **Step 2: First-screen** (test 5): at 375×812, screenshot 10 pages (6 foods, 2 left-out, 2 guides). Pass means the question and the full answer are visible without scrolling. Fix and repeat any failures.
- [ ] **Step 3: Checker** (test 6): run 10 real cases (at least one per verdict, one freezer past max, one on a range boundary). Pass means each verdict matches the food page's numbers and source. Log a table.
- [ ] **Step 4: Accessibility** (test 7): set CSS `filter: grayscale(1)` and check the verdicts are still distinguishable by icon and word; check dark mode; check the checker works by keyboard only.
- [ ] **Step 5: AI cold reader** (test 8). If the owner agrees to a subagent, give 10 page texts to a fresh reader with no other context, and ask for each page: what the answer is, what you would do now, and what this site is. Otherwise, Claude does it from the plain text alone. Rewrite any page that is answered wrongly.
- [ ] **Step 6: Human cold readers** (test 9). Give the owner a 5-page link list and the 3 questions to ask 2–3 people on a phone. Rewrite whatever confused anyone. Log the outcomes.
- [ ] **Step 7:** Commit: `"Clarity test results and fixes"`.

### Task 13: Launch

- [ ] **Step 1: Owner gate.** Ask for approval to push the launch content. If yes, push and watch the workflow until it succeeds.
- [ ] **Step 2:** On the live site, check 5 random pages and the checker (with screenshots).
- [ ] **Step 3: Root robots.** In `ADP Launch\root-site\robots.txt`, add `Sitemap: https://zazakariakarfr13-coder.github.io/keep-or-toss/sitemap.xml`. Commit, then push with owner approval.
- [ ] **Step 4: Owner-only steps.** Give the owner a checklist:
  - (a) Add a Google Search Console URL-prefix property for `BASE_URL`, verified via an HTML meta tag. Claude adds the tag in `config.GSC_TOKEN` and pushes it. Then submit `sitemap.xml`.
  - (b) Create a free Cloudflare account and add Web Analytics for the site. Give Claude the beacon token to put in `ANALYTICS_TOKEN`.
  - (c) Create a "Keep or Toss" Pinterest board.
- [ ] **Step 5: Pins.** Draft a 3-week pin schedule (1–2 a day, each to its exact page) as a list. Schedule it in Metricool only after the owner approves the list.
- [ ] **Step 6:** Update `LOG.md` (launch date, page count, check results) and the project memory, including the reminder to buy the domain, and the next wave: Ramadan pages live by early December 2026.
