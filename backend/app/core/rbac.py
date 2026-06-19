ROLE_PERMISSIONS = {
    "nmb_admin": {"audit:read", "locations:read", "profile:read"},
    "state_officer": {"locations:read", "profile:read"},
    "inspector": {"locations:read", "profile:read"},
    "beneficiary": {"profile:read"},
}


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())

