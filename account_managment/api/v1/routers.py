from fastapi import APIRouter

from account_managment.users import auth_router

all_routers = APIRouter()


def init_routers():
    all_routers.include_router(auth_router, prefix="/auth")


init_routers()
