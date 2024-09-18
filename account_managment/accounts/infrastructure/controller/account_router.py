from fastapi import APIRouter, HTTPException, status

from account_managment.accounts.application import (AccountCreateService,
                                                    AccountGetAllService)
from account_managment.accounts.domain import (AccountCreateDto,
                                               AccountResponseDto)
from account_managment.accounts.infrastructure.repositories.account_pg_repository import \
    AccountPgRepository

account_repository = AccountPgRepository()
account_create_service = AccountCreateService(account_repository)
account_get_all_service = AccountGetAllService(account_repository)

account_router = APIRouter(tags=["Accounts"])


@account_router.post("/create_account", status_code=status.HTTP_201_CREATED, response_model=AccountResponseDto)
async def create_account(account_create: AccountCreateDto):
    try:
        account = AccountCreateDto.model_validate(account_create)

        return await account_create_service.create(account)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


@account_router.get("/accounts", status_code=status.HTTP_200_OK, response_model=list[AccountResponseDto])
async def get_accounts():
    try:
        return await account_get_all_service.get_all()
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
