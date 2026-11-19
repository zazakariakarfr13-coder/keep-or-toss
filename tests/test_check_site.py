import importlib.util
from dataclasses import replace
import tempfile
import unittest
from pathlib import Path

from data.foods_leftovers import FOODS
from kot.build import build
from tests.test_quality import TEMPLATE
from tests.test_schema import make_food

_spec = importlib.util.spec_from_file_location("check_site", Path(__file__).resolve().parent.parent / "scripts" / "check_site.py")
check_site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_site)
check = check_site.check

RICE = replace(FOODS[0], related=[])  # standalone fixture: no links to other foods


class CheckSiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Path(self.tmp.name) / "_site"
        build(self.site, [RICE], [], [])
        self.page = self.site / "food/cooked-rice/index.html"

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, old, new, page=None):
        p = page or self.page
        html = p.read_text(encoding="utf-8")
        self.assertIn(old, html)
        p.write_text(html.replace(old, new, 1), encoding="utf-8")

    def test_clean_site_passes(self):
        self.assertEqual(check(self.site, [RICE]), [])

    def test_broken_link(self):
        self.edit("</main>", '<a href="../nope/">x</a></main>')
        probs = check(self.site, [RICE])
        self.assertTrue(any("food/cooked-rice/" in p and "nope" in p for p in probs), probs)

    def test_broken_anchor(self):
        self.edit("</main>", '<a href="../../#missing">x</a></main>')
        self.assertTrue(any("#missing" in p for p in check(self.site, [RICE])))

    def test_missing_description(self):
        self.edit('<meta name="description"', '<meta name="x-description"')
        self.assertTrue(any("food/cooked-rice/" in p and "description" in p for p in check(self.site, [RICE])))

    def test_answer_not_first(self):
        self.edit("</h1>", "</h1><p>Intro first.</p>")
        self.assertTrue(any("food/cooked-rice/" in p and "answer" in p for p in check(self.site, [RICE])))

    def test_img_without_alt(self):
        self.edit("</main>", '<img src="../../static/favicon.svg"></main>')
        self.assertTrue(any("alt" in p for p in check(self.site, [RICE])))

    def test_hard_text_fails_grade(self):
        hard = make_food(why=("Notwithstanding applicable jurisdictional regulatory determinations, manufacturers "
                              "must substantiate microbiological stabilization methodologies comprehensively. ") * 20)
        self.assertTrue(any("cooked-rice" in p and "grade" in p for p in check(self.site, [hard])))

    def test_thin_page_fails(self):
        thin = make_food()
        self.assertTrue(any("cooked-rice" in p and "words" in p for p in check(self.site, [thin])))

    def test_near_copy_fails(self):
        a = make_food(slug="cooked-rice", why=TEMPLATE.format(f="cooked rice"))
        b = make_food(slug="cooked-pasta", why=TEMPLATE.format(f="cooked pasta"))
        self.assertTrue(any("cooked-rice" in p and "cooked-pasta" in p and "similar" in p
                            for p in check(self.site, [a, b])))

    def test_page_missing_from_sitemap(self):
        extra = self.site / "food/ghost/index.html"
        extra.parent.mkdir(parents=True)
        extra.write_text(self.page.read_text(encoding="utf-8"), encoding="utf-8")
        self.assertTrue(any("food/ghost/" in p and "sitemap" in p for p in check(self.site, [RICE])))


if __name__ == "__main__":
    unittest.main()
