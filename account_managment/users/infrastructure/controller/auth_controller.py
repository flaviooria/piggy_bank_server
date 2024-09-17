from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing_extensions import Annotated

from account_managment.common import settings
from account_managment.entities.entities import Users
from account_managment.shared import (AuthAccessToken, AuthRefreshToken,
                                      JwtUtil, Payload)
from account_managment.users.application import AuthService, UserService
from account_managment.users.domain import (UserCreateDto, UserResponseDto,
                                            UserSigninDto)
from account_managment.users.infrastructure.repositories.user_pg_repository import \
    UserPgRepository
from account_managment.users.infrastructure.utils.crypt import Crypt
from account_managment.users.infrastructure.utils.generate_token import \
    generate_token


def get_expires(expires: str):
    time, _, param = expires.partition(" ")

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

user_repository = UserPgRepository()
auth_service = AuthService(user_repository)
user_service = UserService(user_repository)


async def get_user_with_access_token(payload: Annotated[Payload, Depends(
    AuthAccessToken)]): return await get_user_from_payload(payload)


async def get_user_with_refresh_token(payload: Annotated[Payload, Depends(
    AuthRefreshToken)]): return await get_user_from_payload(payload)


async def get_user_from_payload(payload: Payload):
    email = payload.sub

    user = await user_service.get_user_by_email(email)

    if user is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


auth_router = APIRouter(tags=["auth"])


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserResponseDto)
async def register(user: UserCreateDto) -> Any:
    try:

        user = UserCreateDto.model_validate(user)

        user_exist = await user_service.get_user_by_email(user.email)

        if user_exist is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with already email exists")

        plain_password = user.password
        user.password = await Crypt.encrypt(plain_password)
        user.token = generate_token()

        # TODO: falta añadir el servicio para enviar correo electronico

        return await auth_service.register(user)

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@auth_router.post('/signin', status_code=status.HTTP_200_OK, response_model=UserResponseDto)
async def login(user_signin: UserSigninDto, response: Response) -> Any:
    try:

        user_found = await user_service.get_user_by_email(user_signin.email)

        if user_found is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if not await Crypt.verify(user_signin.password, user_found.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect password")

        expires_access_token = EXPIRES_ACCESS_TOKEN

        expires_refresh_token = EXPIRES_REFRESH_TOKEN

        # ?: Hago cast de la id del usuario a str para que no me de error al hacer json.dumps
        payload_access_token = Payload(
            sub=user_found.email, exp=expires_access_token, id=str(user_found.id))

        payload_refresh_token = Payload(
            sub=user_found.email, exp=expires_refresh_token, id=str(user_found.id))

        access_token = JwtUtil.encode(payload_access_token)
        refresh__token = JwtUtil.encode(payload_refresh_token)

        response.set_cookie("access_token", access_token,
                            httponly=True, expires=expires_access_token)
        response.set_cookie("refresh_token", refresh__token,
                            httponly=True, expires=expires_refresh_token)

        return await auth_service.login(user_signin)

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@auth_router.get('/logout')
async def logout(response: Response):
    response.delete_cookie("access_token", httponly=True)
    response.delete_cookie("refresh_token", httponly=True)

    return {"message": "Logout successfully"}


@auth_router.get('/me', response_model=UserResponseDto)
async def current_user(user: Annotated[Users, Depends(get_user_with_access_token)]):
    # TODO: Añadir almacenamiento en redis al iniciar sesión el usuario
    return await UserResponseDto.from_tortoise_orm(user)


@auth_router.post('/refresh_token')
async def refresh_token(user: Annotated[Users, Depends(get_user_with_refresh_token)], response: Response):
    expires_access_token = EXPIRES_ACCESS_TOKEN
    payload_access_token = Payload(
        sub=user.email, exp=expires_access_token, id=str(user.id))

    access_token = JwtUtil.encode(payload_access_token)

    response.set_cookie("access_token", access_token,
                        httponly=True, expires=expires_access_token)

    return {"message": "Access token refreshed"}
