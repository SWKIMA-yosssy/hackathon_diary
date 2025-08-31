from typing import Optional

from fastapi import Depends, HTTPException, Request
from jwt import PyJWTError
from pydantic import BaseModel

from src.auth.jwt import verify_app_jwt


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
    user: Optional[User] = Depends(optional_current_user),
) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
