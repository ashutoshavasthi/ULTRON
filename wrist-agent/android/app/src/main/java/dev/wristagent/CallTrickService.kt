package dev.wristagent

import android.content.ComponentName
import android.content.Context
import android.net.Uri
import android.os.Bundle
import android.telecom.Connection
import android.telecom.ConnectionRequest
import android.telecom.ConnectionService
import android.telecom.DisconnectCause
import android.telecom.PhoneAccount
import android.telecom.PhoneAccountHandle
import android.telecom.TelecomManager

/**
 * UNVERIFIED on the Noise watch: raises an incoming "call" whose caller name is the
 * question. Answer = approve, Reject = deny. Two variants because watches differ:
 *  - self-managed: no user setup, but the system doesn't ring Bluetooth for it
 *  - calling-account: user must enable it in Phone settings; behaves like a SIM call
 */
object CallTrick {
    var onAnswer: (() -> Unit)? = null
    var onReject: (() -> Unit)? = null
    var log: (String) -> Unit = {}

    private fun handle(ctx: Context, selfManaged: Boolean) = PhoneAccountHandle(
        ComponentName(ctx, CallTrickService::class.java), if (selfManaged) "wrist-self" else "wrist-provider"
    )

    fun register(ctx: Context, selfManaged: Boolean) {
        val tm = ctx.getSystemService(Context.TELECOM_SERVICE) as TelecomManager
        val caps = if (selfManaged) PhoneAccount.CAPABILITY_SELF_MANAGED else PhoneAccount.CAPABILITY_CALL_PROVIDER
        tm.registerPhoneAccount(
            PhoneAccount.builder(handle(ctx, selfManaged), if (selfManaged) "Wrist Agent" else "Wrist Agent (calling account)")
                .setCapabilities(caps)
                .addSupportedUriScheme("agent")
                .build()
        )
    }

    fun ring(ctx: Context, selfManaged: Boolean, title: String) {
        register(ctx, selfManaged)
        val tm = ctx.getSystemService(Context.TELECOM_SERVICE) as TelecomManager
        val extras = Bundle().apply {
            putString("title", title)
            putBoolean("self", selfManaged)
            putParcelable(TelecomManager.EXTRA_INCOMING_CALL_ADDRESS, Uri.fromParts("agent", title.take(30), null))
        }
        try {
            tm.addNewIncomingCall(handle(ctx, selfManaged), extras)
            log("incoming call raised (${if (selfManaged) "self-managed" else "calling-account"})")
        } catch (e: Exception) {
            log("call trick failed: ${e.message}")
        }
    }
}

class CallTrickService : ConnectionService() {
    override fun onCreateIncomingConnection(account: PhoneAccountHandle?, request: ConnectionRequest?): Connection {
        val title = request?.extras?.getString("title") ?: "Approve?"
        val self = request?.extras?.getBoolean("self") ?: true
        val conn = object : Connection() {
            override fun onAnswer() { CallTrick.log("call ANSWERED"); CallTrick.onAnswer?.invoke(); end() }
            override fun onAnswer(videoState: Int) = onAnswer()
            override fun onReject() { CallTrick.log("call REJECTED"); CallTrick.onReject?.invoke(); end() }
            override fun onDisconnect() { CallTrick.log("call disconnected"); end() }
            private fun end() { setDisconnected(DisconnectCause(DisconnectCause.LOCAL)); destroy() }
        }
        if (self) conn.connectionProperties = Connection.PROPERTY_SELF_MANAGED
        conn.setAddress(Uri.fromParts("agent", title.take(30), null), TelecomManager.PRESENTATION_ALLOWED)
        conn.setCallerDisplayName(title.take(40), TelecomManager.PRESENTATION_ALLOWED)
        conn.setRinging()
        return conn
    }
}
