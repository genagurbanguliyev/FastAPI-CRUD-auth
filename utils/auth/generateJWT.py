from datetime import datetime, timedelta
from jose import jwt

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    encode = {'sub': username, 'id': user_id, 'role': role }
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
