from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status

from backend.app.core.rbac import has_permission
from backend.app.core.security import decode_token
from backend.app.data import add_audit, get_user_by_email


def get_current_user(request: Request, authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    payload = decode_token(authorization.replace("Bearer ", "", 1))
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user_by_email(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    request.state.user = user
    return user


def require_permission(permission: str):
    def checker(request: Request, user=Depends(get_current_user)):
        if not has_permission(user.role, permission):
            add_audit(user.email, user.role, "deny", "rbac", f"Denied permission {permission}", request.client.host if request.client else "unknown")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return checker
