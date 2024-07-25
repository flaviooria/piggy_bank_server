from pydantic import EmailStr as PyEmailStr
from typing_extensions import Annotated

EmailStr = Annotated[str, PyEmailStr]
