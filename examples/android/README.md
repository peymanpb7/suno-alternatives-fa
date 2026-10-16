# Android README - how to connect the sample app to your proxy

Quick steps to test on an Android emulator:

1) Run the proxy server locally (from repo/examples/server):

   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt

   # set env vars (Linux/macOS)
   export SUNO_API_URL="https://api.suno.ai/v1/generate"
   export SUNO_API_TOKEN="<YOUR_SUNO_TOKEN>"
   export PROXY_SECRET="<A_RANDOM_SECRET>"

   # run server
   uvicorn app:app --host 0.0.0.0 --port 8000

2) In the Android sample (examples/android), open project in Android Studio.
3) Update MainActivity.kt: set the PROXY_KEY value to the same PROXY_SECRET used above (for quick testing only).
   For emulator use endpoint: http://10.0.2.2:8000/generate
   For physical device, use http://<SERVER_LAN_IP>:8000/generate

4) Run the app and press "تولید و پخش". The app sends prompt to proxy, proxy forwards to Suno, returns WAV and app plays it.

Security notes:
- Do NOT hardcode API tokens or secrets in production apps. Use a secure server-side store.
- Use HTTPS for server endpoints in production.
