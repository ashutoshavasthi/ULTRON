import { createServer } from "node:http";
import { timingSafeEqual } from "node:crypto";
import { relative, resolve } from "node:path";
import { WebSocketServer, type WebSocket } from "ws";
import type { ClientMessage, ServerMessage } from "./protocol.js";
import { Session } from "./session.js";

const TOKEN = process.env.WRIST_TOKEN ?? "";
const PORT = Number(process.env.PORT ?? 8787);
const HOST = process.env.HOST ?? "127.0.0.1"; // use Tailscale/ZeroTier, don't expose publicly
const ROOT = process.env.WRIST_ROOT ?? process.cwd(); // sessions may only start inside this tree

if (TOKEN.length < 16) {
  console.error("Set WRIST_TOKEN to a random string of at least 16 characters.");
  process.exit(1);
}

const sessions = new Map<string, Session>();
const clients = new Set<WebSocket>();

function broadcast(msg: ServerMessage): void {
  const data = JSON.stringify(msg);
  for (const c of clients) if (c.readyState === c.OPEN) c.send(data);
}

function tokenOk(given: string): boolean {
  const a = Buffer.from(given);
  const b = Buffer.from(TOKEN);
  return a.length === b.length && timingSafeEqual(a, b);
}

const http = createServer((_req, res) => {
  res.writeHead(200, { "content-type": "text/plain" }).end("wrist-agent gateway\n");
});
const wss = new WebSocketServer({ server: http });

wss.on("connection", (ws) => {
  let authed = false;
  const authTimer = setTimeout(() => { if (!authed) ws.close(4401, "auth timeout"); }, 5000);
  ws.on("close", () => clearTimeout(authTimer));
  const send = (m: ServerMessage) => ws.send(JSON.stringify(m));
  const get = (id: string) => sessions.get(id);

  ws.on("message", (raw) => {
    let msg: ClientMessage;
    try { msg = JSON.parse(String(raw)); } catch { return send({ type: "error", message: "bad json" }); }
    if (!authed) {
      if (msg.type === "hello" && tokenOk(msg.token)) {
        authed = true;
        clients.add(ws);
        return send({ type: "hello.ok", sessions: [...sessions.values()].map((s) => s.info()) });
      }
      return ws.close(4401, "unauthorized");
    }
    switch (msg.type) {
      case "session.start": {
        const cwd = resolve(ROOT, msg.cwd);
        const rel = relative(ROOT, cwd);
        if (rel.startsWith("..") || resolve(rel) === rel) return send({ type: "error", message: `cwd must be inside ${ROOT}` });
        const s = new Session({ cwd, name: msg.name, model: msg.model, permissionMode: msg.permissionMode, emit: broadcast });
        sessions.set(s.id, s);
        return broadcast({ type: "session.started", session: s.info() });
      }
      case "session.list":
        return send({ type: "sessions", sessions: [...sessions.values()].map((s) => s.info()) });
      case "prompt": return get(msg.sessionId)?.prompt(msg.text);
      case "utterance": return get(msg.sessionId)?.utterance(msg.text);
      case "approval.respond":
        for (const s of sessions.values()) if (s.respond(msg.id, msg.decision, msg.feedback, msg.choice)) return;
        return send({ type: "error", message: "no such pending approval" });
      case "session.interrupt": return void get(msg.sessionId)?.interrupt();
      case "watch.next": return get(msg.sessionId)?.nextCard();
      case "watch.repeat": return get(msg.sessionId)?.repeatCard();
    }
  });
  ws.on("close", () => clients.delete(ws));
});

http.listen(PORT, HOST, () => console.log(`wrist-agent gateway on ${HOST}:${PORT}, root ${ROOT}`));
