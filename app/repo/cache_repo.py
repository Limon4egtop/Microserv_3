import json
from redis import Redis

class CacheRepo:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_json(self, key: str):
        raw = self.redis.get(key)
        return json.loads(raw) if raw else None

    def set_json(self, key: str, value: dict, ttl_s: int):
        self.redis.setex(key, ttl_s, json.dumps(value, ensure_ascii=False))
