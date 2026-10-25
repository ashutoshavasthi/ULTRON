package dev.wristagent

import android.app.RemoteInput
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

/** Handles taps on the Approve / Deny / Modify notification actions. */
class ActionReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val id = intent.getStringExtra("id") ?: return
        val decision = intent.getStringExtra("decision") ?: return
        val feedback = RemoteInput.getResultsFromIntent(intent)?.getCharSequence("feedback")?.toString()
        AgentService.instance?.decide(id, decision, feedback)
    }
}
