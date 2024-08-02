from pydantic import BaseModel

from account_managment.shared import EmailStr


class UserSingInDto(BaseModel):
    email: EmailStr
    password: str
