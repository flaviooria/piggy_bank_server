from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)

from account_managment.settings.settings import settings
from account_managment.shared import (AuthAccessToken, AuthRefreshToken,
                                      JwtUtil, Payload)
from account_managment.user.dtos import (UserCreateDto, UserSingInDto,
                                         UserWithoutPasswordDto)
from account_managment.user.models import Users
from account_managment.user.respositories import UserRepository
from account_managment.user.services import GetUserService, UserRegisterService
from account_managment.user.utils import Crypt, generate_token

auth_router = APIRouter(tags=["auth"])

user_repository = UserRepository()
user_register_service = UserRegisterService(user_repository)
get_user_service = GetUserService(user_repository)


def get_expires(expires: str):
    param, _, time = expires.partition(" ")

    time = int(time)
    _timedelta = timedelta(minutes=30)

    if param == 'days':
        _timedelta = timedelta(days=time)
    if param == 'seconds':
        _timedelta = timedelta(seconds=time)
    if param == 'minutes':
        _timedelta = timedelta(minutes=time)
    if param == 'hours':
        _timedelta = timedelta(hours=time)

    return datetime.now(timezone.utc) + _timedelta


EXPIRES_ACCESS_TOKEN = get_expires(settings.EXPIRES_ACCESS_TOKEN)
EXPIRES_REFRESH_TOKEN = get_expires(settings.EXPIRES_REFRESH_TOKEN)


def get_user_with_access_token(payload: Annotated[Payload, Depends(
    AuthAccessToken)]): return get_user_from_payload(payload)


def get_user_with_refresh_token(payload: Annotated[Payload, Depends(
    AuthRefreshToken)]): return get_user_from_payload(payload)


def get_user_from_payload(payload: Payload):
    email = payload.sub

    user = get_user_service.execute(email)

    if user is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@auth_router.post("/signup")
def register(user_create: UserCreateDto) -> Any:

    try:
        user_exist = get_user_service.execute(user_create.email)

        if user_exist is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with already email exists")

        password_hashed = Crypt.encrypt(user_create.password)

        user_create.password = password_hashed

        user = Users.model_validate(
            user_create, update={"token": generate_token()})

        user_register_service.execute(user)

        return {'Ok': 'User created'}
    except HTTPException:
        raise
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@auth_router.post('/signin')
def login(user_signin: UserSingInDto, request: Request, response: Response):
    try:
        user_exist = get_user_service.execute(user_signin.email)

        if user_exist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if not Crypt.verify(user_signin.password, user_exist.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Password invalid")

        expires_access_token = EXPIRES_ACCESS_TOKEN

        expires_refresh_token = EXPIRES_REFRESH_TOKEN

        payload_access_token = Payload(
            sub=user_exist.email, exp=expires_access_token, id=user_exist.id)

        payload_refresh_token = Payload(
            sub=user_exist.email, exp=expires_refresh_token, id=user_exist.id)

        access_token = JwtUtil.encode(payload_access_token)
        refresh_token = JwtUtil.encode(payload_refresh_token)

        response.set_cookie("access_token", access_token,
                            httponly=True, expires=expires_access_token)
        response.set_cookie("refresh_token", refresh_token,
                            httponly=True, expires=expires_refresh_token)

        user_without_password = user_exist.model_dump(
            exclude={"password": True})

        return user_without_password
    except HTTPException:
        raise


@auth_router.get('/logout')
def logout(response: Response):
    response.delete_cookie("access_token", httponly=True)
    response.delete_cookie("refresh_token", httponly=True)

    return {"message": "Logout successfully"}


@auth_router.get('/me', response_model=UserWithoutPasswordDto)
def current_user(current_user: Annotated[Users, Depends(get_user_with_access_token)]):
    # TODO: Añadir almacenamiento en redis al iniciar sesión el usuario
    return current_user.model_dump()


@auth_router.post('/refresh_token')
def refresh_token(current_user: Annotated[Users, Depends(get_user_with_refresh_token)], response: Response):

    expires_access_token = EXPIRES_ACCESS_TOKEN
    payload_access_token = Payload(
        sub=current_user.email, exp=expires_access_token, id=current_user.id)

    access_token = JwtUtil.encode(payload_access_token)

    response.set_cookie("access_token", access_token,
                        httponly=True, expires=expires_access_token)

    return {"message": "Access token refreshed"}


__all__ = ["auth_router"]
