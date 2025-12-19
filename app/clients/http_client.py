import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class ExternalHttpClient:
    def __init__(self, timeout_s: float, user_agent: str = "CassiopeiaPython/1.0"):
        self._client = httpx.AsyncClient(timeout=timeout_s, headers={"User-Agent": user_agent})

    async def aclose(self):
        await self._client.aclose()

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.3, min=0.3, max=2.0),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError)),
    )
    async def get_json(self, url: str) -> dict:
        r = await self._client.get(url)
        r.raise_for_status()
        return r.json()
