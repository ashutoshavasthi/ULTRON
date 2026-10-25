import test from "node:test";
import assert from "node:assert/strict";
import { Session, type QueryFn } from "../src/session.js";
import type { ServerMessage } from "../src/protocol.js";

// A fake Claude: for each user prompt it asks permission for ExitPlanMode, then
// reports what the permission callback decided.
function fakeQuery(toolName: string, input: Record<string, unknown>, decisions: string[]): QueryFn {
  return (({ prompt, options }: any) => {
    const gen = (async function* () {
      for await (const _msg of prompt) {
        const ac = new AbortController();
        const r = await options.canUseTool(toolName, input, { signal: ac.signal, toolUseID: "t1", requestId: "r1" });
        decisions.push(r.behavior + (r.message ? `:${r.message}` : ""));
        yield { type: "assistant", message: { content: [{ type: "text", text: `decision ${r.behavior}` }] } };
        yield { type: "result", subtype: "success", result: "done", total_cost_usd: 0.01 };
      }
    })() as any;
    gen.interrupt = async () => {};
    gen.close = () => {};
    return gen;
  }) as unknown as QueryFn;
}

function setup(toolName = "ExitPlanMode", input: Record<string, unknown> = { plan: "1. Add db. 2. Migrate." }, timeoutMs = 60_000) {
  const events: ServerMessage[] = [];
  const decisions: string[] = [];
  const s = new Session({ cwd: "/tmp", emit: (m) => events.push(m), queryFn: fakeQuery(toolName, input, decisions), approvalTimeoutMs: timeoutMs });
  const tick = () => new Promise((r) => setTimeout(r, 20));
  const pending = () => events.find((e) => e.type === "approval.request") as Extract<ServerMessage, { type: "approval.request" }> | undefined;
  return { s, events, decisions, tick, pending };
}

test("plan approval by voice allows the tool", async () => {
  const { s, decisions, tick, pending } = setup();
  s.prompt("build it");
  await tick();
  assert.equal(pending()?.approval.kind, "plan");
  s.utterance("approve");
  await tick();
  assert.deepEqual(decisions, ["allow"]);
  s.close();
});

test("modify sends the user's feedback back to the agent as a denial", async () => {
  const { s, decisions, tick } = setup();
  s.prompt("build it");
  await tick();
  s.utterance("modify: use sqlite instead");
  await tick();
  assert.match(decisions[0], /^deny:.*use sqlite instead/);
  assert.match(decisions[0], /Revise and propose again/);
  s.close();
});

test("silence times out to deny", async () => {
  const { s, decisions, tick } = setup("Bash", { command: "rm -rf /tmp/x" }, 30);
  s.prompt("clean");
  await new Promise((r) => setTimeout(r, 120));
  assert.match(decisions[0], /^deny:.*timeout/);
  await tick();
  s.close();
});

test("question choice becomes an answer", async () => {
  const q = { questions: [{ question: "Which DB?", header: "DB", options: [{ label: "SQLite", description: "" }, { label: "Postgres", description: "" }] }] };
  const { s, decisions, tick, pending } = setup("AskUserQuestion", q);
  s.prompt("go");
  await tick();
  assert.deepEqual(pending()?.approval.watchCards, ["Which DB?", "1. SQLite", "2. Postgres"]);
  s.utterance("two");
  await tick();
  assert.deepEqual(decisions, ["allow"]);
  s.close();
});

test("assistant replies are paged for the watch", async () => {
  const { s, events, tick } = setup();
  s.prompt("hi");
  await tick();
  s.utterance("approve");
  await tick();
  const t = events.find((e) => e.type === "assistant.text") as any;
  assert.deepEqual(t.watchCards, ["decision allow"]);
  s.close();
});
