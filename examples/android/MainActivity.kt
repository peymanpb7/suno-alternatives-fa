// examples/android/MainActivity.kt
// نمونهٔ سادهٔ فایل Kotlin برای فراخوانی Hugging Face Inference API

package com.example.sunoandroid

import android.media.MediaPlayer
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private val client = OkHttpClient()
    private val hfToken = "YOUR_HUGGINGFACE_API_TOKEN"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btn = findViewById<Button>(R.id.generateButton)
        btn.setOnClickListener {
            generateAudio("a calm piano melody")
        }
    }

    private fun generateAudio(prompt: String) {
        val url = "https://api-inference.huggingface.co/models/<MODEL-ID>"
        val json = "{\"inputs\": \"$prompt\"}"
        val body = RequestBody.create(MediaType.get("application/json"), json)
        val req = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $hfToken")
            .post(body)
            .build()

        client.newCall(req).enqueue(object: Callback {
            override fun onFailure(call: Call, e: IOException) { e.printStackTrace() }
            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) { println("API error: ${response.code}"); return }
                val bytes = response.body?.bytes()
                if (bytes != null) {
                    val outFile = File(filesDir, "out.wav")
                    FileOutputStream(outFile).use { it.write(bytes) }
                    runOnUiThread {
                        val mp = MediaPlayer().apply {
                            setDataSource(outFile.absolutePath)
                            prepare()
                            start()
                        }
                    }
                }
            }
        })
    }
}
