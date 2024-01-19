from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: { "description": "Not Found" }},
)

templates = Jinja2Templates(directory="templates")

@router.get('/sign-in', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("login.html", { "request": request })



@router.get('/sign-up', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("register.html", { "request": request })
