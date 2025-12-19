from fastapi import APIRouter
from app.routes.health import router as health_router
from app.routes.iss import router as iss_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(iss_router, prefix="/iss", tags=["iss"])
