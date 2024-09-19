from account_managment.common import ICrud
from account_managment.entities.entities import Account


class IAccount(ICrud[Account]):
    async def get_all(self) -> list[Account]:
        pass

    async def insert(self, model: Account) -> Account:
        pass

    async def get_one(self, email: str) -> Account | None:
        pass
