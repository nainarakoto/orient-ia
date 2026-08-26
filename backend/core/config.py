from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "ORIENT'IA Backend & Agent IA"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    USE_MOCKS: bool = True
    MAX_TOOL_ITERATIONS: int = 5
    LOG_FILE_PATH: str = "observability/logs/interactions.jsonl"
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()