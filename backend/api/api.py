from fastapi import APIRouter
from api.routes import router

api_router = APIRouter(prefix="/api")
api_router.include_router(router)

