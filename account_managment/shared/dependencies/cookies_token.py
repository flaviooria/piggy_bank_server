from fastapi import Depends, HTTPException, Request, status
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

from account_managment.shared.utils import JwtUtil


class CookiesTokenSecurity:

    def __init__(self, cookie_name: str) -> None:
        self.cookie_name = cookie_name

    def __call__(self, request: Request) -> str | None:
        cookie = request.cookies.get(self.cookie_name)

        if cookie is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"{self.cookie_name} is missing")

        return cookie


access_token_security = CookiesTokenSecurity("access_token")
refresh_token_security = CookiesTokenSecurity("refresh_token")


async def access_token_required(token: str | None = Depends(access_token_security)
                                ): return await get_token(token=token)


async def refresh_token_required(token: str | None = Depends(
    refresh_token_security)): return await get_token(token=token)


async def get_token(token: str | None):
    try:
        payload = JwtUtil.decode(token)

        return payload

    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Decode error jwt")
