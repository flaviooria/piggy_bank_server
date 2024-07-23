import os

from dotenv import find_dotenv, load_dotenv
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True, env_file_encoding='utf-8', extra='ignore')

    APP_NAME: str
    API_VERSION: str | None = "/api/v1"

    POSTGRES_HOST: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str
    POSTGRES_PORT: str = "5432"
    DB_SCHEME: str
    DB_MOTOR: str
    DB_URI: str | None = None

    SECRET_KEY: str

    @computed_field
    def uri_db(self) -> str:
        if self.DB_URI is not None:
            return self.DB_URI

        return MultiHostUrl.build(scheme=f"postgresql+{self.DB_SCHEME}", username=self.POSTGRES_USERNAME,
                                  password=self.POSTGRES_PASSWORD, host=self.POSTGRES_HOST, path=self.POSTGRES_NAME,
                                  port=int(self.POSTGRES_PORT)).unicode_string()


env_file = ".env.production" if os.environ.get(
    "ENVIRONMENT", "local") == "production" else ".env"

load_dotenv(dotenv_path=find_dotenv(env_file))
settings = Settings()
