from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from raw_dbmodel import create_tables

from account_managment.accounts.models import Accounts
from account_managment.settings.settings import settings
from account_managment.user.models import Users


@asynccontextmanager
async def lifespan_init_db(_app: FastAPI):
    print("Init db")
    create_tables([Users, Accounts])
    yield


app = FastAPI(title=settings.APP_NAME,
              version="0.1.0", lifespan=lifespan_init_db, docs_url=f"{settings.API_VERSION}/docs")


@app.get("/")
def gretting():
    return RedirectResponse(f"{settings.API_VERSION}/docs")


@app.get("/health")
def health():
    return {"ok": True}
