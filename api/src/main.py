import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.auth.transport import requests as grequests
from google.oauth2 import id_token as google_id_token
from jwt import PyJWTError
from pydantic import BaseModel

load_dotenv()

ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]

APP_JWT_SECRET = os.environ["APP_JWT_SECRET"]
APP_JWT_ALG = os.getenv("APP_JWT_ALG", "HS256")
APP_JWT_EXP_SECONDS = int(os.getenv("APP_JWT_EXP_SECONDS", "3600"))
APP_JWT_ISS = os.getenv("APP_JWT_ISS", "hackathon-diary-backend")
APP_JWT_AUD = os.getenv("APP_JWT_AUD", "hackathon-diary-frontend")

app = FastAPI(title="Hackathon Diary Backend (FastAPI)")

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def issue_app_jwt(*, sub: str, email: Optional[str], role: str = "user") -> dict:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=APP_JWT_EXP_SECONDS)
    payload = {
        "sub": sub,
        "email": email,
        "role": role,
        "iss": APP_JWT_ISS,
        "aud": APP_JWT_AUD,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload, APP_JWT_SECRET, algorithm=APP_JWT_ALG)
    return {"appJwt": token, "appJwtExp": int(exp.timestamp())}


def verify_app_jwt(token: str) -> dict:
    return jwt.decode(
        token,
        APP_JWT_SECRET,
        algorithms=[APP_JWT_ALG],
        audience=APP_JWT_AUD,
        options={"require": ["exp", "iss", "aud", "sub"]},
        issuer=APP_JWT_ISS,
    )


class User(BaseModel):
    sub: str
    email: Optional[str] = None
    role: Optional[str] = None


def _extract_bearer(req: Request) -> Optional[str]:
    auth = req.headers.get("authorization") or req.headers.get("Authorization")
    if not auth:
        return None
    parts = auth.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


async def optional_current_user(request: Request) -> Optional[User]:
    token = _extract_bearer(request)
    if not token:
        return None
    try:
        payload = verify_app_jwt(token)
        return User(
            sub=payload["sub"], email=payload.get("email"), role=payload.get("role")
        )
    except PyJWTError:
        return None


async def require_current_user(
    user: Annotated[Optional[User], Depends(optional_current_user)],
) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/auth/exchange")
async def exchange(request: Request):
    id_token_hdr = request.headers.get("X-Google-IDToken")
    access_token_hdr = request.headers.get("X-Google-AccessToken")

    if not id_token_hdr and not access_token_hdr:
        raise HTTPException(status_code=400, detail="Missing Google token")

    if id_token_hdr:
        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_hdr,
                grequests.Request(),
                GOOGLE_CLIENT_ID,
            )
            sub = idinfo.get("sub")
            email = idinfo.get("email")
            if not sub:
                raise HTTPException(status_code=401, detail="Invalid Google ID token")

            return JSONResponse(issue_app_jwt(sub=sub, email=email))
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Exchange failed: {e}")

    raise HTTPException(status_code=400, detail="Use ID Token pathway")


@app.get("/api/secure-whoami")
async def secure_whoami(user: Annotated[User, Depends(require_current_user)]):
    """
    認証必須 API の例
    """
    return {"ok": True, "user": user.model_dump()}


@app.get("/articles")
async def list_articles(
    user: Annotated[Optional[User], Depends(optional_current_user)],
):
    """
    匿名でもOK、認証済みなら追加情報を返す例
    """
    items = [
        {"id": 1, "title": "Public article A"},
        {"id": 2, "title": "Public article B"},
    ]
    resp = {"items": items}
    if user:
        resp["viewer"] = {"sub": user.sub, "email": user.email, "role": user.role}
    return resp
