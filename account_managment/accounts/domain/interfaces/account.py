from account_managment.common import ICrud
from account_managment.common.interfaces.crud_interface import AnyModel
from account_managment.entities.entities import Account


class IAccount(ICrud[Account]):
    async def get_all(self) -> list[AnyModel]:
        pass

    async def insert(self, model: AnyModel) -> AnyModel:
        pass

    async def get_one(self, email: str) -> AnyModel | None:
        pass
