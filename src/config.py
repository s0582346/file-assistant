from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str

    database_url: str
    database_url_sync: str

    app_secret: str = "dev-secret-change-me"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""

    resources_dir: Path = PROJECT_ROOT / "resources"


settings = Settings()
