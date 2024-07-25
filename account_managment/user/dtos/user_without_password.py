from pydantic import Field

from account_managment.user.models import UserBase


class UserWithoutPasswordDto(UserBase):
    password: str = Field(exclude=True)
