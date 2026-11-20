"""Keep or Toss Pinterest pins: risograph-style food characters, one big answer, few words.

Usage: py -3 scripts/make_pins.py            (renders every pin into pins/)
       py -3 scripts/make_pins.py eggs pizza (renders only those)
Each pin links to its exact page (never the homepage). Rendered with headless Edge.
"""
from __future__ import annotations

import csv
import random
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kot import config  # noqa: E402

OUT = ROOT / "pins"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
W, H = 1000, 1500

INK, CREAM, PAPER = "#1d1a2f", "#f6eedd", "#fffaf0"
RED, MUSTARD, CORAL = "#d83a2e", "#f3b33d", "#ef6a4c"
GREEN = "#2f8f5b"


def pin_link(path: str) -> str:
    return f"{config.BASE_URL}{path}?utm_source=pinterest&utm_medium=social&utm_campaign=launch"


@dataclass
class Pin:
    slug: str
    path: str               # site path the pin links to
    question: str           # headline, a few words
    answer: str             # the big stamp
    sub: str                # one short line
    bg: str
    text: str
    shadow: str             # misprint colour behind the headline and art
    stamp_bg: str
    stamp_fg: str
    art: str                # SVG body (1000 x 800 box)
    q_size: int = 112
    a_size: int = 150
    title: str = ""
    description: str = ""


