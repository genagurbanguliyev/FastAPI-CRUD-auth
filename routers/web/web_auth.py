from fastapi import APIRouter, Request, status, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import models
from forms.auth_forms import LoginForm
from utils.dependencies import db_dependency
from routers.api.auth import login_access_token
from utils.bcrypt_helpers import bcrypt_hash, bcrypt_verification
from utils.auth.current_user import web_get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: { "description": "Not Found" }},
)

templates = Jinja2Templates(directory="templates")

@router.get('/sign-in', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", { "request": request })


@router.post('/sign-in', response_class=HTMLResponse)
async def sign_in(request: Request, db: db_dependency):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_access_token(response=response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", { "request": request, "msg": msg })
        return response
    except HTTPException:
        return templates.TemplateResponse("login.html", { "request": request, "msg": "Unknown Error" })


@router.get('/sign-out')
async def sign_out(request: Request):
    msg = "Logout"
    response = templates.TemplateResponse("login.html", { "request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get('/sign-up', response_class=HTMLResponse)
async def registration_page(request: Request):
    return templates.TemplateResponse("register.html", { "request": request })


@router.post('/sign-up', response_class=HTMLResponse)
async def registration(request: Request, db: db_dependency,
                       email: str = Form(...), username: str = Form(...),
                       firstname: str = Form(...), lastname: str = Form(...),
                       password: str = Form(...), password2: str = Form(...)):
    username_validation = db.query(models.Users).filter(models.Users.username == username).first()
    email_validation = db.query(models.Users).filter(models.Users.email == email).first()

    if password != password2:
        msg = "Passwords doesn't match!"
        return templates.TemplateResponse("register.html", { "request": request, "msg": msg })
    elif username_validation is not None:
        msg = "Username already exists!"
        return templates.TemplateResponse("register.html", { "request": request, "msg": msg })
    elif email_validation is not None:
        msg = "Email already exists!"
        return templates.TemplateResponse("register.html", { "request": request, "msg": msg })
    
    user_model = models.Users(
        username = username,
        email = email,
        first_name = firstname,
        last_name = lastname,
        hashed_password = bcrypt_hash(password),
        is_active = True
    )

    db.add(user_model)
    db.commit()

    msg = "User created"
    return templates.TemplateResponse("login.html", { "request": request, "msg": msg })


@router.get('/edit-password', response_class=HTMLResponse)
async def edit_password_page(request: Request):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("edit-password.html", { "request": request, "user": user })


@router.post('/edit-password', response_class=HTMLResponse)
async def user_password_change(request: Request, db: db_dependency, username: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    user = await web_get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=status.HTTP_302_FOUND)
    
    user_data = db.query(models.Users).filter(models.Users.id == user["id"]).first()
    msg = "Invalid password"
    if user_data is not None:
        if username == user_data.username and bcrypt_verification(password, user_data.hashed_password):
            user_data.hashed_password = bcrypt_hash(password2)
            db.add(user_data)
            db.commit()
            msg = "Password updated"
    return templates.TemplateResponse("edit-password.html", {"request": request, "user": user, "msg": msg })
