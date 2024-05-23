from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.v1.routers import login, register, users
from core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.RELEASE_ID)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["*"],
)

app.include_router(
    register.router, prefix=settings.API_V1_STR, tags=["register"]
)
app.include_router(login.router, prefix=settings.API_V1_STR, tags=["login"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["user"])


@app.get(path="/", include_in_schema=False)
def redirect_docs() -> RedirectResponse:
    """Redirects / to API docs"""
    return RedirectResponse("/docs")
