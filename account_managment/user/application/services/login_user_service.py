

from account_managment.user.interfaces import IUser


class LoginUserService:

    def __init__(self, user_repository: IUser) -> None:
        self.repository = user_repository

    def execute(self, email: str):
        return self.repository.get_one(email)
