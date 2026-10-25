// Turns raw speech into an intent. Lives in the gateway so every client (phone,
// watch remote, web) behaves the same and it can be unit-tested.

export type Intent =
  | { kind: "approve" }
  | { kind: "deny"; feedback?: string }
  | { kind: "modify"; feedback: string }
  | { kind: "choose"; choice: number }
  | { kind: "stop" }
  | { kind: "next" }
  | { kind: "repeat" }
  | { kind: "prompt"; text: string };

const APPROVE = /^(yes|yeah|yep|approve|approved|go ahead|do it|proceed|ok|okay|sounds good|looks good|confirm|accept)\b[.!]?$/i;
const DENY = /^(no|nope|deny|denied|reject|cancel|don'?t|do not|stop that|negative)\b[.!]?$/i;
const MODIFY = /^(modify|change|revise|instead|actually|update the plan|edit)\b[:,]?\s*(.*)$/i;
const NEXT = /^(next|more|continue reading|go on)[.!]?$/i;
const REPEAT = /^(repeat|say again|again|read that again)[.!]?$/i;
const STOP = /^(stop|interrupt|abort|halt|hold on)[.!]?$/i;
const WORDS = ["one", "two", "three", "four", "five"];

export function parseUtterance(text: string, hasPending: boolean, optionCount = 0): Intent {
  const t = text.trim();
  if (hasPending) {
    if (APPROVE.test(t)) return { kind: "approve" };
    if (DENY.test(t)) return { kind: "deny" };
    const m = MODIFY.exec(t);
    if (m && m[2]?.trim()) return { kind: "modify", feedback: m[2].trim() };
    if (optionCount > 0) {
      const n = /^(?:option|number|choice)?\s*(\d)\b/i.exec(t)?.[1];
      const w = WORDS.findIndex((x) => new RegExp(`^(?:option|number|choice)?\\s*${x}\\b`, "i").test(t));
      const idx = n ? Number(n) : w >= 0 ? w + 1 : 0;
      if (idx >= 1 && idx <= optionCount) return { kind: "choose", choice: idx - 1 };
    }
    // Anything else while an approval is open is treated as feedback: the safest
    // reading is "not approved, and here is what I want instead".
    return { kind: "modify", feedback: t };
  }
  if (NEXT.test(t)) return { kind: "next" };
  if (REPEAT.test(t)) return { kind: "repeat" };
  if (STOP.test(t)) return { kind: "stop" };
  return { kind: "prompt", text: t };
}
