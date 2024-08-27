from raw_dbmodel import Repository as RawRepository

from account_managment.user.domain import Users, IUser

# Método 1
data = RawRepository[Users]()
data.model = Users


# Método 2


class Repository(RawRepository[Users]):
    pass


class UserRepository(IUser):

    def __init__(self) -> None:
        self.repository = RawRepository[Users]()
        self.repository.model = Users

    def insert(self, user_create: Users):
        try:
            return self.repository.insert(user_create, have_autoincrement_default=False)
        except Exception as ex:
            raise ex

    def get_one(self, email: str) -> Users | None:
        try:
            return self.repository.get_one(where={"email": email}).as_model()
        except Exception as ex:
            raise ex
