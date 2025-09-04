from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from tasks.config import PATH
from tasks.routers import router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory=PATH.parent / "static"), name="static")
templates = Jinja2Templates(directory=PATH.parent / "templates")

app.include_router(router)
