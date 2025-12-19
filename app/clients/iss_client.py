from app.clients.http_client import ExternalHttpClient

ISS_NOW_URL = "http://api.open-notify.org/iss-now.json"

class IssClient:
    def __init__(self, http: ExternalHttpClient):
        self.http = http

    async def fetch_now(self) -> dict:
        return await self.http.get_json(ISS_NOW_URL)
