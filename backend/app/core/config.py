from pydantic import BaseModel
import os
from pathlib import Path


def _load_local_env() -> None:
    root = Path(__file__).resolve().parents[3]
    for env_name in (".env.local", ".env"):
        env_path = root / env_name
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            os.environ.setdefault(key, value)


_load_local_env()


def _default_data_dir() -> Path:
    if os.getenv("VERCEL") == "1":
        return Path("/tmp/national-makhana-portal")
    return Path("backend") / "data"


DEFAULT_DATA_DIR = _default_data_dir()
DEFAULT_SQLITE_PATH = DEFAULT_DATA_DIR / "makhana.db"
DEFAULT_DOCUMENT_ROOT = DEFAULT_DATA_DIR / "documents"


class Settings(BaseModel):
    app_name: str = "National Makhana Portal"
    app_env: str = os.getenv("APP_ENV", "development")
    app_secret: str = os.getenv("APP_SECRET", "change-me")
    data_dir: str = os.getenv("APP_DATA_DIR", str(DEFAULT_DATA_DIR))
    sqlite_path: str = os.getenv("SQLITE_PATH", str(DEFAULT_SQLITE_PATH))
    document_root: str = os.getenv("DOCUMENT_ROOT", str(DEFAULT_DOCUMENT_ROOT))
    sms_gateway_enabled: bool = os.getenv("SMS_GATEWAY_ENABLED", "false").lower() == "true"
    email_gateway_enabled: bool = os.getenv("EMAIL_GATEWAY_ENABLED", "true").lower() == "true"
    whatsapp_gateway_enabled: bool = os.getenv("WHATSAPP_GATEWAY_ENABLED", "false").lower() == "true"
    aadhaar_vault_enabled: bool = os.getenv("AADHAAR_VAULT_ENABLED", "false").lower() == "true"
    chatbot_enabled: bool = os.getenv("CHATBOT_ENABLED", "false").lower() == "true"
    chatbot_provider: str = os.getenv("CHATBOT_PROVIDER", "gemini")
    chatbot_default_language: str = os.getenv("CHATBOT_DEFAULT_LANGUAGE", "en")
    knowledge_base_dir: str = os.getenv("KNOWLEDGE_BASE_DIR", "knowledge")
    knowledge_chunk_size: int = int(os.getenv("KNOWLEDGE_CHUNK_SIZE", "900"))
    knowledge_chunk_overlap: int = int(os.getenv("KNOWLEDGE_CHUNK_OVERLAP", "120"))
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    gemini_api_base_url: str = os.getenv(
        "GEMINI_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
    )


settings = Settings()
