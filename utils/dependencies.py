from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db_config.get_db import get_db
from .auth.get_current_user import get_current_user


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]