from fastapi import HTTPException, Request
from jose import jwt, JWTError

from routers.web.web_auth import sign_out

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

async def web_get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
           await sign_out(request)
        return {"username": username, "id": user_id, 'role': user_role}
    except JWTError as e:
        await sign_out(request)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
