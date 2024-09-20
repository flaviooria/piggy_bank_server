from abc import abstractmethod

from account_managment.accounts.domain.dtos.account_create import AccountCreateDto
from account_managment.entities.entities import Account


class IAccount:
    @abstractmethod
    async def get_all(self) -> list[Account]:
        pass

    @abstractmethod
    async def insert(self, model: AccountCreateDto) -> Account:
        pass

    @abstractmethod
    async def get_one(self, email: str) -> Account | None:
        pass
