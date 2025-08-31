from fastapi import APIRouter, Depends

from src.auth.deps import User, require_current_user

router = APIRouter(prefix="/api", tags=["protected"])


@router.get("/secure-whoami")
async def secure_whoami(user: User = Depends(require_current_user)):
    return {"ok": True, "user": user.model_dump()}
