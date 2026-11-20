import { test } from "node:test";
import assert from "node:assert/strict";
import { matchFoods, placesFor, spanText, verdict } from "../../static/checker.js";

const rice = {
  slug: "cooked-rice", name: "Cooked rice", category: "leftovers",
  places: {
    fridge: { min: 3, max: 4, unit: "days", maxHours: 96, basis: "safety", note: "" },
    freezer: { min: 1, max: 2, unit: "months", maxHours: 1440, basis: "quality", note: "" },
    counter: { min: 0, max: 2, unit: "hours", maxHours: 2, basis: "safety", note: "" },
  },
};
const chicken = {
  slug: "raw-chicken", name: "Raw chicken", category: "meat",
  places: { fridge: { min: 1, max: 2, unit: "days", maxHours: 48, basis: "safety", note: "" }, counter: null },
};

test("day 1 fridge is keep", () => {
  assert.equal(verdict(rice, "fridge", 24).verdict, "keep");
});

test("boundary day is use-today", () => {
  assert.equal(verdict(rice, "fridge", 80).verdict, "use-today");
  assert.equal(verdict(rice, "fridge", 96).verdict, "use-today");
});

test("past max is toss", () => {
  assert.equal(verdict(rice, "fridge", 97).verdict, "toss");
});

test("freezer past max keeps with quality note", () => {
  const v = verdict(rice, "freezer", 2000);
  assert.equal(v.verdict, "keep");
  assert.match(v.reason, /taste and texture fade/);
});

test("counter within 2h is use-today, after is toss", () => {
  assert.equal(verdict(rice, "counter", 1).verdict, "use-today");
  assert.equal(verdict(rice, "counter", 3).verdict, "toss");
});

test("future or missing date gives no verdict", () => {
  assert.equal(verdict(rice, "fridge", -5).verdict, null);
  assert.equal(verdict(rice, "fridge", NaN).verdict, null);
  assert.match(verdict(rice, "fridge", undefined).reason, /Pick when it was opened or cooked/);
});

test("places only lists stored places", () => {
  assert.deepEqual(placesFor(chicken), ["fridge"]);
  const v = verdict(chicken, "counter", 1);
  assert.equal(v.verdict, "toss");
  assert.match(v.reason, /Not recommended/);
});

test("spanText handles years and singular units", () => {
  assert.equal(spanText({ min: 1, max: 2, unit: "years" }), "1–2 years");
  assert.equal(spanText({ min: 1, max: 1, unit: "years" }), "1 year");
  assert.equal(spanText({ min: 6, max: 6, unit: "months" }), "6 months");
});

test("pantry with years works in verdict", () => {
  const honey = { slug: "honey", name: "Honey", places: { pantry: { min: 2, max: 2, unit: "years", maxHours: 17520 } } };
  assert.equal(verdict(honey, "pantry", 24 * 30).verdict, "keep");
});

test("matchFoods ranks words that start with the query first, and limits results", () => {
  const names = ["Pineapple", "Apples", "Apple cider (fresh)", "Grapes", "Applesauce (jar)"];
  assert.deepEqual(matchFoods(names, "apple", 3), ["Apple cider (fresh)", "Apples", "Applesauce (jar)"]);
  assert.deepEqual(matchFoods(names, "", 3), []);
  assert.deepEqual(matchFoods(names, "zzz", 3), []);
  assert.ok(matchFoods(names, "apple", 10).includes("Pineapple"));
});
