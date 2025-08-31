from typing import Optional

from fastapi import APIRouter, Depends

from src.auth.deps import User, optional_current_user

router = APIRouter(tags=["public"])


@router.get("/health")
def health():
    return {"ok": True}


@router.get("/articles")
async def list_articles(user: Optional[User] = Depends(optional_current_user)):
    items = [
        {"id": 1, "title": "Public article A"},
        {"id": 2, "title": "Public article B"},
    ]
    resp = {"items": items}
    if user:
        resp["viewer"] = {"sub": user.sub, "email": user.email, "role": user.role}
    return resp
