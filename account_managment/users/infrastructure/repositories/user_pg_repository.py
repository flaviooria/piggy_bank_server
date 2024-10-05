from account_managment.entities.entities import Users
from account_managment.users import UserCreateDto
from account_managment.users.domain.interfaces.user import IUser


class UserPgRepository(IUser):
    async def get_all(self) -> list[Users]:
        return await Users.all()

    async def insert(self, user_create: UserCreateDto) -> Users:
        try:
            user_created = await Users.create(**user_create.model_dump())

            return user_created
        except Exception as ex:
            raise ex

    async def get_one(self, email: str) -> Users | None:
        try:
            user = await Users.get_or_none(email=email)

            return user
        except Exception as ex:
            raise ex
