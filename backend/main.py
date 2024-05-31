from api.v1.routers import (
    categories,
    comments,
    login,
    posts,
    reactions,
    register,
    users,
)
from bson.errors import InvalidId
from core.config import settings
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.APP_NAME, version=settings.RELEASE_ID)

app.mount("/api/v1/media", StaticFiles(directory="media"), name="static")

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
app.include_router(
    categories.router, prefix=settings.API_V1_STR, tags=["categories"]
)

app.include_router(posts.router, prefix=settings.API_V1_STR, tags=["posts"])

app.include_router(
    comments.router, prefix=settings.API_V1_STR, tags=["comments"]
)

app.include_router(
    reactions.router, prefix=settings.API_V1_STR, tags=["reactions"]
)


@app.get(path="/", include_in_schema=False)
def redirect_docs() -> RedirectResponse:
    """Redirects / to API docs"""
    return RedirectResponse("/docs")


@app.exception_handler(InvalidId)
def invalid_id_handler(request, exc):
    message = {"message": "Invalid Object Id"}
    return JSONResponse(message, status.HTTP_400_BAD_REQUEST)
