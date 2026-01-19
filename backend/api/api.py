from .routes.health import router as healthRouter
from .routes.transcript import router as transcriptRouter
from .websockets.streaming import router as streamingRouter
from fastapi import APIRouter

router=APIRouter()
router.include_router(healthRouter)
router.include_router(transcriptRouter)
api_router = APIRouter(prefix="/api")
api_router.include_router(router)

wsRouter=APIRouter()
wsRouter.include_router(streamingRouter)
ws_router=APIRouter(prefix="/ws")
ws_router.include_router(wsRouter)

