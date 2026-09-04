from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://lamaris:change-me@localhost:5432/lamaris"
    jwt_secret: str = "change-me-in-production"
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:5173,https://tarieciphertech.github.io"

    upload_dir: str = "uploads"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_storage_bucket: str = "property-images"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def supabase_storage_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)

    @property
    def supabase_storage_public_base_url(self) -> str:
        return f"{self.supabase_url.rstrip('/')}/storage/v1/object/public/{self.supabase_storage_bucket}"

    def validate_production(self) -> None:
        if self.environment.lower() != "production":
            return
        missing = []
        if not self.database_url or "change-me" in self.database_url:
            missing.append("DATABASE_URL")
        if not self.jwt_secret or self.jwt_secret == "change-me-in-production":
            missing.append("JWT_SECRET")
        if not self.supabase_url:
            missing.append("SUPABASE_URL")
        if not self.supabase_service_role_key:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")
        if missing:
            raise RuntimeError("Missing required production environment variables: " + ", ".join(missing))


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_production()
    return settings
