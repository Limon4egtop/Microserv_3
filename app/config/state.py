from dataclasses import dataclass
from redis import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config.settings import Settings

@dataclass
class AppState:
    redis: Redis
    db_sessionmaker: async_sessionmaker[AsyncSession] | None

def create_app_state(settings: Settings) -> AppState:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)

    db_sessionmaker = None
    if settings.database_url:
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        db_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    return AppState(redis=redis, db_sessionmaker=db_sessionmaker)
