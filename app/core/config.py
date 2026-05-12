from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Exchange Rate Analyzer"
    environment: str = "local"
    frontend_origin: str = "http://localhost:5173"
    admin_username: str = "admin"
    admin_password: str = "change-me"
    jwt_secret_key: str = "change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    frankfurter_base_url: str = "https://api.frankfurter.dev/v1"
    cache_ttl_seconds: int = 600
    rate_limit_per_minute: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()