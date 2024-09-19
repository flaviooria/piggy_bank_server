from pydantic import BaseModel

from account_managment.accounts.domain.models.account_pydantic import AccountPydantic


class AccountCreateDto(AccountPydantic, BaseModel):
    account_holders_ids: str | list[str]
