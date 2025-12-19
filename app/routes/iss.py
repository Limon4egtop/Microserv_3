from fastapi import APIRouter, Depends
from app.handlers.iss import get_iss_handler
from app.config.deps import get_app_state
from app.domain.schemas import FetchQuery

router = APIRouter()

@router.get("/fetch")
async def fetch_iss(q: FetchQuery = Depends(), h=Depends(get_iss_handler)):
    # поведение совместимое: возвращаем JSON с данными + метаданными
    return await h.fetch(q)

@router.get("/cached")
async def cached_iss(q: FetchQuery = Depends(), h=Depends(get_iss_handler)):
    return await h.cached(q)
