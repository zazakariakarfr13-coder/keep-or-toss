"""Answer-first HTML pages. Every internal link is relative so the site works on
github.io today and on a custom domain later."""
from __future__ import annotations

import json
import posixpath
import re
from html import escape

from kot import config
from kot.schema import Food, Guide, LeftOut, Span

PLACE_LABEL = {"fridge": "Fridge", "freezer": "Freezer", "pantry": "Pantry", "counter": "Counter"}

ICONS = {
    "fridge": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M5 9h14M8 5v2M8 12v4"/></svg>',
    "freezer": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v20M3.5 7l17 10M20.5 7l-17 10M9 3.5l3 2 3-2M9 20.5l3-2 3 2"/></svg>',
    "pantry": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h18M3 12h18M3 20h18"/><rect x="5" y="6" width="4" height="6"/><rect x="11" y="7" width="3" height="5"/><rect x="15" y="14" width="4" height="6"/></svg>',
    "counter": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}

VERDICT = {
    "toss": ("toss", "✕ TOSS"),
    "keep": ("keep", "✓ KEEP"),
    "depends": ("today", "⏱ IT DEPENDS"),
}

_TEMP = re.compile(r"\{temp:(-?\d+)\}")


# ---------- small helpers ----------

def url_for(kind: str, slug: str = "") -> str:
    prefix = {"food": "food", "leftout": "left-out", "guide": "guides", "category": "category"}
    if kind in prefix:
        return f"{prefix[kind]}/{slug}/"
    if kind == "home":
        return ""
    return f"{kind}/"


def rel(from_path: str, to_path: str) -> str:
    """Relative link between two site paths (directories end with '/')."""
    from_dir = from_path.rstrip("/") or "."
    target = to_path or "."
    r = posixpath.relpath(target, from_dir) if from_dir != "." else target
    if r == ".":
        r = "./"
    if (to_path == "" or to_path.endswith("/")) and not r.endswith("/"):
        r += "/"
    return "" if r == "./" and from_path == "" else r


def fmt_temp(f: int) -> str:
    return f"{f}°F ({round((f - 32) * 5 / 9)}°C)"


def expand(text: str) -> str:
    """Escape data, then expand {temp:N} markers."""
    return _TEMP.sub(lambda m: fmt_temp(int(m.group(1))), escape(text))


def _num(x: float) -> str:
    return str(int(x)) if float(x).is_integer() else str(x)


def span_text(s: Span | None) -> str:
    if s is None:
        return "Not recommended"
    unit = s.unit[:-1] if s.max == 1 else s.unit
    if s.min == 0:
        return f"up to {_num(s.max)} {unit}"
    if s.min == s.max:
        return f"{_num(s.max)} {unit}"
    return f"{_num(s.min)}–{_num(s.max)} {unit}"


def make_ctx(foods, leftout, guides, share_images=frozenset()) -> dict:
    sources = {}
    for item in [*foods, *leftout, *guides]:
        for s in item.sources:
            sources.setdefault(s.url, s)
    return {
        "foods_by_slug": {f.slug: f for f in foods},
        "leftout_by_slug": {lo.slug: lo for lo in leftout},
        "guides_by_slug": {g.slug: g for g in guides},
        "all_sources": sorted(sources.values(), key=lambda s: (s.publisher, s.title)),
        "share_images": set(share_images),
    }


def _path_of(slug: str, ctx: dict) -> tuple[str, str]:
    """(site path, label) for any slug."""
    if slug in ctx["foods_by_slug"]:
        f = ctx["foods_by_slug"][slug]
        return url_for("food", slug), f.name
    if slug in ctx["leftout_by_slug"]:
        lo = ctx["leftout_by_slug"][slug]
        return url_for("leftout", slug), lo.question
    g = ctx["guides_by_slug"][slug]
    return url_for("guide", slug), g.title


# ---------- page shell ----------

