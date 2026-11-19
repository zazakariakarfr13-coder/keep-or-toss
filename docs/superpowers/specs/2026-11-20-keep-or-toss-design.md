# Keep or Toss — design

Date: 2026-11-20 · Status: awaiting approval

## In one minute

- **What:** a free website that tells people whether their food is still safe to eat, and for how long it lasts in the fridge, freezer or cupboard.
- **Why:** the Decoder products have no visitors. This site exists to bring visitors from Google and Pinterest, then point some of them to the Decoder.
- **Launch:** about 80 pages, plus a "Is it still OK?" checker that gives a KEEP / USE TODAY / TOSS answer.
- **Cost:** $0. Domain later, when there's budget.
- **The rule that matters most:** the answer is the first thing every visitor sees, in plain words. Everything else on the page supports it.
- **Done means:** all of section 12 passes, the owner approves sample pages, and the site is live and submitted to Google.

## 1. Intent and why

Supermarket Decoder (Gumroad guide + free site) has products but no traffic: $0 / 0 sales in the 30 days to 19 Nov 2026. The bottleneck is distribution, not products.

**Keep or Toss** is a new, separate website that answers the food-storage questions people type into Google every day ("how long does cooked rice last in the fridge", "pizza left out overnight"). It earns search and Pinterest traffic on its own merits, and links back to the Decoder world through one natural bridge: the dates printed on labels (best before / use by / sell by).

The owner's brief: build it from scratch, make it great, take what worked on the Decoder site, fix what went wrong there, be creative, spend **$0**.

## 2. Goals, non-goals, anti-goals

**Goals**
- Launch with ~80 genuinely useful, indexable pages (see §5).
- Grow by 5–10 new pages a week after launch (the "upload schedule").
- Be the storage site people bookmark: a clear verdict, not a dense table.
- Measure from day one: know what Google indexes and where visitors come from.
- Send a share of visitors to the Decoder site / products via the date-label bridge.

**Non-goals (for now)**
- Custom domain (wanted, no budget — see §4). Email list. Paid tools of any kind.
- The halal additive checker (liked; parked as the next branch).
- Videos.

