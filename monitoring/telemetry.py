import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from utils.time import now_ms
from utils.io import ensure_dir

@dataclass
class Telemetry:
    run_dir: str

    def __post_init__(self) -> None:
        ensure_dir(self.run_dir)
        self.events_path = Path(self.run_dir) / "events.jsonl"

    def emit(self, event_type: str, payload: Dict[str, Any]) -> None:
        event = {
            "ts_ms": now_ms(),
            "type": event_type,
            **payload,
        }
        with self.events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
