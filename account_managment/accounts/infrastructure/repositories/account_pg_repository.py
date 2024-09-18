from account_managment.accounts.domain import (AccountCreateDto,
                                               AccountResponseDto, IAccount)
from account_managment.entities.entities import Account, Users


class AccountPgRepository(IAccount):
    async def insert(self, model: AccountCreateDto) -> Account:
        try:
            if isinstance(model.account_holders_ids, str):
                model.account_holders_ids = [model.account_holders_ids]

            user_list = await Users.filter(id__in=model.account_holders_ids).all()

            if len(user_list) == 0:
                raise Exception("Users not found")

            account_created = await Account.create(**model.model_dump(exclude={"account_holder_id"}))

            for user in user_list:
                await user.accounts.add(account_created)

            return await AccountResponseDto.from_tortoise_orm(account_created)
        except Exception as ex:
            raise ex

    async def get_one(self, _id: str) -> Account | None:
        try:

            return await Account.get_or_none(id=_id)
        except Exception as ex:
            raise ex

    async def get_all(self) -> list[Account]:
        try:
            return await Account.all()
        except Exception as ex:
            raise ex