def shell(path: str, title: str, description: str, body: str, ctx: dict, *,
          crumbs=None, jsonld=None, image_slug: str | None = None, absolute: bool = False) -> str:
    def L(to: str) -> str:
        return config.BASE_URL + to if absolute else rel(path, to)

    page_title = f"{title} | {config.SITE_NAME}" if path else f"{config.SITE_NAME}: {title}"
    img = (f"static/img/share/{image_slug}.png" if image_slug in ctx.get("share_images", ())
           else "static/img/share/default.png")
    head = [
        '<!doctype html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title>{escape(page_title)}</title>',
        f'<meta name="description" content="{escape(description)}">',
        f'<link rel="canonical" href="{config.BASE_URL}{path}">',
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{escape(description)}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{config.BASE_URL}{path}">',
        f'<meta property="og:image" content="{config.BASE_URL}{img}">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#0f6e8c">',
        f'<link rel="icon" href="{L("static/favicon.svg")}" type="image/svg+xml">',
        f'<link rel="stylesheet" href="{L("static/site.css")}">',
    ]
    if config.GSC_TOKEN:
        head.append(f'<meta name="google-site-verification" content="{escape(config.GSC_TOKEN)}">')
    data = list(jsonld or [])
    if crumbs:
        data.append({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name, "item": config.BASE_URL + p}
                for i, (name, p) in enumerate(crumbs)
            ],
        })
    for d in data:
        head.append('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    if config.ANALYTICS_TOKEN:
        head.append('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                    f"data-cf-beacon='{{\"token\": \"{escape(config.ANALYTICS_TOKEN)}\"}}'></script>")
    head.append("</head>")

    crumb_html = ""
    if crumbs:
        items = [f'<a href="{L(p)}">{escape(n)}</a>' for n, p in crumbs[:-1]]
        items.append(f'<span aria-current="page">{escape(crumbs[-1][0])}</span>')
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(items) + "</nav>"

    header = (
        '<header class="site-header"><div class="wrap">'
        f'<a class="logo" href="{L("")}" aria-label="Keep or Toss home">'
        '<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="6" y="2" width="20" height="28" rx="4"/>'
        '<path d="M6 12h20M10 6v3M10 16v5"/><path class="tick" d="M14 21l3 3 6-7"/></svg>'
        '<span>Keep <em>or</em> Toss</span></a>'
        f'<a class="header-cta" href="{L("")}#check">Check a food</a>'
        "</div></header>"
    )
    cats = " · ".join(f'<a href="{L(url_for("category", c))}">{escape(n)}</a>' for c, n in config.CATEGORIES.items())
    footer = (
        '<footer class="site-footer"><div class="wrap">'
        f'<p class="cats">{cats}</p>'
        f'<p><a href="{L("about/")}">About</a> · <a href="{L("sources/")}">Sources</a> · '
        f'<a href="{L("privacy/")}">Privacy</a> · <a href="{config.DECODER_URL}">Free Ingredient Decoder</a></p>'
        f'<p class="small">{escape(config.DISCLAIMER)}</p>'
        "</div></footer>"
    )
    return "\n".join(head) + f"\n<body>\n{header}\n<div class=\"wrap\">{crumb_html}\n<main>\n{body}\n</main></div>\n{footer}\n</body>\n</html>\n"


def _sources_html(sources) -> str:
    items = "".join(f'<li><a href="{escape(s.url)}" rel="noopener">{escape(s.publisher)}: {escape(s.title)}</a></li>'
                    for s in sources)
    return f'<section class="sources"><h2>Sources</h2><ul>{items}</ul></section>'


def _disclaimer() -> str:
    return f'<p class="disclaimer">{escape(config.DISCLAIMER)}</p>'


def _related_html(path: str, links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    items = "".join(f'<li><a href="{rel(path, p)}">{escape(n)}</a></li>' for p, n in links)
    return f'<section class="related"><h2>Related</h2><ul>{items}</ul></section>'


def _list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{expand(i)}</li>" for i in items) + "</ul>"


# ---------- pages ----------

def render_food(food: Food, ctx: dict) -> str:
    path = url_for("food", food.slug)
    rows = []
    for place in config.PLACES:
        if place not in food.storage:
            continue
        s = food.storage[place]
        cls = "place" + (" not-rec" if s is None else "")
        tag = '<span class="tag">best quality</span>' if place == "freezer" and s is not None else ""
        note = f'<span class="note">{expand(s.note)}</span>' if s is not None and s.note else ""
        rows.append(f'<li class="{cls}" data-place="{place}">{ICONS[place]}'
                    f'<span class="place-name">{PLACE_LABEL[place]}</span>'
                    f'<span class="time">{span_text(s)}</span>{tag}{note}</li>')
    answer = f'<section class="answer" aria-label="How long it lasts"><ul class="times">{"".join(rows)}</ul></section>'

    links = [_path_of(r, ctx) for r in food.related]
    links += [(url_for("leftout", lo.slug), lo.question)
              for lo in ctx["leftout_by_slug"].values() if lo.food == food.slug]

    q_bad, q_store, q_mistake, q_freeze = ("How can you tell it has gone bad?", "How should you store it?",
                                           "What mistake do most people make?", "Can you freeze it?")
    body = "\n".join([
        f"<h1>{escape(food.question)}</h1>",
        answer,
        f'<p class="why">{expand(food.why)}</p>',
        f'<p class="cta"><a class="button" href="{rel(path, "")}?food={food.slug}#check">Check my {escape(food.name.lower())} →</a></p>',
        f"<section><h2>{q_bad}</h2>{_list(food.spoiled_signs)}</section>",
        f"<section><h2>{q_store}</h2>{_list(food.how_to_store)}</section>",
        f"<section><h2>{q_mistake}</h2><p>{expand(food.common_mistake)}</p></section>",
        f"<section><h2>{q_freeze}</h2><p>{expand(food.freezing)}</p></section>",
        _related_html(path, links),
        f'<aside class="bridge">Reading labels? Try the free <a href="{config.DECODER_URL}">Ingredient Decoder</a>.</aside>',
        _sources_html(food.sources),
        _disclaimer(),
    ])
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in [(food.question, "; ".join(f"{PLACE_LABEL[p]}: {span_text(s)}" for p, s in food.storage.items())),
                         (q_bad, " ".join(food.spoiled_signs)), (q_store, " ".join(food.how_to_store)),
                         (q_mistake, food.common_mistake), (q_freeze, food.freezing)]
        ],
    }
    faq_text = json.loads(_TEMP.sub(lambda m: fmt_temp(int(m.group(1))), json.dumps(faq, ensure_ascii=False)))
    crumbs = [("Home", ""), (config.CATEGORIES[food.category], url_for("category", food.category)), (food.name, path)]
    return shell(path, food.question, food.description, body, ctx, crumbs=crumbs, jsonld=[faq_text],
                 image_slug=food.slug)


def render_leftout(lo: LeftOut, ctx: dict) -> str:
    path = url_for("leftout", lo.slug)
    cls, word = VERDICT[lo.verdict]
    food = ctx["foods_by_slug"][lo.food]
    body = "\n".join([
        f"<h1>{escape(lo.question)}</h1>",
        f'<section class="answer verdict verdict-{cls}" aria-label="Verdict"><p class="verdict-word">{word}</p>'
        f'<p class="verdict-line">{expand(lo.verdict_line)}</p></section>',
        f"<section><h2>Why is it risky?</h2><p>{expand(lo.risk)}</p></section>",
        f"<section><h2>What should you do next time?</h2>{_list(lo.next_time)}</section>",
        f'<p class="cta"><a class="button" href="{rel(path, url_for("food", food.slug))}">How long does {escape(food.name.lower())} last? →</a></p>',
        _related_html(path, [_path_of(r, ctx) for r in lo.related]),
        _sources_html(lo.sources),
        _disclaimer(),
    ])
    crumbs = [("Home", ""), (config.CATEGORIES[food.category], url_for("category", food.category)), (lo.question, path)]
    return shell(path, lo.question, lo.description, body, ctx, crumbs=crumbs, image_slug=lo.slug)


def render_guide(g: Guide, ctx: dict) -> str:
    path = url_for("guide", g.slug)
    secs = []
    for s in g.sections:
        paras = "".join(f"<p>{expand(p)}</p>" for p in s.paragraphs)
        bullets = _list(s.bullets) if s.bullets else ""
        secs.append(f"<section><h2>{escape(s.heading)}</h2>{paras}{bullets}</section>")
    body = "\n".join([
        f"<h1>{escape(g.title)}</h1>",
        f'<section class="answer short-answer" aria-label="Short answer"><p>{expand(g.answer)}</p></section>',
        *secs,
        (f'<aside class="bridge">Want to read the rest of the label? Try the free '
         f'<a href="{config.DECODER_URL}">Ingredient Decoder</a>.</aside>' if g.kind == "bridge" else ""),
        _related_html(path, [_path_of(r, ctx) for r in g.related]),
        _sources_html(g.sources),
        _disclaimer(),
    ])
    return shell(path, g.title, g.description, body, ctx, crumbs=[("Home", ""), (g.title, path)], image_slug=g.slug)


def render_hub(category: str, foods: list[Food], ctx: dict) -> str:
    path = url_for("category", category)
    name = config.CATEGORIES[category]
    items = []
    for f in sorted(foods, key=lambda f: f.name):
        fridge = f.storage.get("fridge")
        hint = f' <span class="hint">fridge: {span_text(fridge)}</span>' if "fridge" in f.storage else ""
        items.append(f'<li><a href="{rel(path, url_for("food", f.slug))}">{escape(f.name)}</a>{hint}</li>')
    slugs = {f.slug for f in foods}
    los = [lo for lo in ctx["leftout_by_slug"].values() if lo.food in slugs]
    lo_html = ""
    if los:
        lo_html = "<section><h2>Left out too long?</h2><ul>" + "".join(
            f'<li><a href="{rel(path, url_for("leftout", lo.slug))}">{escape(lo.question)}</a></li>' for lo in los
        ) + "</ul></section>"
    body = (f"<h1>{escape(name)}: how long does it last?</h1>"
            f'<ul class="food-list">{"".join(items)}</ul>{lo_html}')
    desc = f"How long {name.lower()} last in the fridge, freezer and pantry, with clear keep-or-toss answers."
    return shell(path, f"{name}: how long does it last?", desc, body, ctx,
                 crumbs=[("Home", ""), (name, path)], image_slug=f"category-{category}")


def render_home(ctx: dict) -> str:
    foods = sorted(ctx["foods_by_slug"].values(), key=lambda f: f.name)
    used = [c for c in config.CATEGORIES if any(f.category == c for f in foods)]
    cats = "".join(f'<li><a href="{url_for("category", c)}">{escape(config.CATEGORIES[c])}</a></li>' for c in used)
    all_foods = "".join(f'<li data-name="{escape(f.name.lower())}"><a href="{url_for("food", f.slug)}">{escape(f.name)}</a></li>'
                        for f in foods)
    guides = "".join(f'<li><a href="{url_for("guide", g.slug)}">{escape(g.title)}</a></li>'
                     for g in ctx["guides_by_slug"].values())
    los = "".join(f'<li><a href="{url_for("leftout", lo.slug)}">{escape(lo.question)}</a></li>'
                  for lo in ctx["leftout_by_slug"].values())
    body = "\n".join([
        "<h1>Is it still OK to eat?</h1>",
        '<section class="answer checker" id="check" aria-label="Is it still OK? checker">'
        '<p class="lead">Pick a food, where you keep it, and when you opened or cooked it. '
        'Get a clear answer: keep it, use it today, or toss it.</p>'
        '<div class="checker-app" data-checker></div>'
        '<noscript><p>The checker needs JavaScript. Every food page below has the same answer in plain text.</p></noscript>'
        "</section>",
        f'<section><h2>Browse by type</h2><ul class="cat-grid">{cats}</ul></section>',
        (f"<section><h2>Left out too long?</h2><ul>{los}</ul></section>" if los else ""),
        (f"<section><h2>Guides</h2><ul>{guides}</ul></section>" if guides else ""),
        '<section><h2>Every food</h2><label class="search-label" for="food-search">Find a food</label>'
        '<input id="food-search" type="search" placeholder="e.g. rice, eggs, salsa" autocomplete="off">'
        f'<ul class="food-list" id="all-foods">{all_foods}</ul></section>',
        _disclaimer(),
        '<script type="module" src="static/checker.js"></script>',
    ])
    desc = "Is your food still safe to eat? Clear keep-or-toss answers for the fridge, freezer and pantry, from official food safety sources."
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": config.SITE_NAME, "url": config.BASE_URL}
    return shell("", "How long does food last?", desc, body, ctx, jsonld=[site], image_slug="default")


def render_static(kind: str, ctx: dict) -> str:
    path = url_for(kind)
    if kind == "about":
        title, desc = "About Keep or Toss", "Who runs Keep or Toss, why it exists, and where the storage times come from."
        body = ("<h1>About Keep or Toss</h1>"
                "<p>Keep or Toss answers one question fast: is this food still OK to eat? "
                "Every page puts the answer first, in plain words.</p>"
                "<h2>Where do the times come from?</h2>"
                "<p>Every time on this site comes from official food safety sources, mainly the USDA FoodKeeper, "
                "FoodSafety.gov, USDA FSIS and the FDA. Each page lists its sources. When sources disagree, we use the shorter, safer time.</p>"
                "<h2>Who makes it?</h2>"
                f"<p>Keep or Toss is a small independent project from the makers of the free "
                f'<a href="{config.DECODER_URL}">Ingredient Decoder</a>. It is not run by any government agency or food brand.</p>'
                f"<p>{escape(config.DISCLAIMER)}</p>")
    elif kind == "sources":
        title, desc = "Sources", "Every official food safety source used on Keep or Toss, in one list."
        items = "".join(f'<li><a href="{escape(s.url)}" rel="noopener">{escape(s.publisher)}: {escape(s.title)}</a></li>'
                        for s in ctx["all_sources"])
        body = ("<h1>Sources</h1><p>These are the official sources behind the storage times on this site.</p>"
                f"<ul>{items}</ul>")
    else:
        title, desc = "Privacy", "Keep or Toss uses no cookies and does not collect what you type into the checker."
        body = ("<h1>Privacy</h1>"
                "<p>Keep or Toss does not use cookies and does not ask for your name or email.</p>"
                "<p>The checker runs only in your browser. What you pick is never sent anywhere.</p>"
                "<p>We may count visits with Cloudflare Web Analytics, which does not use cookies "
                "and does not track you across other sites.</p>")
    return shell(path, title, desc, body, ctx, crumbs=[("Home", ""), (title, path)])


def render_404(ctx: dict) -> str:
    body = ("<h1>Page not found</h1><p>That page does not exist. "
            f'Try the <a href="{config.BASE_URL}#check">food checker</a> or the '
            f'<a href="{config.BASE_URL}">home page</a>.</p>')
    return shell("404.html", "Page not found", "This page does not exist on Keep or Toss.", body, ctx, absolute=True)
