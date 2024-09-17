from account_managment.common import ICrud
from account_managment.entities.entities import Users


class UserService:
    def __init__(self, repository: ICrud[Users]):
        self.repository = repository

    async def get_user_by_email(self, email: str) -> Users | None:
        return await self.repository.get_one(email)
