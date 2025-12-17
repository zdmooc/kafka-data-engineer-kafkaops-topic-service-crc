from __future__ import annotations

from fastapi import Header, HTTPException

from .config import settings


def require_auth(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if settings.auth_mode == "disabled":
        return
    if settings.auth_mode == "api_key":
        if not settings.api_key or x_api_key != settings.api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return
    raise HTTPException(status_code=500, detail="Invalid AUTH_MODE")
