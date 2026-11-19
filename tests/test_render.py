import unittest
from unittest import mock

from kot import config
from kot.render import (fmt_temp, make_ctx, rel, render_404, render_food, render_guide, render_home,
                        render_hub, render_leftout, render_static, url_for)
from kot.schema import Guide, Section, Source, Span
from tests.htmlutil import first_after_h1, parse
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
CTX = make_ctx([FOOD], [LO], [GUIDE])


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

    def test_escapes_data(self):
        html = render_food(make_food(why="<script>bad()</script>"), CTX)
        self.assertNotIn("<script>bad()", html)


if __name__ == "__main__":
    unittest.main()
