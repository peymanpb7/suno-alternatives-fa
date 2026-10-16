# راهنمای اجرای از اندروید (setup-android.md)

این راهنما برای توسعه‌دهندگان اندروید نوشته شده تا بتوانند به‌صورت قانونی تولید صوت/موسیقی را از طریق موبایل پیاده‌سازی کنند. دو راه کلی وجود دارد:

A) استفاده از سرویس میزبانی‌شده (پیشنهاد برای موبایل)
B) اجرای مدل روی سرور خودتان و فراخوانی از موبایل

راه A — استفاده از سرویس میزبانی‌شده (Hugging Face / Replicate / API رسمی)
دلایل انتخاب این روش برای موبایل:
- مدل‌های تولید صوت سنگین‌اند و اجرای آن‌ها روی موبایل معمولاً ممکن یا مطلوب نیست.
- سرویس میزبانی‌شده نگهداری مدل، مقیاس و امنیت را برای شما فراهم می‌کند.

گام‌ها (مثال با Hugging Face Inference API)
1) ثبت‌نام در Hugging Face و دریافت API Token
2) انتخاب یک مدل تولید صوت یا TTS از https://huggingface.co/models?pipeline_tag=audio-generation
3) نمونهٔ درخواست از اندروید (Kotlin)

Gradle dependencies (module-level build.gradle.kts یا build.gradle):

dependencies {
    implementation("com.squareup.okhttp3:okhttp:4.11.0")
    implementation("com.squareup.okio:okio:3.5.0")
}

نمونهٔ کد Kotlin برای فراخوانی و ذخیره جواب WAV با OkHttp:

```kotlin
// examples/android/MainActivity.kt
package com.example.sunoandroid

import android.media.MediaPlayer
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import java.io.FileOutputStream
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private val client = OkHttpClient()
    private val hfToken = "YOUR_HUGGINGFACE_API_TOKEN" // امن نگه دارید - نباید در کد عمومی قرار گیرد

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // layout ساده با یک دکمه برای تولید و پخش
        setContentView(R.layout.activity_main)

        // مثال فراخوانی پس از فشردن دکمه
        findViewById<Button>(R.id.generateButton).setOnClickListener {
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
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    println("API error: ${response.code}")
                    return
                }

                // پاسخ احتمالاً باینری (wav) است یا base64 بسته به مدل
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
```

نکات امنیتی
- هرگز توکن API را داخل کد منبع عمومی نگذارید. از Remote Config یا سرور واسط استفاده کنید.
- برای استفادهٔ در محصول نهایی، باید نرخ محدودیت (rate limits)، هزینه و شرایط استفادهٔ سرویس را بررسی کنید.

راه B — اجرای مدل روی سرور شما و فراخوانی از موبایل
- اگر نیاز به کنترل بیشتر دارید یا از مدل‌های متن‌باز استفاده می‌کنید، یک سرور میانی راه‌اندازی کنید (Flask/Express/FastAPI) که مدل را بارگذاری کرده و درخواست‌های اندروید را هندل کند.
- مزایا: می‌توانید از GPUهای قدرتمند استفاده کنید، مدیریت صف و caching انجام دهید.
- معایب: هزینهٔ سرور و نگهداری.

نمونهٔ سادهٔ سرور (Flask) برای تولید و بازگرداندن فایل WAV در مسیر /generate
- توضیحات کامل در README و examples/server

خلاصه
- برای شروع سریع و موبایل محور، از APIهای میزبانی‌شده استفاده کنید.
- برای کنترل بیشتر، مدل را روی سرور خود اجرا کنید و موبایل را به‌عنوان کلاینت نگه دارید.
