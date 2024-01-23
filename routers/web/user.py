# from fastapi import APIRouter, Request, status
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from starlette.responses import RedirectResponse

# from TodoApp.utils.auth.current_user import web_get_current_user

# router = APIRouter(
#     prefix="/user",
#     tags=["user"],
#     responses={404: { "description": "Not Found" }},
# )

# templates = Jinja2Templates(directory="templates")


# @router.get('/edit-password', response_class=HTMLResponse)
# async def edit_password_page(request: Request):
#     user = await web_get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth/sign-in", status_code=status.HTTP_302_FOUND)
#     return templates.TemplateResponse("edit-password.html", { "request": request })
