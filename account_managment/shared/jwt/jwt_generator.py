from datetime import datetime
from typing import ClassVar

from jwt import decode as JwtDecode
from jwt import encode as JwtEncode
from pydantic import BaseModel, ConfigDict, Field

from account_managment.common import settings


class Payload(BaseModel):
    model_config = ConfigDict(extra="allow")

    sub: str | None = Field(default=None)
    iat: int | datetime | None = Field(default=None)
    exp: int | datetime | None = Field(default=None)
    nbf: int | datetime | None = Field(default=None)
    iss: str | None = Field(default=None)
    aud: list[str] | None = Field(default=None)


class JwtUtil:
    _secret: ClassVar[str] = settings.SECRET_KEY

    @staticmethod
    def encode(payload: dict | Payload):

        _payload = payload

        if isinstance(payload, Payload):
            _payload = payload.model_dump(exclude_none=True)

        return JwtEncode(_payload, JwtUtil._secret, algorithm="HS256")

    @staticmethod
    def decode(jwt: str) -> Payload:
        decoded = JwtDecode(jwt, JwtUtil._secret, algorithms=["HS256"])

        return Payload(**decoded)
