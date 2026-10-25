# wrist-agent

Talk to your coding agents (Claude Code now; Gemini CLI / OpenCode later) from a smartwatch, with an
Android phone as the brain and your own UI. Same capability as sitting at the laptop: real sessions with
tools, file edits and plans. You hear and read replies on the wrist and approve, deny, or modify by voice or button.

```
Noise watch  <-- Bluetooth: mic, speaker, notifications, media keys, call buttons -->  Android app
Android app  <-- WebSocket over Tailscale -->  gateway (your laptop / cloud box)  -->  Claude Code (Agent SDK)
```

## What works today

| Piece | State |
|---|---|
| `gateway/`: real Claude Code sessions via the Agent SDK, approvals (tools, **plans**, questions), voice-intent parsing, watch-sized text cards, default-deny timeout, token auth | Built. 10 unit tests pass with a faked Claude. **Not yet run against the real API.** |
| `android/`: gateway client, foreground service, TTS/STT, notifications with Approve/Deny/Modify actions, media-button mapping, probe buttons | Compiles to an APK. **Not yet run on a device.** |
| Noise watch channels (below) | **Unverified.** That is what the probes are for. |

## How approving and modifying plans works

- Claude proposes a plan, which arrives as an `approval` of kind `plan`, paged into ~180-char watch cards.
- **Approve:** say "approve" / press Approve / media Next.
- **Deny:** say "no" / press Deny / media Previous.
- **Modify:** say "modify, use SQLite instead", or type it in the notification's Modify reply. The gateway denies the plan
  with your feedback; Claude revises and proposes again. Any other speech while a plan is open counts as feedback, never as approval.
- Silence for 2 minutes = **deny**.

## Run the gateway

```sh
cd gateway && npm ci
export WRIST_TOKEN=$(openssl rand -hex 24)   # also paste into the phone app
export WRIST_ROOT=$HOME/projects             # sessions can only start inside here
npm start                                    # needs Claude Code auth: `claude login` or ANTHROPIC_API_KEY
```

It binds to `127.0.0.1` by default. These approvals authorise shell commands, so don't expose it: install
[Tailscale](https://tailscale.com) on laptop and phone, then `HOST=<laptop tailscale ip> npm start`
and use `ws://<that ip>:8787` in the app.

## Run the watch probes (please do this and report back)

Install the APK (CI artifact `wrist-agent-debug-apk`, or `cd android && gradle assembleDebug`). Pair the Noise
watch in NoiseFit and in Android Bluetooth settings (so it is also a phone-call/headset device). In NoiseFit, allow
notification access for "Wrist Agent". Tap **Connect** first (starts the service), then:

1. **Route audio + speak test:** does the test sentence play from the *watch* speaker? Then tap *Talk* and speak into the watch: does the log show `heard: ...`?
2. **Media buttons:** open the watch's music/camera-remote controls and press play/next/previous. Does the log show `media key: ...`?
3. **Notification mirror:** does "Watch text test" appear on the watch? Does the long text scroll?
4. **Call trick (4a and 4b):** does the watch ring with the question as the caller name? Do Answer/Reject show `call ANSWERED` / `call REJECTED`? (4b needs the account enabled under Phone → Settings → Calling accounts.)

Whatever fails, we fall back: voice-only approvals plus mirrored notifications always work if (1) and (3) do.

## Not built yet

Gemini CLI / OpenCode adapters, a web dashboard, session resume after gateway restart, and a Wear OS client.
