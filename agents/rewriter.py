"""Rewriter agent: applies critique to revise screenplay text."""

from pathlib import Path

from utils.llm import call_llm

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def rewriter_tool(input: str) -> str:
    template = (_PROMPTS_DIR / "rewriter_prompt.txt").read_text(encoding="utf-8")
    prompt = f"{template}\n\n---\n\n{input}"
    return call_llm(prompt)
