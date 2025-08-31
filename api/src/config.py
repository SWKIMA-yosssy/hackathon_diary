import os

from dotenv import load_dotenv

load_dotenv()

ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
]

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]

APP_JWT_SECRET = os.environ["APP_JWT_SECRET"]
APP_JWT_ALG = os.environ["APP_JWT_ALG"]
APP_JWT_EXP_SECONDS = int(os.environ["APP_JWT_EXP_SECONDS"])
APP_JWT_ISS = os.environ["APP_JWT_ISS"]
APP_JWT_AUD = os.environ["APP_JWT_AUD"]
