import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL")
    scheduler_interval_seconds: int = int(os.getenv("SCHEDULER_INTERVAL_SECONDS"))
    quote_api_url: str = os.getenv("QUOTE_API_URL")


settings = Settings()
