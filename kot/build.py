"""Build the whole site into a folder: `py -3 -m kot.build [out_dir]`."""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sys
from pathlib import Path

from kot import config, render
from kot.schema import validate_all

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"


def _write(out_dir: Path, path: str, html: str) -> None:
    target = out_dir / path / "index.html" if not path.endswith(".html") else out_dir / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def checker_data(foods, quick=()) -> list[dict]:
    pages = {f.slug for f in foods}
    out = []
    for f in sorted([*foods, *quick], key=lambda f: f.name.lower()):
        places = {}
        for place, s in f.storage.items():
            places[place] = None if s is None else {
                "min": s.min, "max": s.max, "unit": s.unit, "maxHours": s.max_hours(),
                "basis": "quality" if place == "freezer" else "safety",
                "note": render.expand_plain(s.note) if s.note else "",
            }
        out.append({"slug": f.slug, "name": f.name, "category": f.category, "places": places,
                    "page": f.slug in pages,
                    "source": "USDA and FDA sources listed on its page" if f.slug in pages else f.source})
    return out


def build(out_dir: Path, foods=None, leftout=None, guides=None, quick=None) -> list[str]:
    if foods is None and leftout is None and guides is None:
        import data
        foods, leftout, guides = data.ALL_FOODS, data.ALL_LEFTOUT, data.ALL_GUIDES
        quick = data.ALL_QUICK if quick is None else quick
    foods, leftout, guides, quick = foods or [], leftout or [], guides or [], quick or []
    validate_all(foods, leftout, guides, quick)

    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(STATIC, out_dir / "static")

    share = {p.stem for p in (STATIC / "img" / "share").glob("*.png")} if (STATIC / "img" / "share").is_dir() else set()
    art_dir = STATIC / "art"
    art = {f.stem: f.read_text(encoding="utf-8") for f in art_dir.glob("*.svg")} if art_dir.is_dir() else {}
    ctx = render.make_ctx(foods, leftout, guides, share, quick, art)

    pages: dict[str, str] = {"": render.render_home(ctx)}
    for f in foods:
        pages[render.url_for("food", f.slug)] = render.render_food(f, ctx)
    for lo in leftout:
        pages[render.url_for("leftout", lo.slug)] = render.render_leftout(lo, ctx)
    for g in guides:
        pages[render.url_for("guide", g.slug)] = render.render_guide(g, ctx)
    for cat in config.CATEGORIES:
        in_cat = [f for f in foods if f.category == cat]
        if in_cat:
            pages[render.url_for("category", cat)] = render.render_hub(cat, in_cat, ctx)
    for kind in ("about", "sources", "privacy"):
        pages[render.url_for(kind)] = render.render_static(kind, ctx)

    for path, html in pages.items():
        _write(out_dir, path, html)
    _write(out_dir, "404.html", render.render_404(ctx))

    today = dt.date.today().isoformat()
    urls = "".join(f"<url><loc>{config.BASE_URL}{p}</loc><lastmod>{today}</lastmod></url>" for p in pages)
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (out_dir / "checker.json").write_text(json.dumps(checker_data(foods, quick), ensure_ascii=False), encoding="utf-8")
    return list(pages)


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else ROOT / "_site"
    try:
        paths = build(out)
    except ValueError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        return 1
    print(f"Built {len(paths)} pages into {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
