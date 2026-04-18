"""Critic agent: reviews drafts and returns structured feedback."""

from pathlib import Path

from utils.llm import call_llm

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def critic_tool(input: str) -> str:
    template = (_PROMPTS_DIR / "critic_prompt.txt").read_text(encoding="utf-8")
    prompt = f"{template}\n\n---\n\n{input}"
    return call_llm(prompt)
