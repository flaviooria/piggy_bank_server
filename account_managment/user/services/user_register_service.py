from account_managment.user.interfaces import IUser
from account_managment.user.models import Users


class UserRegisterService:

    def __init__(self, user_repository: IUser):
        self.user_repository = user_repository

    def execute(self, user_create: Users):
        return self.user_repository.insert(user_create)
