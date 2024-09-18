from account_managment.accounts.application.services.account_service import AccountService
from account_managment.accounts.domain import AccountCreateDto
from account_managment.entities.entities import Account


class AccountCreateService(AccountService):

    async def create(self, account_create: AccountCreateDto) -> Account:
        try:
            return await self.repository.insert(account_create)
        except Exception as ex:
            raise ex
