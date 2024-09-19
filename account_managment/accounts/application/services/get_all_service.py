from account_managment.accounts.application.services.account_service import (
    AccountService,
)
from account_managment.entities.entities import Account


class AccountGetAllService(AccountService):
    async def get_all(self) -> list[Account]:
        try:
            return await self.repository.get_all()
        except Exception as ex:
            raise ex
