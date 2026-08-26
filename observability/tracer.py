import json
import time
import os
import uuid
from typing import Any, Dict
from backend.core.config import settings

class InteractionTracer:
    def __init__(self, log_path: str = settings.LOG_FILE_PATH):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_interaction(self, data: Dict[str, Any]):
        if "request_id" not in data:
            data["request_id"] = str(uuid.uuid4())
        data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

tracer = InteractionTracer()