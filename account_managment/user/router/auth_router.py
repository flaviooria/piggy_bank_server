from typing import Any

from bcrypt import checkpw, gensalt, hashpw
from fastapi import APIRouter, HTTPException, status

from account_managment.user.dtos import UserCreateDto, UserSingInDto
from account_managment.user.models import Users
from account_managment.user.respositories import UserRepository
from account_managment.user.services import GetUserService, UserRegisterService


def generate_token() -> str:
    import uuid

    return str(uuid.uuid4())[:6]


class Crypt:
    @staticmethod
    def _str_to_bytes(text: str) -> bytes:
        return text.encode()

    @staticmethod
    def encrypt(password: str) -> str:
        return hashpw(Crypt._str_to_bytes(password), gensalt()).decode()

    @staticmethod
    def verify(password_plain: str, password_hashed: str) -> bool:
        return checkpw(Crypt._str_to_bytes(password_plain), Crypt._str_to_bytes(password_hashed))


auth_router = APIRouter(tags=["auth"])

user_repository = UserRepository()
user_register_service = UserRegisterService(user_repository)
get_user_service = GetUserService(user_repository)


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

        # TODO: Añadir almacenamiento en redis al iniciar sesión el usuario
        # TODO: Añadir utilidad para crear jwt

        return user_exist.model_dump(exclude={"password": True})
    except HTTPException:
        raise


__all__ = ["auth_router"]
