from fastapi import APIRouter

from account_managment.settings.settings import settings
from .routers import all_routers

api_v1_router = APIRouter(prefix=settings.API_VERSION)

api_v1_router.include_router(all_routers)
