from datetime import datetime
from uuid import uuid4

from sqlmodel import Field, SQLModel


class AccountBase(SQLModel):
    name: str
    base_amount: float


class Accounts(AccountBase, table=True):
    id: str = Field(default_factory=lambda: uuid4(), primary_key=True)
    create_date: datetime | None = Field(
        default_factory=lambda: datetime.now())
    is_saving_account: bool | None = Field(default=False)
    parent_account_id: str | None = Field(
        default=None, foreign_key="accounts.id")
