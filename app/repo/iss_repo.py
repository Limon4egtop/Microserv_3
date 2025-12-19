from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class IssRepo:
    def __init__(self, session: AsyncSession | None):
        self.session = session

    async def ensure_schema(self):
        if not self.session:
            return
        await self.session.execute(text("""
        CREATE TABLE IF NOT EXISTS iss_fetch_log (
            id SERIAL PRIMARY KEY,
            fetched_at TIMESTAMPTZ NOT NULL,
            payload JSONB NOT NULL
        );
        """))
        await self.session.commit()

    async def insert_log(self, fetched_at: datetime, payload: dict):
        if not self.session:
            return
        await self.session.execute(
            text("INSERT INTO iss_fetch_log (fetched_at, payload) VALUES (:fetched_at, :payload::jsonb)"),
            {"fetched_at": fetched_at, "payload": json.dumps(payload, ensure_ascii=False)},
        )
        await self.session.commit()
