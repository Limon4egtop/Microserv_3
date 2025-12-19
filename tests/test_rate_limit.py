import pytest
from fastapi.testclient import TestClient
from app.main import create_app
import fakeredis

class DummyRedis(fakeredis.FakeRedis):
    pass

@pytest.fixture()
def client(monkeypatch):
    app = create_app()
    # подменяем redis на fakeredis для детерминизма
    app.state.app_state.redis = DummyRedis(decode_responses=True)
    return TestClient(app)

def test_rate_limit_allows_some(client):
    # burst=10 (default). 5 запросов точно пройдут
    for _ in range(5):
        r = client.get("/health")
        assert r.status_code == 200

def test_rate_limit_blocks_when_exceeded(client, monkeypatch):
    # настроим очень маленький burst и rps через состояние
    app = client.app
    app.user_middleware.clear()
    from app.middlewares.rate_limit import RateLimitMiddleware
    app.add_middleware(RateLimitMiddleware, redis=app.state.app_state.redis, rps=0.0, burst=1, key_prefix="rl:test:")

    # 1-й проходит
    assert client.get("/health").status_code == 200
    # 2-й блокируется
    assert client.get("/health").status_code == 429
