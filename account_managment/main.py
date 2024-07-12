from contextlib import asynccontextmanager

from fastapi import FastAPI
from raw_dbmodel import create_tables

from account_managment.accounts.models import Accounts
from account_managment.user.models import Users


@asynccontextmanager
async def lifespan_init_db(_app: FastAPI):
    print("Init db")
    create_tables([Users, Accounts])
    yield


app = FastAPI(title="Account Managment Backend",
              version="0.1.0", lifespan=lifespan_init_db)


@app.get("/health")
def health():
    return {"ok": True}
