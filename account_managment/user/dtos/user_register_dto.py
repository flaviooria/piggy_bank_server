from account_managment.user.models.user_model import UserBase


class UserCreateDto(UserBase):
    password: str
