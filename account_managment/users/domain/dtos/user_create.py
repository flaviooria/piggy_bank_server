from account_managment.users.domain.models.user_pydantic import UserPydantic


class UserCreateDto(UserPydantic):
    name: str
    lastname: str
    email: str
    password: str
    token: str | None = None
