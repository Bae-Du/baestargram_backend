from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import auth
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import wait_for_db
from app.utils.storage import upload_dir


@asynccontextmanager
async def lifespan(_: FastAPI):
    wait_for_db()
    upload_dir()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.mount(
    "/uploads",
    StaticFiles(directory=str(Path(settings.UPLOAD_DIR))),
    name="uploads",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
