package dev.wristagent

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import org.json.JSONObject
import java.util.concurrent.TimeUnit

/** WebSocket client for the wrist-agent gateway. Callbacks arrive on OkHttp's thread. */
class Gateway(private val url: String, private val token: String, private val listener: Listener) {

    interface Listener {
        fun onStatus(text: String)
        fun onMessage(msg: JSONObject)
    }

    private val http = OkHttpClient.Builder().pingInterval(20, TimeUnit.SECONDS).build()
    private var ws: WebSocket? = null

    fun connect() {
        ws = http.newWebSocket(Request.Builder().url(url).build(), object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                webSocket.send(JSONObject().put("type", "hello").put("token", token).toString())
                listener.onStatus("connected")
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                runCatching { listener.onMessage(JSONObject(text)) }
            }

            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                listener.onStatus("closed $code $reason")
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                listener.onStatus("failed: ${t.message}")
            }
        })
    }

    fun send(obj: JSONObject) {
        ws?.send(obj.toString())
    }

    fun close() {
        ws?.close(1000, "bye")
        http.dispatcher.executorService.shutdown()
    }
}
