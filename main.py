from fastapi import FastAPI, status

from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import models
from db_config.database import engine
from routers.api import auth, todos, admin, address
from routers.web import web_todos, web_auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#import static files(.css, .js, ...)
app.mount('/static', StaticFiles(directory="static"), name="static")

#redirect root
@app.get("/")
async def redirect_root():
    return RedirectResponse(url="/todos" ,status_code=status.HTTP_302_FOUND)

# ---------routers [APIs]---------
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(address.router)

# -----------router [PAGEs]---------
app.include_router(web_todos.router)
app.include_router(web_auth.router)
