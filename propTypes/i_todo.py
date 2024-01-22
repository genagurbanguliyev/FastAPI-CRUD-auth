from typing import Optional
from pydantic import BaseModel, Field

from fastapi import Form

class ITodo(BaseModel):
    id: Optional[int] = Field(default=None, title="id is not needed")
    title: str = Field(min_length=3)
    description: str = Field(min_length=6)
    priority: int = Field(gt=0, lt=6, default=1)
    complete: bool = Field(default=None, title="complete by default: False")

    class Config:
        json_schema_extra = {
            'example': {
                'title': "title todo",
                'description': "description",
                'priority': 1,
                'complete': False,
            }
        }


class ITodoForm(BaseModel):
    title: str = Form(...)
    description: str = Form(...)
    priority: int = Form(...)
