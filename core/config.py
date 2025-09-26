from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = True


class Settings(BaseSettings):

    # Теперь префикс (/api/v1) задаётся через настройки,
    # а не хардкодится в коде.
    # Это гибче — можно менять через .env.

    api_v1_prefix: str = "/api/v1"  # общий префикс для всех API версий
    db: DbSettings = DbSettings()


settings = Settings()
