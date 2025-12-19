from fastapi import Depends
from app.config.deps import get_settings, get_app_state
from app.clients.http_client import ExternalHttpClient
from app.clients.iss_client import IssClient
from app.repo.cache_repo import CacheRepo
from app.services.iss_service import IssService

class IssHandler:
    def __init__(self, svc: IssService):
        self.svc = svc

    async def fetch(self, q):
        return (await self.svc.fetch(q)).model_dump()

    async def cached(self, q):
        return (await self.svc.cached(q)).model_dump()

async def get_iss_handler(settings=Depends(get_settings), st=Depends(get_app_state)):
    http = ExternalHttpClient(timeout_s=settings.external_timeout_s)
    client = IssClient(http=http)
    cache = CacheRepo(redis=st.redis)
    svc = IssService(client=client, cache=cache)
    return IssHandler(svc=svc)
