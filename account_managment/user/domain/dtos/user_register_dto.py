from pydantic import BaseModel

from account_managment.shared.types import EmailStr


class UserCreateDto(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str
