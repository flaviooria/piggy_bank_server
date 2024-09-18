from account_managment.common import ICrud
from account_managment.entities.entities import Account


class AccountService:

    def __init__(self, repository: ICrud[Account]) -> None:
        self.repository = repository
