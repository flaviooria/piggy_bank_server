from uuid import uuid4

from tortoise import Model, fields


class Users(Model):
    id = fields.UUIDField(primary_key=True, default=uuid4())  # noqa A003

    name: str = fields.TextField()
    lastname: str = fields.TextField()
    email: str = fields.TextField()
    password: str = fields.TextField()
    token: str = fields.TextField()

    # Relations
    accounts: fields.ManyToManyRelation["Account"] = fields.ManyToManyField(
        "models.Account", related_name="accounts_holders"
    )

    class Meta:
        table = "users"


class Account(Model):
    id = fields.UUIDField(primary_key=True, default=uuid4())  # noqa A003

    name: str = fields.TextField()
    total_amount: float = fields.FloatField()

    # Relations
    account_holders: fields.ManyToManyRelation[Users]
