from pydantic import Field

from account_managment.user.domain.models.user_model import UserBase


class UserWithoutPasswordDto(UserBase):
    password: str = Field(exclude=True)
