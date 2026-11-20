import unittest
from unittest import mock

from kot import config
from kot.render import (fmt_temp, make_ctx, rel, render_404, render_food, render_guide, render_home,
                        render_hub, render_leftout, render_static, url_for)
from kot.schema import Guide, QuickFood, Section, Source, Span
from kot.htmltree import first_after_h1, parse
from tests.test_schema import make_food, make_leftout


def make_guide(**over):
    base = dict(slug="best-before-vs-use-by", kind="bridge", title="Best before vs use by",
                description="What the dates on food labels really mean, and which one is about safety.",
                answer="Use by is about safety. Best before is about taste.",
                sections=[Section("What does use by mean?", ["It is the last safe day."])],
                sources=[Source("FDA", "Date labels", "https://www.fda.gov/")], related=[])
    base.update(over)
    return Guide(**base)


FOOD = make_food(storage={"fridge": Span(3, 4, "days", "Keep at {temp:40} or colder."),
                          "freezer": Span(1, 2, "months"), "counter": None})
LO = make_leftout()
GUIDE = make_guide()
KETCHUP = QuickFood("ketchup", "Ketchup", "condiments", {"fridge": Span(6, 6, "months", "After opening.")}, "USDA FoodKeeper")
CTX = make_ctx([FOOD], [LO], [GUIDE], quick=[KETCHUP])


class UrlTests(unittest.TestCase):
    def test_url_for(self):
        self.assertEqual(url_for("food", "cooked-rice"), "food/cooked-rice/")
        self.assertEqual(url_for("leftout", "x"), "left-out/x/")
        self.assertEqual(url_for("guide", "x"), "guides/x/")
        self.assertEqual(url_for("category", "dairy"), "category/dairy/")
        self.assertEqual(url_for("home"), "")
        self.assertEqual(url_for("about"), "about/")

    def test_rel(self):
        self.assertEqual(rel("food/cooked-rice/", "category/leftovers/"), "../../category/leftovers/")
        self.assertEqual(rel("", "food/x/"), "food/x/")
        self.assertEqual(rel("food/x/", ""), "../../")
        self.assertEqual(rel("food/x/", "static/site.css"), "../../static/site.css")

    def test_fmt_temp(self):
        self.assertEqual(fmt_temp(40), "40°F (4°C)")
        self.assertEqual(fmt_temp(90), "90°F (32°C)")
        self.assertEqual(fmt_temp(0), "0°F (-18°C)")


class FoodPageTests(unittest.TestCase):
    def setUp(self):
        self.html = render_food(FOOD, CTX)
        self.root = parse(self.html)

    def test_food_answer_is_first_in_main(self):
        self.assertIn("answer", first_after_h1(self.root).classes)

    def test_food_answer_shows_each_place(self):
        text = first_after_h1(self.root).all_text()
        self.assertIn("3–4 days", text)
        self.assertIn("1–2 months", text)
        self.assertIn("best quality", text)
        self.assertIn("Not recommended", text)

    def test_temperatures_have_both_units(self):
        self.assertIn("40°F (4°C)", self.html)
        self.assertNotIn("{temp:", self.html)

    def test_canonical_and_title(self):
        self.assertIn(f'<link rel="canonical" href="{config.BASE_URL}food/cooked-rice/">', self.html)
        self.assertIn("<title>How long does cooked rice last? | Keep or Toss</title>", self.html)

    def test_question_headings(self):
        heads = [h.all_text() for h in self.root.find_all("h2")]
        for q in ["How can you tell it has gone bad?", "How should you store it?",
                  "What mistake do most people make?", "Can you freeze it?"]:
            self.assertIn(q, heads)

    def test_links_to_leftout_page_and_decoder(self):
        hrefs = [a.attrs.get("href") for a in self.root.find_all("a")]
        self.assertIn("../../left-out/rice-left-out-overnight/", hrefs)
        self.assertIn(config.DECODER_URL, hrefs)
        self.assertIn("../../?food=cooked-rice#check", hrefs)

    def test_relative_links_only(self):
        for n in self.root.iter():
            if n.tag in ("a", "link", "script", "img"):
                if n.tag == "link" and n.attrs.get("rel") == "canonical":
                    continue
                url = n.attrs.get("href") or n.attrs.get("src") or ""
                self.assertFalse(url.startswith("/"), url)
                self.assertFalse(url.startswith(config.BASE_URL), url)

    def test_no_analytics_without_token(self):
        self.assertNotIn("cloudflareinsights", self.html)

    def test_analytics_with_token(self):
        with mock.patch.object(config, "ANALYTICS_TOKEN", "abc123"):
            self.assertIn("cloudflareinsights", render_food(FOOD, CTX))


