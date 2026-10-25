package dev.wristagent

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.RemoteInput
import android.content.Context
import android.content.Intent

/** Notifications are what the Noise watch mirrors, so every card goes through here. */
class Notifier(private val ctx: Context) {
    private val nm = ctx.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

    init {
        nm.createNotificationChannel(NotificationChannel(CH, "Agent", NotificationManager.IMPORTANCE_HIGH))
    }

    fun card(id: Int, title: String, text: String) {
        nm.notify(id, base(title, text).build())
    }

    /** Approval notification with Approve / Deny / Modify (reply) actions. */
    fun approval(approvalId: String, title: String, text: String) {
        val b = base(title, text).setOngoing(true)
        b.addAction(action(approvalId, "approve", "Approve"))
        b.addAction(action(approvalId, "deny", "Deny"))
        val reply = Notification.Action.Builder(
            null, "Modify",
            PendingIntent.getBroadcast(
                ctx, approvalId.hashCode() + 3,
                Intent(ctx, ActionReceiver::class.java).setAction(ACTION).putExtra("id", approvalId).putExtra("decision", "modify"),
                PendingIntent.FLAG_MUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
            )
        ).addRemoteInput(RemoteInput.Builder("feedback").setLabel("What should change?").build()).build()
        b.addAction(reply)
        nm.notify(APPROVAL_ID, b.build())
    }

    fun clearApproval() = nm.cancel(APPROVAL_ID)

    fun foreground(text: String): Notification = base("Wrist Agent", text).setOngoing(true).build()

    private fun action(approvalId: String, decision: String, label: String): Notification.Action {
        val pi = PendingIntent.getBroadcast(
            ctx, approvalId.hashCode() + decision.hashCode(),
            Intent(ctx, ActionReceiver::class.java).setAction(ACTION).putExtra("id", approvalId).putExtra("decision", decision),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        return Notification.Action.Builder(null, label, pi).build()
    }

    private fun base(title: String, text: String) =
        Notification.Builder(ctx, CH)
            .setSmallIcon(android.R.drawable.stat_notify_chat)
            .setContentTitle(title)
            .setContentText(text)
            .setStyle(Notification.BigTextStyle().bigText(text))
            .setCategory(Notification.CATEGORY_MESSAGE)

    companion object {
        const val CH = "agent"
        const val ACTION = "dev.wristagent.DECISION"
        const val APPROVAL_ID = 1001
    }
}
