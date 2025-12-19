from fastapi import FastAPI
from app.config.settings import Settings
from app.config.state import create_app_state
from app.routes import api_router
from app.middlewares.rate_limit import RateLimitMiddleware

def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(title="Cassiopeia API (Python)", version="1.0.0")
    app.state.settings = settings
    app.state.app_state = create_app_state(settings)

    app.add_middleware(
        RateLimitMiddleware,
        redis=app.state.app_state.redis,
        rps=settings.rate_limit_rps,
        burst=settings.rate_limit_burst,
        key_prefix="rl:api:",
    )

    app.include_router(api_router)
    return app

app = create_app()
