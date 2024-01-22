from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
# from starlette import status


from models import Users
from propTypes.i_user import IUser
from propTypes.i_token import Token
from utils.auth.generateJWT import create_access_token
from utils.dependencies import db_dependency

from utils.bcrypt_helpers import bcrypt_verification, bcrypt_hash

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)


def authenticate_user(username: str, password: str, db) -> IUser | bool:
    user = db.query(Users).filter(Users.username == username).first()
    if user and bcrypt_verification(password, user.hashed_password):
        return user
    return False

@router.get("/get-users", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Users).all()


@router.post('/create-user', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: IUser):
    create_user_model = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password= bcrypt_hash(user_request.password),
        role=user_request.role,
        is_active=True,
        phone_number=user_request.phone_number
    )
    
    db.add(create_user_model)
    db.commit()
    return create_user_model


@router.post('/get-user-token', response_model=Token)
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/token', response_model=Token)
async def login_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency) -> bool:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=60))
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return True

