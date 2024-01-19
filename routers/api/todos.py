from fastapi import APIRouter, HTTPException, Path, Depends
from starlette import status

from models import Todos
from propTypes.i_todo import ITodo
from utils.dependencies import user_dependency, db_dependency

router = APIRouter(
    prefix="/api/v1/todos",
    tags=["todos"],
    responses={404: { "description": "Not Found" }},
)


@router.get("/get-todos", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    try:
        return db.query(Todos).filter(Todos.owner_id == user["id"]).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/get-todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user["id"]).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: ITodo, user: user_dependency, db: db_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate user.")
        new_todo = Todos(**todo_request.model_dump(), owner_id=user['id'])
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except KeyError as e:
        print(f"There is no {str(e)} get_user_token function returned dict")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/update-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, todo_request: ITodo, db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete
    db.commit()
    return todo


@router.delete("/delete-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.delete(todo)
    db.commit()
    return todo
