from fastapi import APIRouter

from account_managment.common import settings

from .routers import all_routers

# set the prefix /api/v1
api_v1_router = APIRouter(prefix=settings.API_VERSION)
api_v1_router.include_router(all_routers)
