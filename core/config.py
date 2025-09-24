from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):

    # Теперь префикс (/api/v1) задаётся через настройки, 
    # а не хардкодится в коде. 
    # Это гибче — можно менять через .env.

    api_v1_prefix: str = "/api/v1"  # общий префикс для всех API версий

    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True


settings = Settings()
