from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from google.auth.transport import requests as grequests
from google.oauth2 import id_token as google_id_token

from src.auth.jwt import issue_app_jwt
from src.config import GOOGLE_CLIENT_ID

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/exchange")
async def exchange(request: Request):
    id_token_hdr = request.headers.get("X-Google-IDToken")

    if not id_token_hdr:
        raise HTTPException(status_code=400, detail="Missing Google token")

    try:
        idinfo = google_id_token.verify_oauth2_token(
            id_token_hdr, grequests.Request(), GOOGLE_CLIENT_ID
        )
        sub = idinfo.get("sub")
        email = idinfo.get("email")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid Google ID token")

        return JSONResponse(issue_app_jwt(sub=sub, email=email))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Exchange failed: {e}")
