from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import ALLOWED_ORIGINS
from src.routers import auth as auth_router
from src.routers import protected as protected_router
from src.routers import public as public_router

app = FastAPI(title="Hackathon Diary Backend (FastAPI)")

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(public_router.router)
app.include_router(auth_router.router)
app.include_router(protected_router.router)
