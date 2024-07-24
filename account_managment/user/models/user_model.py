from uuid import uuid4

from sqlmodel import Field, SQLModel

from account_managment.shared.types import EmailStr


class UserBase(SQLModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    password: str
    token: str


class Users(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
