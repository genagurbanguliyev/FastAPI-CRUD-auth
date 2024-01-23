from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db_config.get_db import get_db
from utils.auth.current_user import get_current_user


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
# web_user_dependency = Annotated[dict, Depends(web_get_current_user)]