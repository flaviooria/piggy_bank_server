from pydantic import BaseModel


class RegisterTemplate(BaseModel):
    username: str
    link_token: str
