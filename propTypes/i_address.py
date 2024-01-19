from pydantic import BaseModel
from typing import Optional

class IAddress(BaseModel):
    address1: str
    address2: str = Optional[str]
    city: str
    state: str
    postalcode: str = Optional[str]