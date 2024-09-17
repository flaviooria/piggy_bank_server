from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from account_managment.entities.entities import Users

UserPydantic = pydantic_model_creator(Users, name="UserPydantic", exclude_readonly=True)

UserResponsePydantic = pydantic_model_creator(Users, name="UserResponsePydantic", exclude=("password",))

UserPydanticList = pydantic_queryset_creator(Users, name="UserPydanticList", exclude=("password",))
