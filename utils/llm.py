"""LLM client: load env, OpenAI-compatible chat, single-call helper."""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        base_url = os.getenv("OPENAI_BASE_URL")
        _client = OpenAI(base_url=base_url) if base_url else OpenAI()
    return _client


def call_llm(prompt: str) -> str:
    """Send a full prompt string and return the assistant message text."""
    client = _get_client()
    response = client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    message = response.choices[0].message.content
    return message if message is not None else ""
