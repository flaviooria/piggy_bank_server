from account_managment.accounts.domain import IAccount


class AccountService:
    def __init__(self, repository: IAccount) -> None:
        self.repository = repository
