package dev.wristagent

import android.content.Context
import android.content.Intent
import android.media.AudioAttributes
import android.media.AudioDeviceInfo
import android.media.AudioManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import java.util.Locale

/**
 * Speech in/out. When a Bluetooth headset-profile device (a watch with calling) is
 * connected, audio is routed to it so its mic and speaker are used.
 */
class Voice(private val ctx: Context, private val onHeard: (String) -> Unit, private val log: (String) -> Unit) {

    private val main = Handler(Looper.getMainLooper())
    private val audio = ctx.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    private var tts: TextToSpeech? = null
    private var ttsReady = false
    private var recognizer: SpeechRecognizer? = null
    private var onSpeechDone: (() -> Unit)? = null

    fun start() {
        tts = TextToSpeech(ctx) { status ->
            ttsReady = status == TextToSpeech.SUCCESS
            tts?.language = Locale.getDefault()
            tts?.setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_VOICE_COMMUNICATION)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()
            )
            log(if (ttsReady) "tts ready" else "tts init failed")
        }
    }

    /** Route call audio to a connected Bluetooth SCO device. Returns the device name or null. */
    fun routeToWatch(): String? {
        val sco = audio.availableCommunicationDevices.firstOrNull { it.type == AudioDeviceInfo.TYPE_BLUETOOTH_SCO }
            ?: return null // no watch connected: leave the phone's own mic and speaker alone
        audio.mode = AudioManager.MODE_IN_COMMUNICATION
        return if (audio.setCommunicationDevice(sco)) sco.productName.toString() else null
    }

    fun releaseRoute() {
        audio.clearCommunicationDevice()
        audio.mode = AudioManager.MODE_NORMAL
    }

    fun speak(text: String, then: (() -> Unit)? = null) {
        if (!ttsReady) return log("tts not ready")
        routeToWatch()
        onSpeechDone = then
        tts?.setOnUtteranceProgressListener(object : android.speech.tts.UtteranceProgressListener() {
            override fun onStart(id: String?) {}
            override fun onError(id: String?) { main.post { onSpeechDone?.invoke() } }
            override fun onDone(id: String?) { main.post { onSpeechDone?.invoke() } }
        })
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "u${System.nanoTime()}")
    }

    fun stopSpeaking() {
        tts?.stop()
    }

    fun listen() = main.post {
        stopSpeaking()
        routeToWatch()
        if (!SpeechRecognizer.isRecognitionAvailable(ctx)) return@post log("no speech recognizer on this phone")
        recognizer?.destroy()
        recognizer = SpeechRecognizer.createSpeechRecognizer(ctx).also { r ->
            r.setRecognitionListener(object : RecognitionListener {
                override fun onResults(results: Bundle) {
                    val text = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull()
                    if (text.isNullOrBlank()) log("heard nothing") else { log("heard: $text"); onHeard(text) }
                }
                override fun onError(error: Int) { log("stt error $error") }
                override fun onReadyForSpeech(params: Bundle?) { log("listening...") }
                override fun onBeginningOfSpeech() {}
                override fun onRmsChanged(rmsdB: Float) {}
                override fun onBufferReceived(buffer: ByteArray?) {}
                override fun onEndOfSpeech() {}
                override fun onPartialResults(partialResults: Bundle?) {}
                override fun onEvent(eventType: Int, params: Bundle?) {}
            })
            r.startListening(Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, false)
            })
        }
    }

    fun shutdown() {
        main.post { recognizer?.destroy() }
        tts?.shutdown()
        releaseRoute()
    }
}
