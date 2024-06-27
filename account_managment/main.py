from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan_init_db(_app: FastAPI):
    print("Init db")
    yield


app = FastAPI(title="Account Managment Backend",
              version="0.1.0", lifespan=lifespan_init_db)


@app.get("/health")
def health():
    return {"ok": True}
