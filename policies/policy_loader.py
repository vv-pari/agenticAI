import yaml
from typing import Dict, Any
from utils.io import read_text

def load_policy_rules(path: str) -> Dict[str, Any]:
    return yaml.safe_load(read_text(path))
