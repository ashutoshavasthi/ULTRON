import { randomUUID } from "node:crypto";
import { query as sdkQuery } from "@anthropic-ai/claude-agent-sdk";
import type { CanUseTool, PermissionResult, SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";
import type { PendingApproval, PermissionKind, ServerMessage, SessionInfo } from "./protocol.js";
import { summarizeTool, toWatchCards } from "./watch.js";
import { parseUtterance } from "./intent.js";

export type QueryFn = typeof sdkQuery;

export interface SessionOptions {
  cwd: string;
  name?: string;
  model?: string;
  permissionMode?: "default" | "plan" | "acceptEdits";
  approvalTimeoutMs?: number;
  emit: (msg: ServerMessage) => void;
  queryFn?: QueryFn; // injectable for tests
}

interface Pending {
  approval: PendingApproval;
  input: Record<string, unknown>;
  resolve: (r: PermissionResult) => void;
  timer: NodeJS.Timeout;
}

/** A single Claude Code conversation, driven by prompts and approvals from the wrist. */
export class Session {
  readonly id = randomUUID();
  readonly name: string;
  readonly cwd: string;
  status: SessionInfo["status"] = "idle";

  private readonly emit: (msg: ServerMessage) => void;
  private readonly timeoutMs: number;
  private readonly pending = new Map<string, Pending>();
  private readonly inbox: SDKUserMessage[] = [];
  private wake: (() => void) | null = null;
  private closed = false;
  private cards: string[] = [];
  private cursor = 0;
  private readonly q: ReturnType<QueryFn>;

  constructor(opts: SessionOptions) {
    this.cwd = opts.cwd;
    this.name = opts.name ?? opts.cwd.split("/").filter(Boolean).pop() ?? "session";
    this.emit = opts.emit;
    this.timeoutMs = opts.approvalTimeoutMs ?? 120_000;
    const queryFn = opts.queryFn ?? sdkQuery;
    this.q = queryFn({
      prompt: this.input(),
      options: {
        cwd: opts.cwd,
        model: opts.model,
        permissionMode: opts.permissionMode ?? "default",
        canUseTool: this.canUseTool,
      },
    });
    void this.pump();
  }

  info(): SessionInfo {
    return { id: this.id, name: this.name, cwd: this.cwd, status: this.status };
  }

  prompt(text: string): void {
    this.inbox.push({
      type: "user",
      message: { role: "user", content: text },
      parent_tool_use_id: null,
    });
    this.wake?.();
  }

  /** Voice entry point: decide if speech answers an approval or is a new instruction. */
  utterance(text: string): void {
    const open = [...this.pending.values()][0];
    const intent = parseUtterance(text, !!open, open?.approval.options?.length ?? 0);
    switch (intent.kind) {
      case "approve": return void this.respond(open!.approval.id, "approve");
      case "deny": return void this.respond(open!.approval.id, "deny");
      case "modify": return void this.respond(open!.approval.id, "modify", intent.feedback);
      case "choose": return void this.respond(open!.approval.id, "choose", undefined, intent.choice);
      case "stop": return void this.interrupt();
      case "next": return this.nextCard();
      case "repeat": return this.repeatCard();
      case "prompt": return this.prompt(intent.text);
    }
  }

  respond(id: string, decision: "approve" | "deny" | "modify" | "choose", feedback?: string, choice?: number): boolean {
    const p = this.pending.get(id);
    if (!p) return false;
    clearTimeout(p.timer);
    this.pending.delete(id);
    let result: PermissionResult;
    let outcome: string = decision;
    if (decision === "approve") {
      result = { behavior: "allow", updatedInput: p.input };
    } else if (decision === "choose" && p.approval.kind === "question" && choice !== undefined) {
      const label = p.approval.options?.[choice]?.label ?? "";
      const question = String((p.input.questions as { question: string }[] | undefined)?.[0]?.question ?? "");
      result = { behavior: "allow", updatedInput: { ...p.input, answers: { [question]: label } } };
      outcome = `chose: ${label}`;
    } else if (decision === "modify") {
      const what = p.approval.kind === "plan" ? "plan" : "action";
      result = { behavior: "deny", message: `The user did not approve this ${what} as written and asks for changes: ${feedback ?? "(no details)"}. Revise and propose again.` };
    } else {
      result = { behavior: "deny", message: feedback ? `The user denied this: ${feedback}` : "The user denied this request." };
    }
    this.setStatus(this.pending.size ? "waiting_approval" : "running");
    this.emit({ type: "approval.resolved", id, outcome });
    p.resolve(result);
    return true;
  }

  async interrupt(): Promise<void> {
    for (const id of [...this.pending.keys()]) this.respond(id, "deny", "interrupted");
    await this.q.interrupt();
  }

  nextCard(): void {
    if (this.cursor < this.cards.length - 1) this.cursor++;
    this.sendCard();
  }

  repeatCard(): void {
    this.sendCard();
  }

  close(): void {
    this.closed = true;
    for (const id of [...this.pending.keys()]) this.respond(id, "deny", "session closed");
    this.wake?.();
    this.q.close?.();
  }

  // ---- internals ----

  private async *input(): AsyncGenerator<SDKUserMessage> {
    while (!this.closed) {
      const next = this.inbox.shift();
      if (next) {
        this.setStatus("running");
        yield next;
      } else {
        await new Promise<void>((r) => (this.wake = r));
        this.wake = null;
      }
    }
  }

  private async pump(): Promise<void> {
    try {
      for await (const msg of this.q) {
        if (msg.type === "assistant") {
          const text: string[] = [];
          for (const block of msg.message.content) {
            if (block.type === "text") text.push(block.text);
            else if (block.type === "tool_use") {
              this.emit({ type: "tool.use", sessionId: this.id, tool: block.name, summary: summarizeTool(block.name, block.input as Record<string, unknown>) });
            }
          }
          const joined = text.join("\n").trim();
          if (joined) this.speak(joined);
        } else if (msg.type === "result") {
          const summary = msg.subtype === "success" ? msg.result : `Stopped: ${msg.subtype}`;
          this.setStatus("idle");
          this.emit({ type: "turn.done", sessionId: this.id, summary: toWatchCards(summary)[0] ?? "Done.", costUsd: msg.total_cost_usd });
        }
      }
    } catch (err) {
      this.emit({ type: "error", message: `session ${this.name}: ${(err as Error).message}` });
    } finally {
      this.setStatus("idle");
    }
  }

  private speak(text: string): void {
    this.cards = toWatchCards(text);
    this.cursor = 0;
    this.emit({ type: "assistant.text", sessionId: this.id, text, watchCards: this.cards });
  }

  private sendCard(): void {
    const card = this.cards[this.cursor];
    if (card) this.emit({ type: "watch.card", sessionId: this.id, card, index: this.cursor, total: this.cards.length });
  }

  private setStatus(s: SessionInfo["status"]): void {
    this.status = s;
  }

  private canUseTool: CanUseTool = (toolName, input, options) => {
    let kind: PermissionKind = "tool";
    let title = options.title ?? summarizeTool(toolName, input);
    let detail = options.description ?? JSON.stringify(input, null, 2);
    let choices: PendingApproval["options"];
    if (toolName === "ExitPlanMode") {
      kind = "plan";
      detail = typeof input.plan === "string" ? input.plan : JSON.stringify(input, null, 2);
      title = "Approve plan?";
    } else if (toolName === "AskUserQuestion") {
      kind = "question";
      const q = (input.questions as { question: string; options: { label: string; description: string }[] }[])[0];
      title = q.question;
      detail = q.question;
      choices = q.options;
    }
    const id = randomUUID();
    const watchCards = kind === "question"
      ? [title, ...(choices ?? []).map((o, i) => `${i + 1}. ${o.label}`)]
      : toWatchCards(kind === "plan" ? detail : `${title}`);
    const approval: PendingApproval = {
      id, sessionId: this.id, kind, title, detail, watchCards, options: choices,
      expiresAt: Date.now() + this.timeoutMs,
    };
    return new Promise<PermissionResult>((resolve) => {
      // Default-deny: silence is never consent.
      const timer = setTimeout(() => {
        this.respond(id, "deny", "no response before the approval timeout");
      }, this.timeoutMs);
      this.pending.set(id, { approval, input, resolve, timer });
      options.signal.addEventListener("abort", () => this.respond(id, "deny", "aborted"), { once: true });
      this.setStatus("waiting_approval");
      this.emit({ type: "approval.request", approval });
    });
  };
}
