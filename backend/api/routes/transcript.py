from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

BASE_DIR = "recordings"

@router.get("/transcript/{meeting_id}")
def get_transcript(meeting_id: str):
    transcript_path = os.path.join(BASE_DIR, meeting_id, "transcript.txt")
    
    if not os.path.exists(transcript_path):
        raise HTTPException(status_code=404, detail=f"Transcript not found for meeting {meeting_id}")
    
    with open(transcript_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return {"meeting_id": meeting_id, "transcript": content}
