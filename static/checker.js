// "Is it still OK?" checker. Pure logic first (tested with node --test), DOM wiring after.

const UNIT_HOURS = { hours: 1, days: 24, weeks: 168, months: 720 };
const PLACE_LABEL = { fridge: "fridge", freezer: "freezer", pantry: "pantry", counter: "counter" };

export function placesFor(food) {
  return Object.keys(food.places).filter((p) => food.places[p] !== null);
}

export function spanText(s) {
  const unit = s.max === 1 ? s.unit.slice(0, -1) : s.unit;
  if (s.min === 0) return `up to ${s.max} ${unit}`;
  if (s.min === s.max) return `${s.max} ${unit}`;
  return `${s.min}–${s.max} ${unit}`;
}

export function verdict(food, place, ageHours) {
  if (typeof ageHours !== "number" || Number.isNaN(ageHours) || ageHours < 0) {
    return { verdict: null, reason: "Pick when it was opened or cooked." };
  }
  const s = food.places[place];
  if (!s) {
    const better = food.places.fridge ? " Store it in the fridge instead." : "";
    return { verdict: "toss", reason: `Not recommended: ${food.name.toLowerCase()} should not be kept on the ${PLACE_LABEL[place] || place}.${better}` };
  }
  const span = spanText(s);
  if (place === "freezer") {
    if (ageHours <= s.maxHours) {
      return { verdict: "keep", reason: `Safe while frozen. Best quality within ${span}.` };
    }
    return { verdict: "keep", reason: `Still safe while frozen; taste and texture fade after ${span}.` };
  }
  if (s.maxHours <= 24) {
    if (ageHours <= s.maxHours) {
      return { verdict: "use-today", reason: `Eat it now or put it in the fridge. It is only safe on the ${place} for ${span}.` };
    }
    return { verdict: "toss", reason: `It has been out longer than ${span}. Germs can grow without any smell or sign. Throw it out.` };
  }
  if (ageHours <= s.maxHours - 24) {
    return { verdict: "keep", reason: `Fine to eat. It lasts ${span} in the ${place}.` };
  }
  if (ageHours <= s.maxHours) {
    return { verdict: "use-today", reason: `It is at the end of its safe time (${span} in the ${place}). Eat it today or toss it.` };
  }
  return { verdict: "toss", reason: `It has been longer than ${span} in the ${place}. Throw it out, even if it looks fine.` };
}

const WORD = { keep: ["keep", "✓ KEEP"], "use-today": ["today", "⏱ USE TODAY"], toss: ["toss", "✕ TOSS"] };

function el(tag, attrs = {}, text = "") {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (text) n.textContent = text;
  return n;
}

export async function initChecker(root) {
  const res = await fetch(new URL("../checker.json", import.meta.url));
  const foods = await res.json();
  const bySlug = Object.fromEntries(foods.map((f) => [f.slug, f]));

  const form = el("form", { class: "checker-form", novalidate: "" });
  const foodSel = el("select", { id: "ck-food" });
  foodSel.append(el("option", { value: "" }, "Choose a food…"));
  const groups = {};
  for (const f of foods) {
    if (!groups[f.category]) {
      groups[f.category] = el("optgroup", { label: f.category[0].toUpperCase() + f.category.slice(1) });
      foodSel.append(groups[f.category]);
    }
    groups[f.category].append(el("option", { value: f.slug }, f.name));
  }
  const placeSel = el("select", { id: "ck-place" });
  const ageNum = el("input", { id: "ck-age", type: "number", min: "0", step: "1", inputmode: "numeric", placeholder: "e.g. 3" });
  const ageUnit = el("select", { id: "ck-unit", "aria-label": "Unit" });
  for (const u of ["hours", "days", "weeks", "months"]) ageUnit.append(el("option", { value: u }, `${u} ago`));
  ageUnit.value = "days";

  const field = (label, forId, ...controls) => {
    const d = el("div");
    d.append(el("label", { for: forId }, label));
    if (controls.length > 1) {
      const row = el("div", { class: "age-row" });
      row.append(...controls);
      d.append(row);
    } else d.append(controls[0]);
    return d;
  };
  form.append(field("Food", "ck-food", foodSel), field("Where is it kept?", "ck-place", placeSel),
    field("When was it opened or cooked?", "ck-age", ageNum, ageUnit));
  const out = el("div", { class: "checker-result", "aria-live": "polite" });
  root.append(form, out);

  const fillPlaces = () => {
    const f = bySlug[foodSel.value];
    placeSel.replaceChildren();
    if (!f) return;
    for (const p of placesFor(f)) placeSel.append(el("option", { value: p }, p[0].toUpperCase() + p.slice(1)));
  };
  const show = () => {
    out.replaceChildren();
    out.className = "checker-result";
    const f = bySlug[foodSel.value];
    if (!f || ageNum.value === "") return;
    const hours = Number(ageNum.value) * UNIT_HOURS[ageUnit.value];
    const v = verdict(f, placeSel.value, hours);
    if (!v.verdict) { out.append(el("p", {}, v.reason)); return; }
    const [cls, word] = WORD[v.verdict];
    out.className = `checker-result verdict verdict-${cls}`;
    const link = el("a", { href: `food/${f.slug}/` }, `Everything about ${f.name.toLowerCase()} →`);
    out.append(el("p", { class: "verdict-word" }, word), el("p", {}, v.reason), el("p"));
    out.lastChild.append(link);
  };
  foodSel.addEventListener("change", () => { fillPlaces(); show(); });
  for (const c of [placeSel, ageNum, ageUnit]) c.addEventListener("input", show);
  form.addEventListener("submit", (e) => { e.preventDefault(); show(); });

  const pre = new URLSearchParams(location.search).get("food");
  if (pre && bySlug[pre]) { foodSel.value = pre; fillPlaces(); }
}

function initSearch() {
  const input = document.getElementById("food-search");
  const list = document.getElementById("all-foods");
  if (!input || !list) return;
  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    for (const li of list.children) li.hidden = q !== "" && !li.dataset.name.includes(q);
  });
}

if (typeof document !== "undefined") {
  const root = document.querySelector("[data-checker]");
  if (root) initChecker(root);
  initSearch();
}
