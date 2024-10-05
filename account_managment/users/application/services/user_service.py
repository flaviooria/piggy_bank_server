from account_managment.entities.entities import Users
from account_managment.users.domain import IUser


class UserService:
    def __init__(self, repository: IUser):
        self.repository = repository

    async def get_user_by_email(self, email: str) -> Users | None:
        return await self.repository.get_one(email)