class OtherPageTests(unittest.TestCase):
    def test_disclaimer_present(self):
        for html in (render_food(FOOD, CTX), render_leftout(LO, CTX), render_guide(GUIDE, CTX)):
            self.assertIn(config.DISCLAIMER, html)

    def test_leftout_verdict_first(self):
        box = first_after_h1(parse(render_leftout(LO, CTX)))
        self.assertIn("answer", box.classes)
        self.assertIn("TOSS", box.all_text())

    def test_guide_answer_first(self):
        box = first_after_h1(parse(render_guide(GUIDE, CTX)))
        self.assertIn("answer", box.classes)

    def test_hub_lists_food(self):
        html = render_hub("leftovers", [FOOD], CTX)
        self.assertIn('href="../../food/cooked-rice/"', html)

    def test_home_static_404_render(self):
        self.assertIn('id="check"', render_home(CTX))
        self.assertIn("FoodKeeper", render_static("sources", CTX))
        for kind in ("about", "privacy"):
            self.assertIn("<h1>", render_static(kind, CTX))
        self.assertIn("<h1>", render_404(CTX))

    def test_home_loads_checker_module(self):
        self.assertIn('<script type="module" src="static/checker.js"></script>', render_home(CTX))

    def test_footer_skips_empty_categories(self):
        html = render_food(FOOD, CTX)
        self.assertIn('href="../../category/leftovers/"', html)
        self.assertNotIn("category/dairy/", html)

    def test_home_search_lists_quick_and_page_foods(self):
        html = render_home(CTX)
        self.assertIn('data-food="ketchup"', html)
        self.assertIn("fridge: 6 months", html)
        self.assertIn('href="food/cooked-rice/"', html)

    def test_home_has_clickable_examples(self):
        root = parse(render_home(CTX))
        chips = [a for a in root.find_all("a") if "chip" in a.classes]
        self.assertTrue(chips)
        self.assertTrue(all(a.attrs.get("data-food") for a in chips))
        self.assertTrue(all(a.attrs.get("href", "").startswith("?food=") for a in chips))

    def test_page_art_sits_after_the_answer(self):
        ctx = make_ctx([FOOD], [LO], [GUIDE], quick=[KETCHUP],
                       art={"cooked-rice": '<svg class="page-art"></svg>', "rice-left-out-overnight": '<svg class="page-art"></svg>'})
        for html in (render_food(FOOD, ctx), render_leftout(LO, ctx)):
            root = parse(html)
            self.assertIn("answer", first_after_h1(root).classes)
            figs = [n for n in root.iter() if n.tag == "figure" and "page-art-fig" in n.classes]
            self.assertEqual(len(figs), 1)
            self.assertEqual(figs[0].attrs.get("aria-hidden"), "true")

    def test_no_page_art_without_a_drawing(self):
        self.assertNotIn("page-art-fig", render_food(FOOD, CTX))

    def test_menu_on_every_page_lists_titles_and_subtitles(self):
        root = parse(render_guide(GUIDE, CTX))
        menus = [n for n in root.iter() if n.tag == "details" and "menu" in n.classes]
        self.assertEqual(len(menus), 1)
        menu = menus[0]
        self.assertIn("Menu", menu.find_all("summary")[0].all_text())
        text = menu.all_text()
        for heading in ("Check a food", "Food guides", "Leftovers & cooked food", "Left out too long?", "Guides", "About"):
            self.assertIn(heading, text)
        hrefs = [a.attrs.get("href") for a in menu.find_all("a")]
        for href in ("../../food/cooked-rice/", "../../left-out/rice-left-out-overnight/",
                     "../../about/", "../../sources/", "../../#check"):
            self.assertIn(href, hrefs)
        current = [a for a in menu.find_all("a") if a.attrs.get("aria-current") == "page"]
        self.assertEqual([a.attrs.get("href") for a in current], ["./"])

    def test_menu_links_are_relative_from_home(self):
        menu = [n for n in parse(render_home(CTX)).iter() if n.tag == "details" and "menu" in n.classes][0]
        self.assertIn("food/cooked-rice/", [a.attrs.get("href") for a in menu.find_all("a")])

    def test_home_search_covers_every_kind_of_page(self):
        root = parse(render_home(CTX))
        items = root.find_all("li")
        kinds = {li.attrs.get("data-type") for li in items if li.attrs.get("data-type")}
        self.assertTrue({"Food guide", "Quick answer", "Left out", "Guide", "Category", "Info"} <= kinds, kinds)
        hrefs = [a.attrs.get("href") for a in root.find_all("a")]
        self.assertIn("left-out/rice-left-out-overnight/", hrefs)
        self.assertIn("guides/best-before-vs-use-by/", hrefs)

    def test_home_search_comes_before_the_checker(self):
        main = parse(render_home(CTX)).find_all("main")[0]
        order = [(" ".join(k.classes), k.attrs.get("id")) for k in main.children]
        finder = next(i for i, (c, _) in enumerate(order) if "finder" in c)
        check = next(i for i, (_, i_d) in enumerate(order) if i_d == "check")
        self.assertLess(finder, check)

    def test_seasonal_guide_is_valid_and_labelled(self):
        from kot.schema import validate_all
        g = make_guide(slug="ramadan-meal-prep", kind="seasonal", title="Ramadan meal prep")
        validate_all([FOOD], [], [g])
        html = render_guide(g, make_ctx([FOOD], [], [g]))
        self.assertIn("answer", first_after_h1(parse(html)).classes)
        self.assertIn('data-type="Seasonal"', render_home(make_ctx([FOOD], [], [g])))

    def test_guide_section_headings_are_searchable(self):
        g = make_guide(sections=[Section("Can you freeze samosas?", ["Yes."])])
        html = render_home(make_ctx([FOOD], [], [g]))
        row = next(li for li in parse(html).find_all("li") if li.attrs.get("data-type") == "Guide")
        self.assertIn("samosas", row.attrs["data-name"])

    def test_escapes_data(self):
        html = render_food(make_food(why="<script>bad()</script>"), CTX)
        self.assertNotIn("<script>bad()", html)


if __name__ == "__main__":
    unittest.main()
