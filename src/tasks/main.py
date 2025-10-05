from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi import HTTPException
from starlette.middleware.sessions import SessionMiddleware


from tasks.config import PATH
from tasks.routers import router
from tasks.annotation_routers import router as annotation_router


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="strasne-netolik-tajny-123-f5E")
app.mount("/static", StaticFiles(directory=PATH.parent / "static"), name="static")
templates = Jinja2Templates(directory=PATH.parent / "templates")


@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/login", status_code=302)
    return await request.app.default_exception_handler(request, exc)


app.include_router(router)
app.include_router(annotation_router)
