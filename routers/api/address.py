import sys
sys.path.append("..")

from fastapi import APIRouter
from starlette import status
import models
from propTypes.i_address import IAddress
from utils.dependencies import user_dependency, db_dependency

router = APIRouter(
    prefix='/api/v1/address',
    tags=['address'],
    responses={404: { 'description': 'Not Found' }},
)


@router.get('/get-user-address', status_code=status.HTTP_200_OK)
async def read_address(user: user_dependency,
                        db: db_dependency,
                        ):
    return db.query(models.Address).filter(models.Address.id == user["id"]).first()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_address(address_form: IAddress,
                         user: user_dependency,
                         db: db_dependency,
                         ):
    new_address = models.Address(
        address1=address_form.address1,
        address2=address_form.address2,
        city=address_form.city,
        state=address_form.state,
        postalcode=address_form.postalcode,
    )

    db.add(new_address)
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    user_model.address_id = new_address.id

    db.add(user_model)
    db.commit()