# ---------------------------------------------------------------- SVG helpers
def defs(shadow: str) -> str:
    return f"""<defs>
<pattern id="hatch" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
  <line x1="0" y1="0" x2="0" y2="11" stroke="{INK}" stroke-width="2.6" opacity=".5"/></pattern>
<pattern id="dots" width="13" height="13" patternUnits="userSpaceOnUse">
  <circle cx="6.5" cy="6.5" r="2.4" fill="{INK}" opacity=".32"/></pattern>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7"/>
  <feDisplacementMap in="SourceGraphic" scale="6"/></filter>
<filter id="riso" x="-15%" y="-15%" width="140%" height="140%">
  <feOffset in="SourceAlpha" dx="13" dy="13" result="o"/><feFlood flood-color="{shadow}"/>
  <feComposite in2="o" operator="in" result="s"/>
  <feMerge><feMergeNode in="s"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


S = f'stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'


def face(x, y, mood="happy", s=1.0, color=INK):
    """A tiny expressive face centred on (x, y)."""
    e = 13 * s
    dx = 34 * s
    if mood == "sleep":
        eyes = (f'<path d="M{x-dx-e} {y} q{e} {e} {2*e} 0" fill="none" stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>'
                f'<path d="M{x+dx-e} {y} q{e} {e} {2*e} 0" fill="none" stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>')
        mouth = f'<ellipse cx="{x}" cy="{y+34*s}" rx="{9*s}" ry="{11*s}" fill="{color}"/>'
    elif mood == "worried":
        eyes = (f'<circle cx="{x-dx}" cy="{y}" r="{e}" fill="{color}"/><circle cx="{x+dx}" cy="{y}" r="{e}" fill="{color}"/>'
                f'<path d="M{x-dx-16*s} {y-28*s} l{26*s} {8*s}M{x+dx+16*s} {y-28*s} l{-26*s} {8*s}" stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>')
        mouth = f'<path d="M{x-22*s} {y+40*s} q{11*s} {-14*s} {22*s} 0 q{11*s} {14*s} {22*s} 0" fill="none" stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>'
    elif mood == "shock":
        eyes = (f'<circle cx="{x-dx}" cy="{y}" r="{e*1.35}" fill="#fff" stroke="{color}" stroke-width="{5*s}"/><circle cx="{x-dx}" cy="{y+3*s}" r="{e*.6}" fill="{color}"/>'
                f'<circle cx="{x+dx}" cy="{y}" r="{e*1.35}" fill="#fff" stroke="{color}" stroke-width="{5*s}"/><circle cx="{x+dx}" cy="{y+3*s}" r="{e*.6}" fill="{color}"/>')
        mouth = f'<ellipse cx="{x}" cy="{y+42*s}" rx="{12*s}" ry="{16*s}" fill="{color}"/>'
    elif mood == "cool":
        eyes = (f'<path d="M{x-dx-24*s} {y-10*s} h{48*s} v{12*s} q{-24*s} {22*s} {-48*s} 0 z M{x+dx-24*s} {y-10*s} h{48*s} v{12*s} q{-24*s} {22*s} {-48*s} 0 z" fill="{color}"/>'
                f'<path d="M{x-dx+24*s} {y-6*s} h{2*dx-48*s}" stroke="{color}" stroke-width="{5*s}"/>')
        mouth = f'<path d="M{x-24*s} {y+34*s} q{24*s} {20*s} {48*s} -4" fill="none" stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>'
    else:
        eyes = f'<circle cx="{x-dx}" cy="{y}" r="{e}" fill="{color}"/><circle cx="{x+dx}" cy="{y}" r="{e}" fill="{color}"/>'
        mouth = f'<path d="M{x-24*s} {y+28*s} q{24*s} {26*s} {48*s} 0" fill="none" stroke="{color}" stroke-width="{6*s}" stroke-linecap="round"/>'
    cheeks = f'<circle cx="{x-dx-22*s}" cy="{y+22*s}" r="{10*s}" fill="{CORAL}" opacity=".55"/><circle cx="{x+dx+22*s}" cy="{y+22*s}" r="{10*s}" fill="{CORAL}" opacity=".55"/>'
    return eyes + mouth + (cheeks if mood in ("happy", "cool") else "")


def star(x, y, r, color):
    return (f'<path d="M{x} {y-r} Q{x+r*.18} {y-r*.18} {x+r} {y} Q{x+r*.18} {y+r*.18} {x} {y+r} '
            f'Q{x-r*.18} {y+r*.18} {x-r} {y} Q{x-r*.18} {y-r*.18} {x} {y-r}Z" fill="{color}"/>')


def moon(x, y, r, bg):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}"/><circle cx="{x+r*.42}" cy="{y-r*.3}" r="{r*.92}" fill="{bg}"/>'


def clock(x, y, r, hour=3):
    import math
    a = math.radians(hour * 30 - 90)
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}" {S}/>'
            + "".join(f'<circle cx="{x + (r-18)*math.cos(math.radians(i*30))}" cy="{y + (r-18)*math.sin(math.radians(i*30))}" r="4" fill="{INK}"/>' for i in range(12))
            + f'<path d="M{x} {y} L{x + r*.45*math.cos(a)} {y + r*.45*math.sin(a)} M{x} {y} L{x} {y - r*.7}" {S}/>')


def grains(x0, x1, base, peak, n, seed):
    """Rice grains inside a dome drawn as Q(x0,base)-(mid,peak_ctrl)-(x1,base); `peak` is the control y."""
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        t = rnd.uniform(0.08, 0.92)
        x = x0 + (x1 - x0) * t
        top = base * (1 - t) ** 2 + 2 * peak * t * (1 - t) + base * t * t
        if top + 22 > base - 14:
            continue
        y = rnd.uniform(top + 22, base - 14)
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="15" ry="7" transform="rotate({rnd.uniform(-70, 70):.0f} {x:.0f} {y:.0f})" fill="#fff" stroke="{INK}" stroke-width="3"/>')
    return "".join(out)


def art(shadow: str, body: str, backdrop: str = "") -> str:
    return (f'<svg viewBox="0 0 1000 800" width="1000" height="800" xmlns="http://www.w3.org/2000/svg">{defs(shadow)}'
            f'{backdrop}<g filter="url(#rough)"><g filter="url(#riso)">{body}</g></g></svg>')


# ---------------------------------------------------------------- the ten pieces
def rice_art(bg):
    back = (f'<g class="bob">{moon(840, 120, 72, bg)}</g><g class="tw">' + star(130, 110, 22, CREAM) + star(220, 60, 12, CREAM)
            + star(720, 70, 14, CREAM) + star(900, 300, 16, CREAM) + '</g>')
    body = (f'<g class="breathe"><path d="M240 440 Q500 160 760 440Z" fill="#fff" {S}/>'
            + grains(240, 760, 440, 160, 34, 11)
            + f'<path d="M190 440 L810 440 Q800 650 610 705 L390 705 Q200 650 190 440Z" fill="{CORAL}" {S}/>'
            + f'<path d="M660 440 L810 440 Q800 650 610 705 Q720 610 660 440Z" fill="url(#hatch)"/>'
            + f'<path d="M190 470 L810 470" stroke="{INK}" stroke-width="5" stroke-dasharray="2 22" stroke-linecap="round"/>'
            + f'<path d="M420 705 L580 705 L565 745 L435 745Z" fill="{CORAL}" {S}/>'
            + face(500, 560, "sleep", 1.25) + '</g>'
            + f'<text class="z1" x="235" y="330" font-family="Anton" font-size="96" fill="{CREAM}">Z</text>'
            + f'<text class="z2" x="170" y="245" font-family="Anton" font-size="62" fill="{CREAM}">z</text>')
    return art("#0e1430", body, back)


def pizza_art(bg):
    back = clock(835, 130, 85, 3)
    body = (f'<path d="M500 770 L215 260 Q500 170 785 260Z" fill="#f9cf4f" {S}/>'
            f'<path d="M560 660 L500 770 L440 660 Q500 700 560 660Z" fill="url(#hatch)"/>'
            f'<path d="M215 260 Q500 170 785 260 L805 205 Q500 100 195 205Z" fill="#d98b3a" {S}/>'
            f'<path d="M260 210 q20 -10 40 0 M420 165 q20 -10 40 0 M600 168 q20 -10 40 0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED}" {S}/><circle cx="{x}" cy="{y}" r="{r-8}" fill="url(#dots)"/>'
                      for x, y, r in [(360, 290, 42), (630, 300, 46), (520, 470, 38), (440, 600, 30)])
            + f'<path d="M262 345 q-6 50 10 70 q14 -20 4 -70Z M735 330 q8 45 -8 66 q-14 -18 -2 -66Z" fill="#f9cf4f" {S}/>'
            + face(510, 365, "shock", 1.1))
    return art("#0b4a49", body, back)


def eggs_art(bg):
    back = star(140, 120, 40, "#fff") + star(860, 90, 26, "#fff") + star(900, 230, 15, "#fff")
    eggs = ""
    for x, mood in [(290, "happy"), (500, "cool"), (710, "happy")]:
        eggs += (f'<ellipse cx="{x}" cy="380" rx="92" ry="122" fill="{PAPER}" {S}/>'
                 f'<path d="M{x+40} 270 Q{x+110} 360 {x+70} 470 Q{x+110} 380 {x+40} 270Z" fill="url(#hatch)"/>'
                 + face(x, 380, mood, .95))
    body = (f'<ellipse cx="380" cy="300" rx="70" ry="92" fill="#f1e6d0" {S}/><ellipse cx="620" cy="300" rx="70" ry="92" fill="#f1e6d0" {S}/>'
            + eggs
            + f'<path d="M150 470 Q205 440 260 470 Q315 440 370 470 Q425 440 480 470 Q535 440 590 470 Q645 440 700 470 Q755 440 810 470 Q840 455 860 470 L805 700 L195 700Z" fill="#cbb08a" {S}/>'
            + f'<path d="M200 540 L800 540 M215 620 L785 620" stroke="{INK}" stroke-width="5" stroke-dasharray="3 20" stroke-linecap="round"/>'
            + f'<path d="M640 470 L860 470 L805 700 L700 700Z" fill="url(#hatch)"/>')
    return art("#2d5f86", body, back)


def chicken_art(bg):
    back = (f'<g transform="rotate(-6 210 230)"><rect x="110" y="120" width="210" height="220" rx="16" fill="{PAPER}" {S}/>'
            f'<rect x="110" y="120" width="210" height="62" rx="16" fill="{RED}" {S}/>'
            f'<text x="215" y="300" font-family="Anton" font-size="120" text-anchor="middle" fill="{INK}">2</text>'
            f'<circle cx="160" cy="120" r="10" fill="{INK}"/><circle cx="270" cy="120" r="10" fill="{INK}"/></g>')
    body = (f'<path d="M455 520 L285 690" stroke="{INK}" stroke-width="86" stroke-linecap="round"/>'
            f'<path d="M455 520 L285 690" stroke="{PAPER}" stroke-width="62" stroke-linecap="round"/>'
            f'<circle cx="245" cy="690" r="44" fill="{PAPER}" {S}/><circle cx="290" cy="738" r="44" fill="{PAPER}" {S}/>'
            f'<ellipse cx="610" cy="390" rx="235" ry="170" transform="rotate(-32 610 390)" fill="#f5a7b3" {S}/>'
            f'<path d="M700 220 Q860 330 760 520 Q820 360 700 220Z" fill="url(#hatch)"/>'
            f'<ellipse cx="610" cy="390" rx="235" ry="170" transform="rotate(-32 610 390)" fill="url(#dots)" opacity=".5"/>'
            + face(600, 380, "shock", 1.2)
            + f'<path d="M760 300 q14 -26 0 -46 q-16 22 0 46Z" fill="#7cc4f2" stroke="{INK}" stroke-width="4"/>')
    return art("#1f6b55", body, back)


def butter_art(bg):
    import math
    rays = "".join(f'<path d="M{170 + 95*math.cos(math.radians(a))} {150 + 95*math.sin(math.radians(a))} L{170 + 130*math.cos(math.radians(a))} {150 + 130*math.sin(math.radians(a))}" stroke="{MUSTARD}" stroke-width="12" stroke-linecap="round"/>'
                   for a in range(0, 360, 30))
    back = f'<circle cx="170" cy="150" r="72" fill="{MUSTARD}"/>' + rays
    body = (f'<ellipse cx="500" cy="660" rx="350" ry="78" fill="{PAPER}" {S}/>'
            f'<ellipse cx="500" cy="648" rx="270" ry="48" fill="none" stroke="{INK}" stroke-width="4" opacity=".5"/>'
            f'<path d="M290 470 L660 470 L660 625 L290 625Z" fill="#f8d66d" {S}/>'
            f'<path d="M290 470 L380 395 L750 395 L660 470Z" fill="#fde9a6" {S}/>'
            f'<path d="M660 470 L750 395 L750 550 L660 625Z" fill="#e7b947" {S}/>'
            f'<path d="M660 470 L750 395 L750 550 L660 625Z" fill="url(#hatch)"/>'
            f'<path d="M340 625 q8 40 22 0 M560 625 q10 52 26 0" fill="#f8d66d" {S}/>'
            f'<path d="M560 420 L760 220 L800 250 L620 440Z" fill="#dfe5ea" {S}/>'
            f'<path d="M760 220 L840 140 L880 175 L800 250Z" fill="{INK}"/>'
            + face(475, 540, "happy", 1.1))
    return art("#9c3a24", body, back)


def avocado_art(bg):
    def pear(cx, y0, s=1.0):
        return (f"M{cx} {y0} C{cx+110*s} {y0} {cx+120*s} {y0+150*s} {cx+150*s} {y0+260*s} "
                f"C{cx+190*s} {y0+420*s} {cx+60*s} {y0+470*s} {cx} {y0+470*s} "
                f"C{cx-60*s} {y0+470*s} {cx-190*s} {y0+420*s} {cx-150*s} {y0+260*s} "
                f"C{cx-120*s} {y0+150*s} {cx-110*s} {y0} {cx} {y0}Z")
    halves = ""
    for cx, rot, pit, mood in [(330, -10, True, "happy"), (680, 10, False, "cool")]:
        halves += (f'<g transform="rotate({rot} {cx} 420)">'
                   f'<path d="{pear(cx, 170, 1.0)}" fill="#2f5d34" {S}/>'
                   f'<path d="{pear(cx, 200, .86)}" transform="translate(0 6)" fill="#c6df74" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="{pear(cx, 250, .6)}" transform="translate(0 30)" fill="#eef4ae"/>')
        halves += (f'<circle cx="{cx}" cy="500" r="78" fill="#7a4a2a" {S}/><circle cx="{cx-24}" cy="472" r="18" fill="#fff" opacity=".45"/>'
                   if pit else f'<circle cx="{cx}" cy="500" r="72" fill="#e3ec9a" stroke="{INK}" stroke-width="5"/>')
        halves += face(cx, 340, mood, .9) + "</g>"
    return art("#b4613b", halves)


def deli_art(bg):
    slices = ""
    for i, (x, y, r) in enumerate([(430, 520, 190), (520, 470, 190), (600, 420, 185)]):
        slices += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f29aa8" {S}/>'
                   f'<circle cx="{x}" cy="{y}" r="{r-22}" fill="none" stroke="#fff" stroke-width="6" opacity=".7"/>'
                   + "".join(f'<ellipse cx="{x + dx}" cy="{y + dy}" rx="14" ry="8" fill="#fbd1d8"/>'
                             for dx, dy in [(-60, -40), (50, 30), (-20, 70), (70, -60), (-90, 40)]))
    body = (f'<rect x="170" y="200" width="300" height="420" rx="24" fill="{PAPER}" opacity=".9" {S}/>'
            f'<path d="M170 260 L300 200 L470 200 L470 230Z" fill="#cfd8dc" {S}/>'
            + slices
            + f'<path d="M780 420 Q790 330 720 290 Q760 420 780 420Z" fill="url(#hatch)"/>'
            + face(600, 410, "shock", 1.05)
            + f'<g transform="rotate(-12 300 650)"><rect x="180" y="610" width="250" height="80" rx="10" fill="{MUSTARD}" {S}/>'
            f'<text x="305" y="668" font-family="Anton" font-size="46" text-anchor="middle" fill="{INK}">OPENED</text></g>')
    return art("#18286b", body)


def beef_art(bg):
    left = f'<path d="M480 200 A260 260 0 0 0 480 720 L520 640 L460 560 L530 470 L460 380 L520 290Z" fill="#c8453b" {S}/>'
    right = (f'<g class="crack"><g transform="translate(70 -10) rotate(8 520 460)">'
             f'<path d="M520 200 A260 260 0 0 1 520 720 L560 640 L500 560 L570 470 L500 380 L560 290Z" fill="#c8453b" {S}/>'
             f'<path d="M560 290 L500 380 L570 470 L500 560 L560 640 L520 720 Q660 600 650 460 Q660 330 520 200Z" fill="#8f8a86" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M560 290 L500 380 L570 470 L500 560 L560 640 L520 720 Q660 600 650 460 Q660 330 520 200Z" fill="url(#dots)"/></g></g>')
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#f2a59a"/>' for x, y in [(330, 330), (390, 470), (300, 560), (420, 620), (350, 420)])
    lens = (f'<g class="lens"><circle cx="690" cy="430" r="120" fill="#ffffff" fill-opacity=".22" stroke="{INK}" stroke-width="16"/>'
            f'<path d="M775 520 L880 640" stroke="{INK}" stroke-width="34" stroke-linecap="round"/></g>')
    body = left + dots + right + f'<g class="blink">{face(360, 440, "shock", 1.05)}</g>' + lens
    return art("#e2b07a", body)


def hb_eggs_art(bg):
    def half(cx, cy, rot, mood):
        return (f'<g transform="rotate({rot} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="150" ry="112" fill="{PAPER}" {S}/>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="78" ry="70" fill="#ffc72c" {S}/>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="78" ry="70" fill="none" stroke="#8aa36b" stroke-width="7" opacity=".7"/>'
                + face(cx, cy - 6, mood, .8) + "</g>")
    body = (f'<ellipse cx="500" cy="300" rx="100" ry="132" fill="#e9dcc4" {S}/>'
            f'<path d="M545 180 Q620 290 575 410 Q625 300 545 180Z" fill="url(#hatch)"/>'
            + face(500, 300, "sleep", .9)
            + half(300, 540, -8, "happy") + half(700, 540, 8, "cool"))
    return art("#3f2a8a", body)


def dates_art(bg):
    def tag(x, y, rot, color, label, icon):
        return (f'<g transform="rotate({rot} {x} {y})">'
                f'<path d="M{x-220} {y-120} L{x+160} {y-120} L{x+230} {y} L{x+160} {y+120} L{x-220} {y+120}Z" fill="{color}" {S}/>'
                f'<circle cx="{x+150}" cy="{y}" r="20" fill="{bg}" {S}/>'
                f'<text x="{x-40}" y="{y-20}" font-family="Anton" font-size="78" text-anchor="middle" fill="{INK}">{label}</text>'
                f'{icon(x-40, y+55)}</g>')
    taste = lambda x, y: (star(x - 70, y, 26, INK) + star(x, y, 26, INK) + star(x + 70, y, 26, INK))
    safety = lambda x, y: (f'<path d="M{x} {y-42} L{x+38} {y-28} L{x+34} {y+10} Q{x+26} {y+36} {x} {y+48} Q{x-26} {y+36} {x-34} {y+10} L{x-38} {y-28}Z" fill="{PAPER}" {S}/>'
                           f'<path d="M{x-16} {y+2} l12 14 l22 -26" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    body = (f'<path d="M500 60 L500 160" stroke="{INK}" stroke-width="6" stroke-dasharray="4 14" stroke-linecap="round"/>'
            + tag(470, 270, -7, MUSTARD, "BEST BEFORE", taste)
            + tag(530, 560, 6, "#ff8a7a", "USE BY", safety))
    return art("#8f2f4f", body)


PINS = [
    Pin("rice-left-out-overnight", "left-out/rice-left-out-overnight/", "Rice left out overnight?", "TOSS IT",
        "Reheating won't save it.", "#22306b", CREAM, CORAL, RED, CREAM, "", q_size=118),
    Pin("pizza-left-out-overnight", "left-out/pizza-left-out-overnight/", "Pizza left out all night?", "TOSS IT",
        "2 hours max on the counter.", "#1f7a78", CREAM, MUSTARD, RED, CREAM, "", q_size=118),
    Pin("eggs", "food/eggs/", "How long do eggs last?", "3–5 WEEKS",
        "In the fridge. Middle shelf, not the door.", "#9cc9e8", INK, "#fff", CREAM, INK, "", q_size=118),
    Pin("raw-chicken", "food/raw-chicken/", "Raw chicken in the fridge?", "1–2 DAYS",
        "Then cook it or freeze it.", "#a8dcc6", INK, CREAM, INK, CREAM, "", q_size=112),
    Pin("butter", "food/butter/", "Butter on the counter?", "1–2 DAYS",
        "Fridge: 1–2 months. Keep it cool.", CORAL, INK, MUSTARD, CREAM, INK, "", q_size=118),
    Pin("avocado", "food/avocado/", "Ripe avocado?", "FRIDGE: 3–4 DAYS",
        "Ripen on the counter. Then chill.", "#f7d4bd", INK, "#2f5d34", "#2f5d34", CREAM, "", q_size=130, a_size=118),
    Pin("deli-meat", "food/deli-meat/", "Opened deli meat?", "3–5 DAYS",
        "Opening the pack starts the clock.", "#2f4bbf", CREAM, "#f29aa8", "#f29aa8", INK, "", q_size=124),
    Pin("ground-beef", "food/ground-beef/", "Gray inside your ground beef?", "IT'S NORMAL",
        "Trust the date and smell, not the color.", CREAM, INK, CORAL, GREEN, CREAM, "", q_size=104, a_size=140),
    Pin("hard-boiled-eggs", "food/hard-boiled-eggs/", "Hard-boiled eggs?", "1 WEEK",
        "In the fridge. Peeled or not.", "#7b5cd6", CREAM, MUSTARD, MUSTARD, INK, "", q_size=124, a_size=170),
    Pin("best-before-vs-use-by", "guides/best-before-vs-use-by/", "Best before or use by?", "TASTE ≠ SAFETY",
        "What the dates on food really mean.", "#f4a7b9", INK, "#fff", INK, CREAM, "", q_size=118, a_size=126),
]

ARTS = {"rice-left-out-overnight": rice_art, "pizza-left-out-overnight": pizza_art, "eggs": eggs_art,
        "raw-chicken": chicken_art, "butter": butter_art, "avocado": avocado_art, "deli-meat": deli_art,
        "ground-beef": beef_art, "hard-boiled-eggs": hb_eggs_art, "best-before-vs-use-by": dates_art}

COPY = {  # Pinterest title (<= 100 chars) and description (keyword-rich, honest)
    "rice-left-out-overnight": ("Rice left out overnight: is it safe to eat?",
        "Cooked rice left out overnight should be thrown out, even if you reheat it. Here's why rice is riskier than most leftovers, and how to store it safely. Answers from USDA food safety guidance."),
    "pizza-left-out-overnight": ("Pizza left out overnight: keep or toss?",
        "Leftover pizza can sit out 2 hours at most. After a night on the counter, toss it. How long pizza lasts in the fridge and freezer, from USDA data."),
    "eggs": ("How long do eggs last in the fridge?",
        "Raw eggs in the shell last 3 to 5 weeks in the fridge. Keep them on a middle shelf, not in the door. Egg storage tips and how to spot a bad egg."),
    "raw-chicken": ("How long does raw chicken last in the fridge?",
        "Raw chicken keeps only 1 to 2 days in the fridge and up to 9 months in the freezer. Safe thawing tips and signs it has gone bad, from USDA guidance."),
    "butter": ("Can butter stay on the counter?",
        "Butter can sit out 1 to 2 days in a covered dish, away from heat. In the fridge it lasts 1 to 2 months, frozen 6 to 9 months. Kitchen storage tips."),
    "avocado": ("How long do avocados last in the fridge?",
        "Ripen avocados on the counter, then move them to the fridge: a ripe avocado lasts 3 to 4 days. How to store cut avocado and spot a bad one."),
    "deli-meat": ("How long does deli meat last after opening?",
        "Opened or deli-sliced lunch meat lasts 3 to 5 days in the fridge, whatever date the pack says. Listeria tips and freezing guide, from USDA and CDC."),
    "ground-beef": ("Ground beef gray inside: is it bad?",
        "A gray center in ground beef is normal: it just didn't get air. Judge by the date, smell and feel instead. Ground beef lasts 1 to 2 days in the fridge."),
    "hard-boiled-eggs": ("How long do hard-boiled eggs last?",
        "Hard-boiled eggs last 1 week in the fridge, peeled or in the shell. Don't freeze them. Storage tips and how to tell if a boiled egg has gone bad."),
    "best-before-vs-use-by": ("Best before vs use by: what do food dates mean?",
        "Best before is about taste, use by is about safety in the UK and Europe, and sell by is for the store. A simple guide to the dates on food labels."),
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@500;700&display=block');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1000px;height:1500px;overflow:hidden}
.pin{width:1000px;height:1500px;position:relative;overflow:hidden;background:var(--bg);color:var(--text)}
.q{position:absolute;top:66px;left:66px;right:66px;font-family:Anton,Impact,sans-serif;font-size:var(--qs);
   line-height:.98;text-transform:uppercase;letter-spacing:.5px;text-shadow:7px 7px 0 var(--shadow)}
.art{position:absolute;left:0;width:1000px;height:800px;top:var(--art-top)}
.stamp{position:absolute;left:62px;bottom:224px;transform:rotate(-4deg);background:var(--sbg);color:var(--sfg);
   font-family:Anton,Impact,sans-serif;font-size:var(--as);line-height:1;padding:18px 36px 8px;border:8px solid #1d1a2f;
   box-shadow:14px 14px 0 #1d1a2f;letter-spacing:1px}
.sub{position:absolute;left:68px;right:60px;bottom:120px;font:700 40px 'Space Grotesk',sans-serif;line-height:1.15}
.foot{position:absolute;left:0;right:0;bottom:0;height:96px;background:#1d1a2f;color:#f6eedd;display:flex;
   align-items:center;justify-content:space-between;padding:0 66px;font:700 30px 'Space Grotesk',sans-serif}
.foot b{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:40px;letter-spacing:1px}
.foot b i{font-style:normal;color:#f3b33d}
.foot span{opacity:.85}
.grain{position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.42;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter><rect width='400' height='400' filter='url(%23n)'/></svg>")}
.speck{position:absolute;inset:0;pointer-events:none;opacity:.5;background-image:radial-gradient(rgba(255,255,255,.35) 1.2px,transparent 1.4px);background-size:23px 29px}
"""


