# راهنمای اجرای محلی (setup-local.md)

این راهنما گام‌به‌گام نحوهٔ راه‌اندازی محیط محلی برای اجرای مدل‌های تولید موسیقی متن‌باز را توضیح می‌دهد. این مثال روی MusicGen (audiocraft) تمرکز دارد ولی مفاهیم عمومی برای سایر پروژه‌ها نیز کاربردی است.

ملزومات پیش‌نیاز
- Python 3.8+ (توصیه شده 3.9 یا 3.10)
- حداقل یک GPU با CUDA (برای تولید با کیفیت) یا CPU (برای آزمایش‌های ساده)
- فضای دیسک کافی برای مدل‌ها (چند صد مگابایت تا چند گیگابایت بسته به مدل)

گام‌ها
1) ایجاد محیط مجازی

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.\.venv\Scripts\activate  # Windows (PowerShell)

pip install --upgrade pip
```

2) نصب PyTorch
- به صفحهٔ https://pytorch.org/ بروید و دستور مناسب برای CUDA یا CPU را کپی کنید.
- مثال (برای CUDA 11.8):

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

3) نصب Audiocraft (MusicGen)

```bash
pip install git+https://github.com/facebookresearch/audiocraft.git
```

> نکته: بسته به زمان و تغییرات upstream این دستور ممکن است تغییر کند — مستندات رسمی audiocraft را بررسی کنید.

4) نصب بقیهٔ وابستگی‌ها

```bash
pip install -r examples/requirements.txt
```

5) اجرای مثال

```bash
python examples/generate_music.py --prompt "a calm piano melody" --output out.wav
```

در صورت بروز خطا
- پیام خطا را کامل در این مخزن (Issue) ثبت کنید و ما به شما کمک می‌کنیم.
- اگر مشکل مربوط به CUDA / درایور است، نسخهٔ درایور و خروجی nvidia-smi را ارائه دهید.

توضیحات بیشتر
- اجرای مدل‌ها روی CPU معمولاً بسیار کند است. برای نتایج واقعی و سریع از GPU استفاده کنید.
- برخی از مدل‌ها نیاز به دانلود وزن‌های از پیش‌آموزش‌دیده دارند؛ این دانلود ممکن است چند گیگابایت باشد.
