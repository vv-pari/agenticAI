from typing import Dict, Any
import json
from utils.io import read_text
from utils.llm import call_llm
from mocks.mock_llm import mock_route

class RouterAgent:
    name = "router"

    def __init__(self, mode: str, prompt_path: str):
        self.mode = mode
        self.prompt = read_text(prompt_path)

    def run(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        msg = ticket["message"]
        if self.mode == "mock":
            return mock_route(msg)

        # live: ask LLM to output JSON
        out = call_llm(self.prompt, f"Ticket:\n{msg}\n\nReturn JSON only.")
        try:
            return json.loads(out)
        except Exception:
            # fallback conservative
            return {"category":"general","priority":"P1","confidence":0.4,"rationale":"Failed to parse JSON; defaulted conservatively."}
