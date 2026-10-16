from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import base64

app = FastAPI(title="Suno Proxy (secure)")

# Allow local testing from Android/emulator; in production lock this down
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Required environment variables
SUNO_API_URL = os.environ.get("SUNO_API_URL")  # e.g. https://api.suno.ai/generate
SUNO_API_TOKEN = os.environ.get("SUNO_API_TOKEN")
PROXY_SECRET = os.environ.get("PROXY_SECRET")  # simple shared secret for clients

if not SUNO_API_URL or not SUNO_API_TOKEN or not PROXY_SECRET:
    print("Warning: SUNO_API_URL, SUNO_API_TOKEN or PROXY_SECRET not set. See .env.example")


@app.post("/generate")
async def generate(request: Request):
    # Simple auth: client must provide X-API-KEY header equal to PROXY_SECRET
    api_key = request.headers.get("X-API-KEY")
    if PROXY_SECRET and api_key != PROXY_SECRET:
        raise HTTPException(status_code=401, detail="Missing or invalid X-API-KEY header")

    body = await request.json()
    prompt = body.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Missing 'prompt' in JSON body")

    # Forward to Suno API
    headers = {
        "Authorization": f"Bearer {SUNO_API_TOKEN}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Forward the same body to Suno. If Suno expects different fields, adapt here.
            resp = await client.post(SUNO_API_URL, json=body, headers=headers)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Failed to reach Suno API: {e}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=f"Suno API error: {resp.text}")

    # Handle response: if binary audio returned, pass through; if JSON with base64, decode
    content_type = resp.headers.get("content-type", "")
    if content_type.startswith("audio/"):
        return Response(content=resp.content, media_type=content_type)

    # If JSON with base64 payload
    try:
        data = resp.json()
        # common field names: 'audio', 'wav', 'data'
        b64 = None
        for key in ("audio", "wav", "data"):
            if key in data and isinstance(data[key], str):
                b64 = data[key]
                break
        if b64:
            audio_bytes = base64.b64decode(b64)
            return Response(content=audio_bytes, media_type="audio/wav")
    except Exception:
        pass

    # Fallback: return raw response body
    return Response(content=resp.content, media_type=content_type or "application/octet-stream")
