from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from account_managment.shared import CurrentUserDependency, JwtUtil, Payload
from account_managment.user.dtos import UserCreateDto, UserSingInDto
from account_managment.user.models import Users
from account_managment.user.respositories import UserRepository
from account_managment.user.services import GetUserService, UserRegisterService
from account_managment.user.utils import Crypt, generate_token

auth_router = APIRouter(tags=["auth"])

user_repository = UserRepository()
user_register_service = UserRegisterService(user_repository)
get_user_service = GetUserService(user_repository)


def get_user(payload: Annotated[Payload, Depends(CurrentUserDependency)]):
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
def login(user_signin: UserSingInDto):
    try:
        user_exist = get_user_service.execute(user_signin.email)

        if user_exist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if not Crypt.verify(user_signin.password, user_exist.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Password invalid")

        # TODO: Añadir utilidad para crear jwt
        expires = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        payload = Payload(sub=user_exist.email, exp=expires, id=user_exist.id)

        # return user_exist.model_dump(exclude={"password": True})
        token = JwtUtil.encode(payload)

        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise


@auth_router.post('/me')
def get_user(current_user: Annotated[Users, Depends(get_user)]):
    # TODO: Añadir almacenamiento en redis al iniciar sesión el usuario
    return current_user.model_dump(exclude={"password": True})


__all__ = ["auth_router"]
