from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

import models
from utils.dependencies import db_dependency
from utils.auth.get_current_user import web_get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: { "description": "Not Found" }},
)

templates = Jinja2Templates(directory="templates")

@router.get('/', response_class=HTMLResponse)
async def get_todos_by_user(request: Request, db: db_dependency):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user["id"]).all()
    return templates.TemplateResponse("home.html", { "request": request, "todos": todos, "user": user })


@router.get('/add-todo', response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", { "request": request, "user": user })

@router.post('/add-todo', response_class=HTMLResponse)
async def add_new_todo(request: Request,db: db_dependency, title: str = Form(...), description: str = Form(...), priority: int = Form(...)):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    todo_model = models.Todos(
        title = title,
        description = description,
        priority = priority,
        complete = False,
        owner_id = user["id"],
    )
    db.add(todo_model)
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(todo_id: int, request: Request, db: db_dependency):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    return templates.TemplateResponse("edit-todo.html", {"request":request, "todo": todo, "user": user })


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(todo_id: int, request: Request, db: db_dependency, title: str = Form(...), description: str = Form(...), priority: int = Form(...)):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = priority
    db.add(todo)
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)


@router.get("/delete-todo/{todo_id}", response_class=HTMLResponse)
async def delete_todo(todo_id: int, request: Request, db: db_dependency):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user["id"]).first()
    if todo_model is None:
        return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)
    db.delete(todo_model)
    db.commit()
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)


@router.get('/complete/{todo_id}', response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: db_dependency):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse("/auth/sign-in", status_code=status.HTTP_302_FOUND)
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo_model.complete = not todo_model.complete
    db.add(todo_model)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    
