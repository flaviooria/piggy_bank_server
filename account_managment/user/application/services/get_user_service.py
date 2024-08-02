from account_managment.user.domain import IUser


class GetUserService:

    def __init__(self, user_repository: IUser) -> None:
        self.repository = user_repository

    def execute(self, email: str):
        return self.repository.get_one(email)
