from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from account_managment.api import api_v1_router
from account_managment.common import InitDb, settings

app = FastAPI(title=settings.APP_NAME, version="0.1.1",
              summary="Gestor de cuentas de Flavio Y Laura 😍😍😍",
              docs_url=f"{settings.API_VERSION}/docs")

# init db tortoise orm
InitDb(app)

# include routers

app.include_router(api_v1_router)


@app.get("/")
async def greeting():
    return RedirectResponse(f"{settings.API_VERSION}/docs")


@app.get("/health")
async def health():
    return {"ok": True}