MOTION = """
.q{animation:drop .7s cubic-bezier(.2,1.4,.4,1) both}
.art{animation:fadeup .8s .25s both}
.stamp{animation:slam .5s cubic-bezier(.2,1.5,.4,1) var(--slam,1.8s) both}
.pin{animation:shake .35s calc(var(--slam,1.8s) + .3s) both}
.sub{animation:fadeup .6s calc(var(--slam,1.8s) + .6s) both}
.foot{animation:fadeup .6s calc(var(--slam,1.8s) + .9s) both}
@keyframes drop{from{transform:translateY(-70px);opacity:0}to{transform:none;opacity:1}}
@keyframes fadeup{from{transform:translateY(30px);opacity:0}to{transform:none;opacity:1}}
@keyframes slam{0%{transform:rotate(-4deg) scale(2.6);opacity:0}55%{opacity:1}100%{transform:rotate(-4deg) scale(1);opacity:1}}
@keyframes shake{0%,100%{transform:none}25%{transform:translate(7px,-5px)}50%{transform:translate(-6px,5px)}75%{transform:translate(3px,2px)}}
.breathe{transform-box:fill-box;transform-origin:50% 100%;animation:breathe 2.6s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:scale(1,1)}50%{transform:scale(1.03,.97)}}
.z1,.z2{animation:float 2.6s ease-in infinite}.z2{animation-delay:1.3s}
@keyframes float{0%{transform:translate(0,30px);opacity:0}20%{opacity:1}100%{transform:translate(-50px,-110px);opacity:0}}
.tw>*{transform-box:fill-box;transform-origin:center;animation:tw 1.8s ease-in-out infinite}.tw>*:nth-child(2n){animation-delay:.9s}
@keyframes tw{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(.45);opacity:.35}}
.bob{animation:bob 4s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-14px)}}
.crack{animation:crack 1.1s cubic-bezier(.3,1.5,.5,1) .6s both}
@keyframes crack{from{transform:translate(-70px,10px) rotate(-6deg)}to{transform:none}}
.lens{animation:lens 1.3s cubic-bezier(.4,0,.2,1) 1.2s both}
@keyframes lens{from{transform:translate(-430px,170px);opacity:0}25%{opacity:1}to{transform:none;opacity:1}}
.blink{transform-box:fill-box;transform-origin:center;animation:blink 3.2s 1.4s infinite}
@keyframes blink{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.1)}}
"""


