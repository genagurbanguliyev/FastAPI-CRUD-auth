from fastapi import APIRouter, HTTPException
from starlette import status
from passlib.context import CryptContext

from models import Users
from utils.dependencies import user_dependency, db_dependency
from propTypes.i_user import IUserPassVerification

router = APIRouter(
    prefix='/api/v1/user',
    tags=['user']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get("/get-users", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Users).all()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    try:
        return db.query(Users).filter(Users.id == user["id"]).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal My Server ERROR")


@router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, pass_form: IUserPassVerification, db: db_dependency):
    user_model = db.query(Users).filter(Users.id == user["id"]).first()
    if not bcrypt_context.verify(pass_form.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    user_model.hashed_password = bcrypt_context.encrypt(pass_form.new_password)
    db.add(user_model)
    db.commit()
        
