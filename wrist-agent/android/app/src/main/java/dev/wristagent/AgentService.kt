package dev.wristagent

import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.os.IBinder
import android.support.v4.media.session.MediaSessionCompat
import android.support.v4.media.session.PlaybackStateCompat
import android.view.KeyEvent
import org.json.JSONObject

/** Keeps the gateway connection, voice, media-button handling and notifications alive. */
class AgentService : Service(), Gateway.Listener {
    private lateinit var notifier: Notifier
    private lateinit var voice: Voice
    private var gateway: Gateway? = null
    private var media: MediaSessionCompat? = null
    private var silence: AudioTrack? = null
    private var sessionId: String? = null
    private var pendingId: String? = null
    private var callMode = false

    override fun onCreate() {
        super.onCreate()
        instance = this
        notifier = Notifier(this)
        voice = Voice(this, onHeard = { text -> sessionId?.let { send("utterance", it, text) } }, log = ::log)
        voice.start()
        startForeground(
            1, notifier.foreground("Starting..."),
            ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE or ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
        )
        startMedia()
        CallTrick.log = ::log
        CallTrick.onAnswer = { pendingId?.let { decide(it, "approve", null) } }
        CallTrick.onReject = { pendingId?.let { decide(it, "deny", null) } }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        intent?.let {
            val url = it.getStringExtra("url")
            val token = it.getStringExtra("token")
            callMode = it.getBooleanExtra("callMode", false)
            if (url != null && token != null) {
                gateway?.close()
                gateway = Gateway(url, token, this).also { g -> g.connect() }
            }
            if (it.getBooleanExtra("route", false)) log("route to watch: ${voice.routeToWatch() ?: "no Bluetooth SCO device found"}")
        }
        return START_STICKY
    }

    // ---- gateway events ----

    override fun onStatus(text: String) = log("gateway: $text")

    override fun onMessage(msg: JSONObject) {
        when (msg.getString("type")) {
            "hello.ok" -> {
                val list = msg.getJSONArray("sessions")
                if (list.length() > 0) sessionId = list.getJSONObject(0).getString("id")
                else gateway?.send(JSONObject().put("type", "session.start").put("cwd", ".").put("name", "main"))
            }
            "session.started" -> if (sessionId == null) sessionId = msg.getJSONObject("session").getString("id")
            "assistant.text" -> {
                val cards = msg.getJSONArray("watchCards")
                if (cards.length() == 0) return
                notifier.card(2000, "Claude", cards.getString(0))
                log("claude: ${msg.getString("text").take(300)}")
                voice.speak(msg.getString("text").take(500))
            }
            "tool.use" -> log("tool: ${msg.getString("summary")}")
            "approval.request" -> onApproval(msg.getJSONObject("approval"))
            "approval.resolved" -> { pendingId = null; notifier.clearApproval(); log("resolved: ${msg.getString("outcome")}") }
            "turn.done" -> notifier.card(2002, "Done", msg.getString("summary"))
            "error" -> log("error: ${msg.getString("message")}")
            "watch.card" -> {
                val c = msg.getString("card")
                notifier.card(2001, "Claude ${msg.getInt("index") + 1}/${msg.getInt("total")}", c)
                voice.speak(c)
            }
        }
    }

    private fun onApproval(a: JSONObject) {
        pendingId = a.getString("id")
        val kind = a.getString("kind")
        val cards = a.getJSONArray("watchCards")
        val first = if (cards.length() > 0) cards.getString(0) else a.getString("title")
        val title = when (kind) { "plan" -> "Plan: approve?"; "question" -> a.getString("title"); else -> a.getString("title") }
        notifier.approval(a.getString("id"), title, first)
        val spoken = when (kind) {
            "plan" -> "Plan proposed. $first. Say approve, deny, or modify followed by your change."
            "question" -> (0 until cards.length()).joinToString(". ") { cards.getString(it) }
            else -> "${a.getString("title")}. Approve or deny?"
        }
        voice.speak(spoken) { voice.listen() }
        if (callMode) CallTrick.ring(this, selfManaged = true, title = title)
    }

    fun decide(id: String, decision: String, feedback: String?) {
        gateway?.send(JSONObject().put("type", "approval.respond").put("id", id).put("decision", decision).apply {
            if (!feedback.isNullOrBlank()) put("feedback", feedback)
        })
    }

    private fun send(type: String, session: String, text: String) {
        gateway?.send(JSONObject().put("type", type).put("sessionId", session).put("text", text))
    }

    // ---- media buttons (watch music controls) ----

    private fun startMedia() {
        // A silent looping track keeps our MediaSession the target of media buttons.
        silence = AudioTrack.Builder()
            .setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_MEDIA).build())
            .setAudioFormat(AudioFormat.Builder().setEncoding(AudioFormat.ENCODING_PCM_16BIT).setSampleRate(8000).setChannelMask(AudioFormat.CHANNEL_OUT_MONO).build())
            .setBufferSizeInBytes(16000).setTransferMode(AudioTrack.MODE_STATIC).build().also {
                it.write(ByteArray(16000), 0, 16000); it.setLoopPoints(0, 8000, -1); it.play()
            }
        media = MediaSessionCompat(this, "wrist-agent").apply {
            setCallback(object : MediaSessionCompat.Callback() {
                override fun onMediaButtonEvent(mediaButtonEvent: Intent?): Boolean {
                    val ev = mediaButtonEvent?.getParcelableExtra<KeyEvent>(Intent.EXTRA_KEY_EVENT)
                    if (ev != null && ev.action == KeyEvent.ACTION_DOWN) log("media key: ${KeyEvent.keyCodeToString(ev.keyCode)}")
                    return super.onMediaButtonEvent(mediaButtonEvent)
                }
                override fun onPlay() { talk() }
                override fun onPause() { talk() }
                override fun onSkipToNext() { pendingId?.let { decide(it, "approve", null) } ?: sessionId?.let { gateway?.send(JSONObject().put("type", "watch.next").put("sessionId", it)) } }
                override fun onSkipToPrevious() { pendingId?.let { decide(it, "deny", null) } ?: sessionId?.let { gateway?.send(JSONObject().put("type", "watch.repeat").put("sessionId", it)) } }
            })
            setPlaybackState(PlaybackStateCompat.Builder()
                .setActions(PlaybackStateCompat.ACTION_PLAY or PlaybackStateCompat.ACTION_PAUSE or PlaybackStateCompat.ACTION_PLAY_PAUSE or PlaybackStateCompat.ACTION_SKIP_TO_NEXT or PlaybackStateCompat.ACTION_SKIP_TO_PREVIOUS)
                .setState(PlaybackStateCompat.STATE_PLAYING, 0, 1f).build())
            isActive = true
        }
    }

    fun talk() { voice.listen() }

    fun typed(text: String) { sessionId?.let { send("utterance", it, text) } }

    fun probeSpeak() = voice.speak("Watch speaker test. If you hear this on your watch, the audio route works.")

    fun probeRoute(): String? = voice.routeToWatch()

    private fun log(s: String) { sink?.invoke(s) }

    override fun onDestroy() {
        instance = null
        gateway?.close(); voice.shutdown(); media?.release(); silence?.release()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    companion object {
        var instance: AgentService? = null
        var sink: ((String) -> Unit)? = null
    }
}
