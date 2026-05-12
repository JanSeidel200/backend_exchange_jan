import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FileStorage:
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.settings_path = self.data_dir / "settings.json"
        self.history_path = self.data_dir / "analysis_history.jsonl"

    def save_settings(self, payload: dict[str, Any]) -> None:
        self.settings_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def append_analysis_history(
        self,
        request: dict[str, Any],
        response: dict[str, Any],
    ) -> None:
        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": request,
            "response": response,
        }
        with self.history_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")