def html(p: Pin, animated: bool = False, slam: float = 1.8) -> str:
    lines = 1 if len(p.question) <= 14 else 2 if len(p.question) <= 26 else 3
    art_top = {1: 210, 2: 300, 3: 390}[lines]
    style = (f"--bg:{p.bg};--text:{p.text};--shadow:{p.shadow};--sbg:{p.stamp_bg};--sfg:{p.stamp_fg};"
             f"--qs:{p.q_size}px;--as:{p.a_size}px;--art-top:{art_top}px")
    if animated:
        style += f";--slam:{slam}s"
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{MOTION if animated else ''}</style></head><body>"
            f"<div class='pin' style='{style}'>"
            f"<div class='art'>{ARTS[p.slug](p.bg)}</div>"
            f"<div class='q'>{p.question}</div>"
            f"<div class='stamp'>{p.answer}</div>"
            f"<div class='sub'>{p.sub}</div>"
            f"<div class='foot'><b>KEEP <i>OR</i> TOSS</b><span>Check 438 foods free →</span></div>"
            f"<div class='speck'></div><div class='grain'></div></div></body></html>")


def render(html_text: str, out_png: Path) -> None:
    tmp = Path(tempfile.mkdtemp())
    src = tmp / "pin.html"
    src.write_text(html_text, encoding="utf-8")
    args = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={tmp / 'p'}",
            "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw",
            "--force-device-scale-factor=1", f"--window-size={W},{H}", f"--screenshot={out_png}", src.as_uri()]
    subprocess.run(args, check=True, capture_output=True, timeout=180)
    shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str]) -> int:
    OUT.mkdir(exist_ok=True)
    wanted = set(argv[1:])
    for p in PINS:
        if wanted and p.slug not in wanted:
            continue
        (OUT / "src").mkdir(exist_ok=True)
        doc = html(p)
        (OUT / "src" / f"{p.slug}.html").write_text(doc, encoding="utf-8")
        render(doc, OUT / f"{p.slug}.png")
        print(f"rendered pins/{p.slug}.png")
    with open(OUT / "pins.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "title", "description", "link", "alt_text"])
        for p in PINS:
            title, desc = COPY[p.slug]
            alt = f"Illustrated pin: {p.question} Answer: {p.answer.title()}. {p.sub}"
            w.writerow([f"{p.slug}.png", title, desc, pin_link(p.path), alt])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
