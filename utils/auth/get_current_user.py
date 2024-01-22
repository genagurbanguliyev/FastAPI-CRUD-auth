from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from propTypes.i_user import ITokenToUser

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

oauth2_bearer  = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> ITokenToUser:
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "id": user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


async def web_get_current_user(request: Request) -> ITokenToUser:
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            return None
        return {"username": username, "id": user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
