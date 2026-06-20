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
    chatbot_enabled: bool = os.getenv("CHATBOT_ENABLED", "false").lower() == "true"
    chatbot_provider: str = os.getenv("CHATBOT_PROVIDER", "azure_openai")
    chatbot_default_language: str = os.getenv("CHATBOT_DEFAULT_LANGUAGE", "en")
    knowledge_base_dir: str = os.getenv("KNOWLEDGE_BASE_DIR", "knowledge")
    knowledge_chunk_size: int = int(os.getenv("KNOWLEDGE_CHUNK_SIZE", "900"))
    knowledge_chunk_overlap: int = int(os.getenv("KNOWLEDGE_CHUNK_OVERLAP", "120"))
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")


settings = Settings()
