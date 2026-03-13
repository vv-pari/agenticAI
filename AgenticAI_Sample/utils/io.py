import json
from pathlib import Path
from typing import Any, Dict, List

def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def write_text(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")
