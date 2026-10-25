import test from "node:test";
import assert from "node:assert/strict";
import { parseUtterance } from "../src/intent.js";
import { toWatchCards } from "../src/watch.js";

test("approve/deny words only count while an approval is pending", () => {
  assert.deepEqual(parseUtterance("yes", true), { kind: "approve" });
  assert.deepEqual(parseUtterance("Go ahead.", true), { kind: "approve" });
  assert.deepEqual(parseUtterance("no", true), { kind: "deny" });
  assert.deepEqual(parseUtterance("yes", false), { kind: "prompt", text: "yes" });
});

test("anything else during an approval is feedback, never approval", () => {
  assert.deepEqual(parseUtterance("modify: use sqlite instead", true), { kind: "modify", feedback: "use sqlite instead" });
  assert.deepEqual(parseUtterance("yes but skip the tests", true), { kind: "modify", feedback: "yes but skip the tests" });
});

test("choosing question options by number or word", () => {
  assert.deepEqual(parseUtterance("option 2", true, 3), { kind: "choose", choice: 1 });
  assert.deepEqual(parseUtterance("three", true, 3), { kind: "choose", choice: 2 });
  assert.equal(parseUtterance("five", true, 3).kind, "modify");
});

test("reading controls", () => {
  assert.deepEqual(parseUtterance("next", false), { kind: "next" });
  assert.deepEqual(parseUtterance("repeat", false), { kind: "repeat" });
  assert.deepEqual(parseUtterance("stop", false), { kind: "stop" });
});

test("watch cards respect the limit and are numbered", () => {
  const text = "First sentence here. ".repeat(30);
  const cards = toWatchCards(text);
  assert.ok(cards.length > 1);
  assert.ok(cards.every((c) => c.length <= 190));
  assert.match(cards[0], /^1\/\d+ /);
  assert.deepEqual(toWatchCards("Short."), ["Short."]);
  assert.deepEqual(toWatchCards("```x```"), ["[code]"]);
});
