import os
import secrets

SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(64)
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
