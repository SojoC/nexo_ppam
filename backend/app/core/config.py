from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://nexo:nexo@db:5432/nexo"
    REDIS_URL: str = "redis://redis:6379/0"
    FIREBASE_CREDENTIALS: str = "backend/creds/serviceAccountKey.json"
    SECRET_KEY: str = "change-me"
    ENV: str = "dev"

settings = Settings()
