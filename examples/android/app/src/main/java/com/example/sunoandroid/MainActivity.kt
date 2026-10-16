package com.example.sunoandroid

import android.media.MediaPlayer
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private val client = OkHttpClient()

    // For quick local testing replace PROXY_KEY with the same value as PROXY_SECRET on the server.
    // In production, do NOT store secrets in the app.
    private val PROXY_KEY: String? = "replace_with_proxy_secret_for_testing"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btn = findViewById<Button>(R.id.generateButton)
        val status = findViewById<TextView>(R.id.statusText)

        btn.setOnClickListener {
            status.text = "در حال تولید..."
            val endpoint = "http://10.0.2.2:8000/generate"
            generateAudio(endpoint, "a calm piano melody") { success ->
                runOnUiThread { status.text = if (success) "تکمیل" else "خطا" }
            }
        }
    }

    private fun generateAudio(endpoint: String, prompt: String, callback: (Boolean) -> Unit) {
        val json = "{\"prompt\": \"$prompt\"}"
        val body = RequestBody.create(MediaType.get("application/json"), json)
        val reqBuilder = Request.Builder()
            .url(endpoint)
            .post(body)

        // Add proxy key header for simple auth
        PROXY_KEY?.let { reqBuilder.addHeader("X-API-KEY", it) }

        val req = reqBuilder.build()

        client.newCall(req).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
                callback(false)
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    println("API error: ${response.code}")
                    callback(false)
                    return
                }

                val bytes = response.body?.bytes()
                if (bytes != null) {
                    try {
                        val outFile = File(filesDir, "out.wav")
                        FileOutputStream(outFile).use { it.write(bytes) }

                        runOnUiThread {
                            val mp = MediaPlayer().apply {
                                setDataSource(outFile.absolutePath)
                                prepare()
                                start()
                            }
                        }

                        callback(true)
                    } catch (e: Exception) {
                        e.printStackTrace()
                        callback(false)
                    }
                } else {
                    callback(false)
                }
            }
        })
    }
}
