from fastapi import WebSocket, APIRouter
from starlette.websockets import WebSocketDisconnect
import os
import numpy as np
import soundfile as sf
import librosa
from shared_state import meeting_states

router = APIRouter()

# Import will be set by dependency injection in main.py, but for now we'll access the singleton
orchestrator_instance = None
BASE_DIR = "recordings"


def convert_mp3_to_pcm(mp3_path: str, pcm_path: str) -> None:
    """Convert an MP3 file to 16kHz mono 16-bit PCM using soundfile/librosa."""
    if not os.path.exists(mp3_path):
        print(f"[WebSocket] MP3 file not found for conversion: {mp3_path}")
        return

    try:
        # Load audio
        audio, sr = sf.read(mp3_path)
        
        # Convert to mono if stereo
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)
        
        # Resample to 16kHz if needed
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        
        # Convert to int16 PCM
        audio = np.clip(audio, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Save as PCM
        audio_int16.tofile(pcm_path)
        print(f"[WebSocket] Converted MP3 to PCM: {mp3_path} -> {pcm_path} ({len(audio_int16)} samples)")
    except Exception as e:
        print(f"[WebSocket] Failed to convert MP3 to PCM: {e}")


@router.websocket("/audio")
async def receive_audio(websocket: WebSocket, meeting_id: str):
    await websocket.accept()

    meeting_dir = os.path.join(BASE_DIR, meeting_id)
    os.makedirs(meeting_dir, exist_ok=True)

    mp3_path = os.path.join(meeting_dir, "audio.mp3")
    pcm_path = os.path.join(meeting_dir, "audio.pcm")

    meeting_states.setdefault(meeting_id, {"last_processed_bytes": 0})

    with open(mp3_path, "ab") as f:
        try:
            while True:
                chunk = await websocket.receive_bytes()
                f.write(chunk)
        except WebSocketDisconnect:
            # Normal client disconnect (code 1000) – Starlette will close the socket.
            pass
        finally:
            # Convert the received MP3 to PCM and then process remaining audio
            print(f"[WebSocket] Connection closed for {meeting_id}, converting and processing remaining audio...")
            convert_mp3_to_pcm(mp3_path, pcm_path)
            if orchestrator_instance:
                orchestrator_instance.process_meeting_workflow(meeting_id, force_remaining=True)
            # Remove meeting from state so polling stops
            if meeting_id in meeting_states:
                del meeting_states[meeting_id]