**Anti-goals — failure even if it "works"**
- **The scaled-content trap:** near-identical template pages ("X lasts 4 days" with everything else copy-pasted). Google penalises this. Every page must carry its own real substance.
- **Unsafe advice.** Food safety is a health topic: times must come from official sources, be conservative, and say "when in doubt, throw it out". Never contradict USDA/FDA guidance.
- **Renaming after launch** (the Decoder's `/Zakaria/` → `/supermarket-decoder/` mistake).
- **Decoration over substance** (the Decoder comic was redesigned ~6 times while the site has ~9 rankable articles).
- **Pins that land on the homepage** instead of the exact matching page.

## 3. Constraints

- Budget $0: GitHub Pages hosting, free analytics only, existing free Metricool for Pinterest.
- Owner works from Morocco; audience is US-first, English. Show °F and °C, US units with metric in brackets.
- Tooling available on this PC: Python (`py -3`), git, gh, Edge (headless rendering; Chrome is not installed), Node (portable). Git/gh may need full paths: `C:\Program Files\Git\cmd\git.exe`, `C:\Program Files\GitHub CLI\gh.exe`.
- GitHub account `zazakariakarfr13-coder`. The root repo `zazakariakarfr13-coder.github.io` owns `/robots.txt` for the whole github.io domain (currently lists only the Decoder sitemap).
- Never publish pins/posts or push without the owner's approval. Never put paid PDFs in a public repo.

## 4. Name and address

- **Name: Keep or Toss** (owner handed this choice to Claude; Claude's pick — it is the verdict people want and matches the checker tool).
- **Repo:** `keep-or-toss` → `https://zazakariakarfr13-coder.github.io/keep-or-toss/`. Final from day one; never renamed.
- **Custom domain later:** when budget allows (~$10–12/yr), add it in Pages settings; GitHub then redirects github.io URLs to the domain, so search trust carries over. Remind the owner each session until bought.
- Add `Sitemap: …/keep-or-toss/sitemap.xml` to the root repo's `robots.txt`.

## 5. Launch content (~80 pages)

| Family | Count | Example | What makes each page unique |
|---|---|---|---|
| Core food pages | ~60 | "How long does cooked rice last?" | Fridge/freezer/pantry times; spoilage signs specific to that food; best storage method; the common mistake; freezing/thawing notes; sources |
| "Left out" pages | 10–15 | "Rice left out overnight: keep or toss?" | One-screen verdict + the specific risk for that food (e.g. *Bacillus cereus* for rice) + what to do next time |
| Country-difference pages | ~5 | "Why Americans refrigerate eggs and Europeans don't" | Explainer with the real regulatory/processing reason, cited |
| Emergency guide | 1 | "Power outage: what to keep and what to toss" | Checklist by fridge/freezer and hours without power (USDA guidance) |
| Bridge page | 1 | "Best before vs use by vs sell by" | US vs EU date-label rules; links to the Decoder site |
| Hubs & essentials | ~6 | Home, category hubs (dairy, meat, leftovers, produce, pantry…), About, Sources, Privacy | Navigation + internal links |

**Food selection:** prefer foods where Google autocomplete / "People also ask" shows the question (free demand check, done in the browser during the build).

**Next waves (after launch, not in this design's build):** Ramadan meal-prep storage pages live by early December 2026 (Ramadan ≈ mid-Feb 2027); Eid al-Adha meat storage by ~March 2027; myth-busters; fridge shelf map; "what to cook first" ranker; printable fridge cheat sheet.

## 5b. What a visitor sees: every page, top to bottom

The "message" of a page is its answer. Someone who reads only the first screen on a phone must leave with the right answer. (The figures in the sketch only show the layout. Real figures come from the cited sources.)

```
┌───────────────────────────────┐
│ Keep or Toss        [search]  │
│ Home › Leftovers › Cooked rice│
│                               │
│ How long does cooked rice     │
│ last?                         │  ← the exact question people search
│ ┌───────────────────────────┐ │
│ │ FRIDGE   3–4 days         │ │  ← THE ANSWER, first screen,
│ │ FREEZER  1–2 months       │ │     big, with icons + words
│ │ COUNTER  max 2 hours      │ │     (not colour alone)
│ └───────────────────────────┘ │
│ One-line why: rice can carry  │
│ spores that survive cooking.  │
│ [ Check my rice → ]           │  ← opens the checker, pre-filled
├───────────────────────────────┤
│ How to tell it's gone bad     │  ← food-specific details
│ Store it the right way        │     (short sections, bullet points)
│ The mistake most people make  │
│ Freezing and reheating        │
│ Sources (USDA, FDA…)          │
│ Related: pasta · quinoa ·     │  ← keeps them on the site
│ "rice left out overnight"     │
│ Reading labels? Try the free  │  ← quiet bridge to the Decoder
│ Ingredient Decoder            │
└───────────────────────────────┘
```

**Writing rules for every page**
- Answer first, explanation after. No intro paragraph before the answer.
- Plain words, short sentences, aimed at a 12-year-old reading level (US grade 6–8). Technical terms only with a plain explanation next to them.
- Section headings phrased as the questions people ask.
- One idea per paragraph, at most 3 sentences per paragraph.
- Numbers are always shown with their unit and place ("3–4 days in the fridge"), never on their own.

## 6. The signature feature: "Is it still OK?" checker

On the homepage and every food page: pick a food → pick where it's stored (fridge / freezer / counter) → pick when it was opened or cooked → get a big **KEEP / USE TODAY / TOSS** verdict with the reason and a link to the full page. Plain JavaScript reading the same data file as the pages (exported to JSON at build time). No server, no tracking of what users type. Freezer times are labelled "quality" not "safety", as USDA does.

## 7. How it's built (approaches)

| Approach | Trade-off | Decision |
|---|---|---|
| **Data file + Python page generator + check script + GitHub Pages** (as the Decoder E-number pages) | Proven in this folder; free; pages stay consistent; content edits in one place | **Chosen** |
| Site builder (Wix, blog platform) | Costs money or locks content in; weak control over SEO | Rejected |
| Hand-written HTML pages | Slow for 80 pages; drifts out of sync | Rejected |

**Parts**
- `data/foods.py` (or JSON/YAML): one record per page with times, signs, storage, mistake, freezing, left-out verdict, sources, related foods. Prose fields are written per food, not filled from a sentence template.
- `scripts/build.py`: renders all pages, hubs, sitemap, checker JSON, share images.
- `scripts/check_site.py`: the Decoder checks (links, titles, descriptions, canonicals, images) **plus the trap-guard**: fail if a page's unique prose is below a minimum word count, or if any two pages are too similar (text-shingle similarity above a threshold). Runs in GitHub Actions before every deploy.
- `scripts/make_pins.py`: one vertical Pinterest image per page (storage chart look), each linking to its exact page with UTM tags.
- Measurement: Google Search Console (URL-prefix property + sitemap), plus a free, cookie-free analytics counter (Claude's call: Cloudflare Web Analytics or GoatCounter, whichever needs no paid plan and no cookie banner).
- SEO basics from day one: titles, descriptions, canonicals, structured data (FAQ/HowTo-style where honest), Open Graph share images, internal "related foods" links, breadcrumbs.

**Look:** same calm, clean, mobile-first feel as the Decoder site, but its own identity (its own palette and logo — e.g. a cool fridge blue/mint with traffic-light verdict colours) so it does not read as a copy. Light and dark mode. Verdict colours must stay readable for colour-blind users (icons + words, not colour alone).

## 8. Content accuracy

- Times from USDA FoodKeeper (public domain), FoodSafety.gov, USDA FSIS and FDA; cite on each page. Where sources disagree, use the more conservative figure and say so.
- A visible "general guidance, not a guarantee; when in doubt, throw it out" note.
- The owner reviews a sample of pages before launch.

## 9. Links to the Decoder world

- Bridge page (best before / use by) links to the Decoder site and the free Ingredient Decoder.
- Small, honest footer/aside mention on food pages ("Reading labels? Try the free Ingredient Decoder").
- No hard selling on storage pages. Later: a paid storage/meal-prep printable kit that pairs with the Real-Food Reset planner.

## 10. Claude's calls (owner may override)

- **Clarity tests (§12):** the reading-level target (grade 8 or below) and the cold-reader tests are Claude's calls, made in response to the owner asking that "everyone gets the message".
- **Who writes:** Claude researches and writes every page from the cited sources; the owner reviews ~10 sample pages (mix of families) before launch.
- **Analytics:** Cloudflare Web Analytics (free, no cookies, allowed on commercial sites; GoatCounter's free tier is for non-commercial sites, and this one links to products).
- **Pinterest:** a new "Keep or Toss" board on the existing Pinterest account, scheduled through the existing Metricool brand; nothing scheduled without approval.
- **Owner-only steps** (accounts and sign-ins Claude must not do): create the free Cloudflare account, verify the site in Google Search Console with the owner's Google account, create the Pinterest board, approve the push to GitHub and every pin.

## 12. Clarity tests: proving the message gets through

Claude runs these before launch, and again on every new batch of pages. Results go in the project log.

**Automatic (in `check_site.py`, which blocks publishing on failure)**
1. **Answer first:** on every food and left-out page, the answer box is the first content after the title.
2. **Reading level:** prose scores at US grade 8 or below (Flesch–Kincaid). Pages above that fail.
3. **Trap-guard:** minimum unique words per page, and no two pages too similar (see §7).
4. **Basics:** no broken links; every page has a title, description and share image; every image has a description for blind users.

**In the browser (Claude, with screenshots as proof)**
5. **First-screen test:** open a sample of pages at phone size (375 px wide). Pass = the question and the full answer are visible without scrolling.
6. **Checker test:** run 10 real cases through the checker (e.g. rice cooked 5 days ago, kept in the fridge). Pass = the verdict matches the food's page and its source every time.
7. **Accessibility:** verdicts still readable in greyscale and in dark mode; the checker works with keyboard only.

**Cold-reader test**
8. **AI cold reader:** a fresh reader who has never seen the project gets 10 pages and must answer, for each, three questions: what is the answer, what would you do now, and what is this site. Pass = it gets all three right on every page. Anything it gets wrong gets rewritten.
9. **Human cold readers (the real test):** the owner shows 5 pages on a phone to 2–3 people (family or friends, ideally one weak English reader) and asks the same three questions. Every page that confuses anyone gets rewritten before launch.

## 13. Left to the builder

Exact data format, similarity threshold and minimum word count (tune so honest pages pass and template copies fail), the 60 foods (driven by the demand check), palette and logo details, analytics provider choice between the two free options, page URL scheme (suggested `/food/cooked-rice/`, `/left-out/rice-overnight/`).
