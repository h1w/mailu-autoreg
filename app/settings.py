from functools import lru_cache

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    api_token: str | None = None
    start_num: int | None = None
    accounts_count: int | None = None
    domain: str | None = None
    title_format: str | None = None
    title_name: str | None = None
    user_comment: str | None = None
    pass_length: int | None = None
    api_endpoint_user_create: str | None = None

    def validate_settings(self) -> None:
        for field_name, field_value in self.model_dump().items():
            if field_value is None:
                raise ValueError(f"Field '{field_name}' can't be empty")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


@lru_cache
def get_app_settings() -> AppSettings:
    app_settings = AppSettings()
    app_settings.validate_settings()
    return app_settings
