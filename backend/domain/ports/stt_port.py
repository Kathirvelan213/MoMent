from typing import Protocol
from pydantic import BaseModel

class AudioInput(BaseModel):
    audio_path: str

class STTPort(Protocol):
    def process_meeting(self, meeting_id: str) -> str | None:
        ...

