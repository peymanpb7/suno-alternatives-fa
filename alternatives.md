# alternatives.md

این فایل فهرستی از جایگزین‌های متن‌باز برای تولید موسیقی و صوت است که می‌توانید به‌صورت قانونی و محلی اجرا کنید.

1) MusicGen / Audiocraft (Meta / Facebook)
- توضیح: مدل تولید موسیقی از Meta که کیفیت خوبی برای تولید ملودی و آهنگ دارد.
- لینک: https://github.com/facebookresearch/audiocraft
- یادداشت: معمولاً نیاز به PyTorch و منابع GPU دارد. مستندات رسمی را برای نسخه‌ها و API ببینید.

2) AudioLDM
- توضیح: چارچوب تبدیل متن به موسیقی/صدا با رویکردهای مبتنی بر diffusion.
- لینک: https://github.com/haoheliu/AudioLDM

3) Riffusion
- توضیح: تولید موسیقی با تبدیل طیف‌نگاره به تصویر و استفاده از مدل‌های diffusion تصویری.
- لینک: https://github.com/riffusion/riffusion

4) Hugging Face Models
- توضیح: Hugging Face میزبان مدل‌های متعددی از جمله مدل‌های صوتی متن‌باز است؛ می‌توانید جستجو کرده و مدل مناسب را پیدا کنید.
- لینک: https://huggingface.co/models?pipeline_tag=audio-generation

5) Coqui (برای TTS)
- توضیح: کتابخانهٔ متن‌باز برای تبدیل متن به گفتار (TTS) با چندین مدل از پیش‌آموزش‌دیده.
- لینک: https://github.com/coqui-ai/TTS

راهنمایی برای انتخاب
- اگر دنبال کیفیت بالا و آماده‌سازی سریع هستید و GPU دارید: MusicGen/audiocraft را امتحان کنید.
- اگر دنبال راهکارهای سبک‌تر یا تحقیقاتی هستید: AudioLDM یا مدل‌های Hugging Face را بررسی کنید.
- همیشه مستندات رسمی هر پروژه را مطالعه کنید و به مجوز (license) توجه داشته باشید.
