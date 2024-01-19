from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: { "description": "Not Found" }},
)

templates = Jinja2Templates(directory="templates")

@router.get('/', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("home.html", { "request": request })


@router.get('/add-todo', response_class=HTMLResponse)
async def add_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", { "request": request })


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(todo_id: int, request: Request):
    return templates.TemplateResponse("edit-todo.html", {"request":request})
