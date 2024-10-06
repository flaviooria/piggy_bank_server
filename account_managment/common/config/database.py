from fastapi import FastAPI
from tortoise import generate_config
from tortoise.contrib.fastapi import register_tortoise

from account_managment.common.config.settings import settings


def InitDb(app: FastAPI):
    config = generate_config(
        db_url=settings.uri_db_postgres,
        app_modules={"models": ["account_managment.entities.entities"]},
    )

    register_tortoise(app, config=config, generate_schemas=True, add_exception_handlers=True)
