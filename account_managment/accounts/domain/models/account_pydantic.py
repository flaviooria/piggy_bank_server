from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from account_managment.entities.entities import Account

AccountPydantic = pydantic_model_creator(
    Account, name="AccountPydantic", exclude_readonly=True)

AccountResponsePydantic = pydantic_model_creator(
    Account, name="AccountResponsePydantic")


AccountPydanticList = pydantic_queryset_creator(
    Account, name="AccountPydanticList")
