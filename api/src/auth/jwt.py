from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt

from src.config import (
    APP_JWT_ALG,
    APP_JWT_AUD,
    APP_JWT_EXP_SECONDS,
    APP_JWT_ISS,
    APP_JWT_SECRET,
)


def issue_app_jwt(
    *, sub: str, email: Optional[str], role: str = "user"
) -> Dict[str, Any]:
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


def verify_app_jwt(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        APP_JWT_SECRET,
        algorithms=[APP_JWT_ALG],
        audience=APP_JWT_AUD,
        options={"require": ["exp", "iss", "aud", "sub"]},
        issuer=APP_JWT_ISS,
    )
