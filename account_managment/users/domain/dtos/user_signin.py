from pydantic import BaseModel, EmailStr


class UserSigninDto(BaseModel):
    email: EmailStr
    password: str
