from typing import Dict, Any
from utils.io import read_text
from utils.llm import call_llm
from mocks.mock_llm import mock_draft

class DraftAgent:
    name = "drafter"

    def __init__(self, mode: str, prompt_path: str):
        self.mode = mode
        self.prompt = read_text(prompt_path)

    def run(self, ticket: Dict[str, Any], route: Dict[str, Any]) -> str:
        msg = ticket["message"]
        if self.mode == "mock":
            return mock_draft(msg, route.get("category","general"), route.get("priority","P2"))
        user = f"""Ticket:\n{msg}\n\nCategory: {route.get('category')}\nPriority: {route.get('priority')}\n\nDraft the response."""
        return call_llm(self.prompt, user)
