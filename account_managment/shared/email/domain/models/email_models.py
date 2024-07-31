from pydantic import BaseModel


class SmtpOptions(BaseModel):
    host: str
    port: int
    user: str
    password: str
    ssl: bool | None = False
    tls: bool | None = False
