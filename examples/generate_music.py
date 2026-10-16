"""examples/generate_music.py

مثال سادهٔ تولید موسیقی با استفاده از Audiocraft / MusicGen.

توجه: API ممکن است با زمان تغییر کند؛ اگر اجرای مستقیم خطا داد، به مستندات رسمی audiocraft مراجعه کنید:
https://github.com/facebookresearch/audiocraft
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Generate music using MusicGen (audiocraft)')
    parser.add_argument('--prompt', type=str, required=True, help='Text prompt describing the music')
    parser.add_argument('--output', type=str, default='output.wav', help='Output WAV file')
    parser.add_argument('--model', type=str, default='medium', help='Model size: small | medium | large (if available)')
    args = parser.parse_args()

    try:
        # Try to import audiocraft. If the API changed, refer to the repo README.
        from audiocraft.models import MusicGen
        from audiocraft.data.audio import audio_write
    except Exception as e:
        print('خطا در وارد کردن بستهٔ audiocraft: ', e)
        print('مطمئن شوید که بسته را نصب کرده‌اید: pip install git+https://github.com/facebookresearch/audiocraft.git')
        return

    print('بارگذاری مدل (ممکن است دانلود وزن‌ها لازم باشد)...')
    # این فراخوانی ممکن است بسته به نسخهٔ audiocraft متفاوت باشد — این یک الگوی رایج است
    model = MusicGen.get_pretrained(args.model)

    # تولید (مثالی ساده)
    print(f'تولید موسیقی برای عبارت: "{args.prompt}"')
    wavs = model.generate([args.prompt])  # خروجی معمولاً لیستی از tensores یا آرایه‌های numpy

    # تابع نوشتن فایل (API ممکن است نام متفاوتی داشته باشد)
    try:
        # اگر wavs یک numpy array یا tensor است، آن را به فایل بنویسید
        audio_write(args.output, wavs[0], model.sample_rate)
        print('فایل خروجی نوشته شد:', args.output)
    except Exception as e:
        print('خطا در نوشتن فایل خروجی:', e)


if __name__ == '__main__':
    main()
