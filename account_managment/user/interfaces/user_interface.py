from abc import ABC, abstractmethod

from account_managment.user.models import Users


class IUser(ABC):

    @abstractmethod
    def insert(self, user_create: Users) -> bool:
        pass

    @abstractmethod
    def get_one(self, email: str) -> Users | None:
        pass
