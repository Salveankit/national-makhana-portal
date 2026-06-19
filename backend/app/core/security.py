from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta

from backend.app.core.config import settings


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def issue_token(subject: str, role: str, ttl_minutes: int = 60) -> str:
    payload = {
        "sub": subject,
        "role": role,
        "exp": int((datetime.now(UTC) + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    body = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    sig = hmac.new(settings.app_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"


def decode_token(token: str) -> dict | None:
    try:
        body, sig = token.split(".", 1)
        expected = hmac.new(settings.app_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        payload = json.loads(base64.urlsafe_b64decode(body.encode("utf-8")))
        if payload["exp"] < int(datetime.now(UTC).timestamp()):
            return None
        return payload
    except Exception:
        return None

