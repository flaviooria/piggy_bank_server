from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from raw_dbmodel import create_tables

from account_managment.accounts.models import Accounts
from account_managment.api_v1 import api_v1_router
from account_managment.settings.settings import settings
from account_managment.user.domain import Users


@asynccontextmanager
async def lifespan_init_db(_app: FastAPI):
    create_tables([Users, Accounts])
    yield


app = FastAPI(title=settings.APP_NAME,
              version="0.1.0", lifespan=lifespan_init_db, docs_url=f"{settings.API_VERSION}/docs")

app.include_router(api_v1_router)


@app.get("/")
async def greeting():
    return RedirectResponse(f"{settings.API_VERSION}/docs")


@app.get("/health")
async def health():
    return {"ok": True}
