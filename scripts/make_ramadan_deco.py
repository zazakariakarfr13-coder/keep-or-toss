"""Ramadan page decoration: string lights, three swaying lanterns (fanous), crescent sticker.

Usage: py -3 scripts/make_ramadan_deco.py   -> writes static/art/ramadan-meal-prep.svg
Decorative only (aria-hidden); every motion sits inside prefers-reduced-motion: no-preference.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INK, GOLD, GOLD_DARK, GLASS = "#1d1a2f", "#e0a92e", "#a8741a", "#ffd166"
BULBS = ["#ffd25e", "#ff8a5c", "#7fd1c7", "#ffd25e", "#f4a7b9"]

# the string is two quadratic curves: (-10,18) -> ctrl (200,80) -> (400,26) -> ctrl (600,80) -> (810,18)
CURVES = [((-10, 18), (200, 80), (400, 26)), ((400, 26), (600, 80), (810, 18))]


def point(x: float) -> tuple[float, float]:
    """y on the string at horizontal position x (solve the quadratic for t, then evaluate)."""
    (x0, y0), (cx, cy), (x1, y1) = CURVES[0] if x <= 400 else CURVES[1]
    lo, hi = 0.0, 1.0
    for _ in range(40):
        t = (lo + hi) / 2
        xt = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
        lo, hi = (t, hi) if xt < x else (lo, t)
    return x, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1


def lantern(x: float, drop: float, scale: float, cls: str) -> str:
    _, y = point(x)
    s = scale
    body = (
        f'<line x1="0" y1="0" x2="0" y2="{drop}" stroke="{GOLD_DARK}" stroke-width="2"/>'
        f'<g transform="translate(0 {drop}) scale({s})">'
        f'<circle cx="0" cy="5" r="5" fill="none" stroke="{GOLD}" stroke-width="2.5"/>'
        f'<path d="M-14 25 L0 9 L14 25Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<rect x="-18" y="25" width="36" height="7" rx="2" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>'
        f'<circle class="flick" cx="0" cy="60" r="34" fill="url(#glow)"/>'
        f'<path d="M-18 32 L18 32 L25 60 L18 88 L-18 88 L-25 60Z" fill="{GLASS}" fill-opacity=".85" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<path d="M-6 33 L-8 60 L-6 87 M6 33 L8 60 L6 87 M-24 60 L24 60" stroke="{GOLD_DARK}" stroke-width="2" fill="none"/>'
        f'<path d="M0 46 L4 56 L0 66 L-4 56Z" fill="#fff6d6"/>'
        f'<rect x="-18" y="88" width="36" height="7" rx="2" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>'
        f'<path d="M-10 95 L0 112 L10 95Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        f"</g>"
    )
    return f'<g transform="translate({x:.1f} {y:.1f})"><g class="sway {cls}">{body}</g></g>'


def bulbs() -> str:
    out = []
    for i, x in enumerate(range(30, 800, 44)):
        if any(abs(x - lx) < 26 for lx in (140, 400, 660)):
            continue
        _, y = point(x)
        color = BULBS[i % len(BULBS)]
        out.append(f'<g class="tw t{i % 3 + 1}"><circle cx="{x}" cy="{y + 9:.1f}" r="13" fill="url(#glow)"/>'
                   f'<circle cx="{x}" cy="{y + 9:.1f}" r="5.5" fill="{color}" stroke="{INK}" stroke-width="1.5"/></g>')
    return "".join(out)


def crescent() -> str:
    return (f'<g class="drift"><path d="M530 110 A30 30 0 1 0 530 170 A22 30 0 1 1 530 110Z" fill="{GOLD}" '
            f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M559 124 l3.5 7.5 8 1 -6 5.5 1.5 8 -7 -4 -7 4 1.5 -8 -6 -5.5 8 -1Z" fill="#fff3c4" '
            f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/></g>')


STYLE = """@media (prefers-reduced-motion: no-preference){
.sway{transform-box:fill-box;transform-origin:50% 0;animation:sway 5s ease-in-out infinite}
.sway.s2{animation-duration:6.2s;animation-delay:-2s}.sway.s3{animation-duration:5.6s;animation-delay:-4s}
@keyframes sway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
.tw{animation:tw 2.6s ease-in-out infinite}.tw.t2{animation-delay:-.9s}.tw.t3{animation-delay:-1.7s}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.4}}
.flick{animation:flick 3.2s ease-in-out infinite}
@keyframes flick{0%,100%{opacity:.85}45%{opacity:.55}60%{opacity:1}}
.drift{transform-box:fill-box;transform-origin:center;animation:drift 9s ease-in-out infinite}
@keyframes drift{50%{transform:translate(-5px,-7px) rotate(-5deg)}}
}"""


def svg() -> str:
    string = "M-10 18 Q200 80 400 26 Q600 80 810 18"
    return (
        '<svg class="page-deco-art" viewBox="0 0 800 200" preserveAspectRatio="xMidYMin slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
        f"<style>{STYLE}</style>"
        '<defs><radialGradient id="glow"><stop offset="0" stop-color="#ffd166" stop-opacity=".75"/>'
        '<stop offset="1" stop-color="#ffd166" stop-opacity="0"/></radialGradient></defs>'
        f'<path d="{string}" fill="none" style="stroke:var(--muted)" stroke-width="2" stroke-linecap="round"/>'
        + bulbs()
        + lantern(140, 34, 0.9, "s1")
        + lantern(400, 22, 1.0, "s2")
        + lantern(660, 40, 0.85, "s3")
        + crescent()
        + "</svg>"
    )


if __name__ == "__main__":
    out = ROOT / "static" / "art" / "ramadan-meal-prep.svg"
    out.write_text(svg(), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
