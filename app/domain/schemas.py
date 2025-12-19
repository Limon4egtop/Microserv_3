from datetime import datetime
from pydantic import BaseModel, Field

class ApiError(BaseModel):
    code: str
    message: str

class FetchQuery(BaseModel):
    # пример запроса: выборка по дате/лимиту (для совместимости со стилем REST-ручек)
    limit: int = Field(default=1, ge=1, le=100)
    at: datetime | None = Field(default=None, description="timestamp for fetched_at / updated_at demo")

class IssPosition(BaseModel):
    latitude: float
    longitude: float
    timestamp: int

class FetchResponse(BaseModel):
    source: str
    fetched_at: datetime
    data: dict
    cached: bool = False
