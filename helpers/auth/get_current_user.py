from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

oauth_bearer  = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, message="Could not validate user.")
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, message="Could not validate credentials.")
