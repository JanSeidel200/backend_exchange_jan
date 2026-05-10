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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()