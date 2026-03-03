from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    # App
    ENV: str = "dev"
    APP_BASE_URL: str = "http://localhost:8000"

    # DB
    DATABASE_URL: str

    # Redis / RQ
    REDIS_URL: str = "redis://redis:6379/0"
    RQ_DEFAULT_QUEUE: str = "default"

    # Telegram
    TELEGRAM_BOT_TOKEN: str | None = None
    TELEGRAM_CHAT_ID: str | None = None

    # SMTP
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASS: str | None = None
    SMTP_FROM: str | None = None
    EMAIL_TO: str | None = None

settings = Settings()