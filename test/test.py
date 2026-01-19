import asyncio
import websockets
import numpy as np
import soundfile as sf
import librosa
import time

WS_URL = "ws://localhost:8000/ws/audio?meeting_id=test-meeting-1"
AUDIO_FILE = "test/sample.mp3"

TARGET_SR = 16000
CHUNK_DURATION = 0.03  # 30 ms
CHUNK_SIZE = int(TARGET_SR * CHUNK_DURATION)

async def stream_audio():
    # Load audio (any sample rate)
    audio, sr = sf.read(AUDIO_FILE)

    # Convert to mono if stereo
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Resample if needed
    if sr != TARGET_SR:
        print(f"Resampling from {sr} Hz → {TARGET_SR} Hz")
        audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

    # Convert float32 → int16 PCM
    audio = np.clip(audio, -1.0, 1.0)
    audio_int16 = (audio * 32767).astype(np.int16)

    async with websockets.connect(WS_URL) as ws:
        print("Connected to WebSocket")

        for i in range(0, len(audio_int16), CHUNK_SIZE):
            chunk = audio_int16[i:i + CHUNK_SIZE]

            if len(chunk) == 0:
                break

            await ws.send(chunk.tobytes())
            time.sleep(CHUNK_DURATION)

        print("Finished streaming audio")

asyncio.run(stream_audio())
