// Wire protocol between the gateway and clients (phone app, web dashboard, test tools).
// Every message is one JSON object per WebSocket frame.

export type PermissionKind = "tool" | "plan" | "question";

export interface PendingApproval {
  id: string;
  sessionId: string;
  kind: PermissionKind;
  title: string; // one-line summary, safe for a watch screen
  detail: string; // full text (command, plan markdown, question)
  watchCards: string[]; // detail split into watch-sized pages
  options?: { label: string; description: string }[]; // for kind === "question"
  expiresAt: number; // epoch ms; default-deny after this
}

// client -> gateway
export type ClientMessage =
  | { type: "hello"; token: string }
  | { type: "session.start"; cwd: string; name?: string; model?: string; permissionMode?: "default" | "plan" | "acceptEdits" }
  | { type: "session.list" }
  | { type: "prompt"; sessionId: string; text: string }
  // Raw speech-to-text from the phone/watch. The gateway decides whether it is an
  // answer to a pending approval or a new instruction.
  | { type: "utterance"; sessionId: string; text: string }
  | { type: "approval.respond"; id: string; decision: "approve" | "deny" | "modify" | "choose"; feedback?: string; choice?: number }
  | { type: "session.interrupt"; sessionId: string }
  | { type: "watch.next"; sessionId: string }
  | { type: "watch.repeat"; sessionId: string };

// gateway -> client
export type ServerMessage =
  | { type: "hello.ok"; sessions: SessionInfo[] }
  | { type: "error"; message: string }
  | { type: "session.started"; session: SessionInfo }
  | { type: "sessions"; sessions: SessionInfo[] }
  | { type: "assistant.text"; sessionId: string; text: string; watchCards: string[] }
  | { type: "tool.use"; sessionId: string; tool: string; summary: string }
  | { type: "approval.request"; approval: PendingApproval }
  | { type: "approval.resolved"; id: string; outcome: string }
  | { type: "turn.done"; sessionId: string; summary: string; costUsd?: number }
  | { type: "watch.card"; sessionId: string; card: string; index: number; total: number };

export interface SessionInfo {
  id: string;
  name: string;
  cwd: string;
  status: "idle" | "running" | "waiting_approval";
}
