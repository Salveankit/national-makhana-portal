from pydantic import BaseModel
import os
from pathlib import Path


class Settings(BaseModel):
    app_name: str = "National Makhana Portal"
    app_env: str = os.getenv("APP_ENV", "development")
    app_secret: str = os.getenv("APP_SECRET", "change-me")
    data_dir: str = os.getenv("APP_DATA_DIR", str(Path("backend") / "data"))
    sqlite_path: str = os.getenv("SQLITE_PATH", str(Path(data_dir) / "makhana.db"))
    document_root: str = os.getenv("DOCUMENT_ROOT", str(Path(data_dir) / "documents"))
    sms_gateway_enabled: bool = os.getenv("SMS_GATEWAY_ENABLED", "false").lower() == "true"
    email_gateway_enabled: bool = os.getenv("EMAIL_GATEWAY_ENABLED", "true").lower() == "true"
    whatsapp_gateway_enabled: bool = os.getenv("WHATSAPP_GATEWAY_ENABLED", "false").lower() == "true"
    aadhaar_vault_enabled: bool = os.getenv("AADHAAR_VAULT_ENABLED", "false").lower() == "true"


settings = Settings()
