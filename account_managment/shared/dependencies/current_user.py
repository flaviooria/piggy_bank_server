from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

from account_managment.shared.utils import JwtUtil

security = HTTPBearer()


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
