from __future__ import annotations

from typing import Optional
import os

def call_llm(system: str, user: str, model: Optional[str] = None) -> str:
    """Minimal chat call for live mode.

    We keep this intentionally small for classroom reliability.

    Requirements:
    - OPENAI_API_KEY set in environment or .env
    - OPENAI_MODEL optional (defaults to gpt-4o-mini)
    """
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    # Import lazily so mock mode can run even if OpenAI SDK isn't installed yet.
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
