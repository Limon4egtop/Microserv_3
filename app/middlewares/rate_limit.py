import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

# Token bucket in Redis (atomic via Lua).
LUA = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local rps = tonumber(ARGV[2])
local burst = tonumber(ARGV[3])

local data = redis.call('HMGET', key, 'tokens', 'ts')
local tokens = tonumber(data[1])
local ts = tonumber(data[2])

if tokens == nil then tokens = burst end
if ts == nil then ts = now end

local delta = math.max(0, now - ts)
local refill = delta * rps
tokens = math.min(burst, tokens + refill)
ts = now

local allowed = 0
if tokens >= 1 then
  tokens = tokens - 1
  allowed = 1
end

redis.call('HMSET', key, 'tokens', tokens, 'ts', ts)
redis.call('EXPIRE', key, 60)

return allowed
"""

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis, rps: float, burst: int, key_prefix: str):
        super().__init__(app)
        self.redis = redis
        self.rps = float(rps)
        self.burst = int(burst)
        self.key_prefix = key_prefix
        self._sha = None

    def _load(self):
        if self._sha is None:
            self._sha = self.redis.script_load(LUA)

    async def dispatch(self, request: Request, call_next):
        self._load()
        ip = request.client.host if request.client else "unknown"
        key = f"{self.key_prefix}{ip}"
        now = time.time()
        try:
            allowed = self.redis.evalsha(self._sha, 1, key, now, self.rps, self.burst)
        except Exception:
            # fail-open if redis issue
            allowed = 1

        if int(allowed) != 1:
            return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)

        resp: Response = await call_next(request)
        return resp
