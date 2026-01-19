import asyncio
from fastapi import FastAPI
from api.api import api_router, ws_router

from application.moments_orchestrator import MomentsOrchestrator
from application.meeting_polling import poll_meetings
from infrastructure.whisper import WhisperSTT
from infrastructure.file_handler import LocalFileHandler

app = FastAPI(
    title="AI Meeting Assistant API",
    description="for speech-to-text and MoM generation",
    version="1.0.0",
)

app.include_router(api_router)
app.include_router(ws_router)


@app.on_event("startup")
async def startup_event():
    from api.websockets import streaming
    
    stt_adapter = WhisperSTT()
    file_handler = LocalFileHandler()
    orchestrator = MomentsOrchestrator(stt_adapter, file_handler)
    
    # Make orchestrator available to websocket handler for final flush
    streaming.orchestrator_instance = orchestrator
    
    asyncio.create_task(poll_meetings(orchestrator))


@app.get("/")
def root():
    return {"message": "AI Meeting Assistant API is running"}
