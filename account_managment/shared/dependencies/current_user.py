from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

from account_managment.shared.utils import JwtUtil

security = HTTPBearer()


class CookiesToken:

    def __init__(self, cookie_name: str = "access_token") -> None:
        self.cookie_key = cookie_name

    def __call__(self, request: Request) -> str | None:
        cookies = request.cookies.get(self.cookie_key)

        if cookies is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"{self.cookie_key} is missing")

        return cookies


def get_current_user(authorizathion: HTTPAuthorizationCredentials = Depends(security)):
    token = authorizathion.credentials

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


access_token_security = CookiesToken()
refresh_token_security = CookiesToken("refresh_token")


def access_token_required(token: str | None = Depends(access_token_security)
                          ): return get_token(token=token)


def refresh_token_required(token: str | None = Depends(
    refresh_token_security)): return get_token(token=token)


def get_token(token: str | None):
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
