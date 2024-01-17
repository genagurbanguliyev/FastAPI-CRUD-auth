from fastapi import APIRouter, HTTPException, Path
from starlette import status

from models import Todos
from utils.dependencies import user_dependency, db_dependency


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@router.get('/todos', status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    try:
        if user is None or user['role'] != 'admin':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")
        return db.query(Todos).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal My Server ERROR")
    

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user["role"] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.delete(todo)
    db.commit()

