package dev.wristagent

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.InputType
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

/** Settings, a live log, and one button per watch-channel probe. */
class MainActivity : Activity() {
    private lateinit var logView: TextView
    private lateinit var scroll: ScrollView
    private val ui = Handler(Looper.getMainLooper())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("cfg", Context.MODE_PRIVATE)
        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(32, 48, 32, 32) }

        fun field(hint: String, key: String, password: Boolean = false) = EditText(this).apply {
            this.hint = hint
            setText(prefs.getString(key, ""))
            if (password) inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            root.addView(this)
        }
        fun button(label: String, onClick: () -> Unit) = Button(this).apply {
            text = label; isAllCaps = false; setOnClickListener { onClick() }; root.addView(this)
        }
        fun svc(block: AgentService.() -> Unit) {
            val s = AgentService.instance
            if (s == null) log("service not running: tap Connect first") else s.block()
        }

        val url = field("ws://100.x.y.z:8787 (gateway)", "url")
        val token = field("token", "token", password = true)
        val prompt = field("type an instruction", "prompt")

        button("Connect / start service") {
            prefs.edit().putString("url", url.text.toString()).putString("token", token.text.toString()).apply()
            startForegroundService(Intent(this, AgentService::class.java)
                .putExtra("url", url.text.toString()).putExtra("token", token.text.toString()))
        }
        button("Send typed instruction") { svc { prompt.text.toString().let { t -> instanceSend(t) } } }
        button("Talk (push to talk)") { svc { talk() } }

        TextView(this).apply { text = "\nProbes: run each, then note what your watch did"; root.addView(this) }
        button("1. Route audio to watch + speak test") {
            startForegroundService(Intent(this, AgentService::class.java).putExtra("route", true))
            ui.postDelayed({ svc { probeSpeak() } }, 1500)
        }
        button("2. Media buttons (press watch music controls)") { log("media session is live: press play/next/prev on the watch music screen") }
        button("3. Notification mirror test") { Notifier(this).card(3000, "Probe", "Watch text test: did this reach your watch?"); log("posted notification") }
        button("4a. Call trick (self-managed)") { CallTrick.ring(this, true, "Approve: run tests?") }
        button("4b. Call trick (calling account)") { CallTrick.ring(this, false, "Approve: run tests?") }

        logView = TextView(this).apply { textSize = 12f; setTextIsSelectable(true) }
        scroll = ScrollView(this).apply { addView(logView) }
        root.addView(scroll, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        setContentView(root)

        AgentService.sink = { line -> ui.post { logView.append("$line\n"); scroll.post { scroll.fullScroll(ScrollView.FOCUS_DOWN) } } }
        requestPermissions(arrayOf(
            Manifest.permission.RECORD_AUDIO, Manifest.permission.POST_NOTIFICATIONS, Manifest.permission.BLUETOOTH_CONNECT
        ), 1)
    }

    private fun AgentService.instanceSend(text: String) = typed(text)

    private fun log(s: String) { logView.append("$s\n") }
}
