"""Site check. Blocks publishing when anything breaks the rules.

Usage: py -3 scripts/check_site.py _site
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urldefrag, urlsplit

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kot import config  # noqa: E402
from kot.htmltree import first_after_h1, parse  # noqa: E402
from kot.quality import find_duplicates, kind_of, prose_text, prose_words, reading_grade  # noqa: E402


def _site_path(site: Path, file: Path) -> str:
    rel = file.relative_to(site).as_posix()
    return rel[: -len("index.html")] if rel.endswith("index.html") else rel


def _resolve(site: Path, file: Path, url: str) -> Path | None:
    """Local file a relative URL points to, or None for external/absolute URLs."""
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or url.startswith(("mailto:", "#")):
        return None
    target = (file.parent / parts.path).resolve() if parts.path else file
    if parts.path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def check_pages(site: Path) -> list[str]:
    problems: list[str] = []
    files = sorted(site.rglob("*.html"))
    trees = {f.resolve(): parse(f.read_text(encoding="utf-8")) for f in files}
    ids = {f: {n.attrs.get("id") for n in t.iter() if n.attrs.get("id")} for f, t in trees.items()}

    for f in files:
        tree = trees[f.resolve()]
        page = _site_path(site, f)
        label = page or "(home)"

        # 1. links and anchors
        for n in tree.iter():
            url = None
            if n.tag == "a" or (n.tag == "link" and n.attrs.get("rel") not in ("canonical",)):
                url = n.attrs.get("href")
            elif n.tag in ("script", "img"):
                url = n.attrs.get("src")
            if not url:
                continue
            path_part, frag = urldefrag(url)
            if url.startswith("#"):
                if frag and frag not in ids[f.resolve()]:
                    problems.append(f"{label}: anchor #{frag} not found")
                continue
            target = _resolve(site, f, path_part)
            if target is None:
                continue
            if not target.is_file():
                problems.append(f"{label}: broken link {url}")
            elif frag and target.suffix == ".html" and frag not in ids.get(target.resolve(), set()):
                problems.append(f"{label}: anchor #{frag} not found in {url}")

        # 2. metadata
        title = "".join(t.all_text() for t in tree.find_all("title")).strip()
        if not title:
            problems.append(f"{label}: missing <title>")
        metas = tree.find_all("meta")
        desc = next((m.attrs.get("content", "") for m in metas if m.attrs.get("name") == "description"), None)
        if desc is None:
            problems.append(f"{label}: missing meta description")
        elif not 50 <= len(desc) <= 160:
            problems.append(f"{label}: meta description is {len(desc)} characters (needs 50-160)")
        if not any(n.attrs.get("rel") == "canonical" for n in tree.find_all("link")):
            problems.append(f"{label}: missing canonical link")
        if not any(m.attrs.get("property") == "og:image" for m in metas):
            problems.append(f"{label}: missing og:image")

        # 3. images and icons
        for img in tree.find_all("img"):
            if "alt" not in img.attrs:
                problems.append(f"{label}: image {img.attrs.get('src')} has no alt text")
        for svg in tree.find_all("svg"):
            if svg.attrs.get("aria-hidden") != "true" and not svg.find_all("title"):
                problems.append(f"{label}: svg icon needs aria-hidden or a <title>")

        # 4. answer first
        if page.startswith(("food/", "left-out/")):
            first = first_after_h1(tree)
            if first is None or "answer" not in first.classes:
                problems.append(f"{label}: the answer box must come right after the h1")

    # 8. sitemap <-> pages
    sm = site / "sitemap.xml"
    if not sm.is_file():
        problems.append("sitemap.xml is missing")
    else:
        text = sm.read_text(encoding="utf-8")
        listed = {loc[len(config.BASE_URL):] for loc in
                  (chunk.split("</loc>")[0] for chunk in text.split("<loc>")[1:])}
        pages = {_site_path(site, f) for f in files if f.name != "404.html"}
        for p in sorted(pages - listed):
            problems.append(f"{p or '(home)'}: page is not in the sitemap")
        for p in sorted(listed - pages):
            problems.append(f"{p or '(home)'}: in the sitemap but the page does not exist")
    return problems


def check_items(items) -> list[str]:
    problems = []
    for item in items:
        grade = reading_grade(prose_text(item))
        if grade > config.MAX_GRADE:
            problems.append(f"{item.slug}: reading grade {grade:.1f} is above {config.MAX_GRADE}")
        words, need = prose_words(item), config.MIN_PROSE_WORDS[kind_of(item)]
        if words < need:
            problems.append(f"{item.slug}: only {words} words of its own (needs {need})")
    for a, b, s in find_duplicates(items, config.SIMILARITY_MAX):
        problems.append(f"{a} and {b}: too similar ({s:.2f} > {config.SIMILARITY_MAX})")
    return problems


def check(site_dir: Path, items) -> list[str]:
    return check_pages(Path(site_dir)) + check_items(items)


def main(argv: list[str]) -> int:
    import data
    site = Path(argv[1]) if len(argv) > 1 else ROOT / "_site"
    items = [*data.ALL_FOODS, *data.ALL_LEFTOUT, *data.ALL_GUIDES]
    problems = check(site, items)
    for p in problems:
        print(f"PROBLEM: {p}")
    print(f"Checked {len(list(site.rglob('*.html')))} pages and {len(items)} items: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
