from pydantic import BaseModel

from account_managment.accounts.domain.models.account_pydantic import (
    AccountPydanticList, AccountResponsePydantic)


class AccountResponseDto(AccountResponsePydantic, BaseModel):
    pass


class AccountListResponseDto(AccountPydanticList, BaseModel):
    pass
