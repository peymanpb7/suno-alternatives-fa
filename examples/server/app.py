from fastapi import FastAPI, Request, Response, HTTPException
import io
import os

app = FastAPI()

# Configure model name via env var; default to 'medium' for MusicGen if available
MODEL_NAME = os.environ.get("MODEL_NAME", "medium")

# Try to import audiocraft; if not available, return helpful error
try:
    from audiocraft.models import MusicGen
    from audiocraft.data.audio import audio_write
except Exception as e:
    MusicGen = None
    audio_write = None
    _import_error = e

model = None

@app.on_event("startup")
def load_model():
    global model
    if MusicGen is None:
        print("audiocraft (MusicGen) is not available:", _import_error)
        return
    try:
        print(f"Loading MusicGen pretrained model: {MODEL_NAME}")
        model = MusicGen.get_pretrained(MODEL_NAME)
        print("Model loaded.")
    except Exception as e:
        print("Failed to load model:", e)
        model = None

@app.post("/generate")
async def generate(request: Request):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded on server. Check logs and dependencies.")

    payload = await request.json()
    prompt = payload.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Missing 'prompt' in JSON body")

    # Generate audio
    try:
        wavs = model.generate([prompt])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")

    # Write WAV to buffer
    buf = io.BytesIO()
    try:
        audio_write(buf, wavs[0], model.sample_rate, format="wav")
    except Exception as e:
        # Fallback: try to handle numpy/tensor manually
        raise HTTPException(status_code=500, detail=f"Failed to write audio buffer: {e}")

    return Response(content=buf.getvalue(), media_type="audio/wav")
