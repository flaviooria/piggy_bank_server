from abc import abstractmethod

from account_managment.entities.entities import Users
from account_managment.users.domain.dtos.user_create import UserCreateDto


class IUser:
    @abstractmethod
    async def get_all(self) -> list[Users]:
        pass

    @abstractmethod
    async def insert(self, model: UserCreateDto) -> Users:
        pass

    @abstractmethod
    async def get_one(self, email: str) -> Users | None:
        pass
