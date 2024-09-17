from pydantic import BaseModel

from account_managment.users.domain.models.user_pydantic import UserPydanticList, UserResponsePydantic


class UserResponseDto(UserResponsePydantic, BaseModel):
    pass


class UserListResponseDto(UserPydanticList, BaseModel):
    pass
