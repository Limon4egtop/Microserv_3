from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = Field(default="dev", alias="APP_ENV")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    database_url: str = Field(default="", alias="DATABASE_URL")

    rate_limit_rps: float = Field(default=5.0, alias="RATE_LIMIT_RPS")
    rate_limit_burst: int = Field(default=10, alias="RATE_LIMIT_BURST")

    external_timeout_s: float = Field(default=4.0, alias="EXTERNAL_TIMEOUT_S")
