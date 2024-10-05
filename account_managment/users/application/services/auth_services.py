from account_managment.entities.entities import Users
from account_managment.users.domain import IUser, UserCreateDto, UserSigninDto


class AuthService:
    def __init__(self, repository: IUser) -> None:
        self.repository = repository

    async def register(self, user: UserCreateDto) -> Users:
        return await self.repository.insert(user)

    async def login(self, user: UserSigninDto) -> Users | None:
        return await self.repository.get_one(user.email)
