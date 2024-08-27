from fastapi import APIRouter

from account_managment.user.infrastructure import auth_router

all_routers = APIRouter()


def includes_routers():
    all_routers.include_router(auth_router, prefix="/auth")


includes_routers()
