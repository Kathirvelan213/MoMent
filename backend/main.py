from fastapi import FastAPI
from api.api import api_router

app = FastAPI(
    title="AI Meeting Assistant API",
    description="Backend for speech-to-text and MoM generation",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "AI Meeting Assistant API is running"}
