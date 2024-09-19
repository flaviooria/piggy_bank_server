from dotenv import find_dotenv, load_dotenv
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str
    API_VERSION: str | None = "/api/v1"

    POSTGRES_HOST: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DBNAME: str
    POSTGRES_PORT: str = "5432"

    PG_URI_DB: str | None = None

    SECRET_KEY: str

    EXPIRES_ACCESS_TOKEN: str
    EXPIRES_REFRESH_TOKEN: str

    SMTP_HOST: str | None = None
    SMTP_PORT: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_SSL: bool | None = False
    SMTP_TLS: bool | None = False

    @computed_field
    def uri_db_postgress(self) -> str:
        if self.PG_URI_DB is not None:
            return self.PG_URI_DB

        return MultiHostUrl.build(
            scheme="postgres",
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DBNAME,
            port=int(self.POSTGRES_PORT),
        ).unicode_string()


load_dotenv(dotenv_path=find_dotenv(".env"))
settings = Settings()
