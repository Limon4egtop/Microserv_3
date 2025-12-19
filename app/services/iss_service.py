from datetime import datetime, timezone
from app.clients.iss_client import IssClient
from app.repo.cache_repo import CacheRepo
from app.domain.schemas import FetchQuery, FetchResponse

class IssService:
    def __init__(self, client: IssClient, cache: CacheRepo):
        self.client = client
        self.cache = cache

    async def fetch(self, q: FetchQuery) -> FetchResponse:
        data = await self.client.fetch_now()
        return FetchResponse(
            source="ISS",
            fetched_at=datetime.now(timezone.utc),
            data=data,
            cached=False,
        )

    async def cached(self, q: FetchQuery) -> FetchResponse:
        key = f"iss:now:limit={q.limit}"
        cached = self.cache.get_json(key)
        if cached:
            return FetchResponse(
                source="ISS",
                fetched_at=datetime.now(timezone.utc),
                data=cached,
                cached=True,
            )
        data = await self.client.fetch_now()
        self.cache.set_json(key, data, ttl_s=30)
        return FetchResponse(
            source="ISS",
            fetched_at=datetime.now(timezone.utc),
            data=data,
            cached=False,
        )
