from fastapi import WebSocket, APIRouter

router = APIRouter()

audio_buffer = []

@router.websocket("/audio")
async def receive_audio(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            chunk = await websocket.receive_bytes()
            audio_buffer.append(chunk)
    except:
        await websocket.close()

@router.get("/getBuffer")
async def display():
    total_bytes = sum(len(chunk) for chunk in audio_buffer)
    return {
        "chunks": len(audio_buffer),
        "total_bytes": total_bytes,
        "approx_seconds": round(total_bytes / (16000 * 2), 2)
    }