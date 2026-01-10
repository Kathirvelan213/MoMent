from .health import router as healthRouter
from fastapi import APIRouter

router=APIRouter()

router.include_router(healthRouter)