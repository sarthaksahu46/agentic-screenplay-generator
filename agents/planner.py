"""Planner agent: breaks high-level goals into screenplay planning steps."""

from pathlib import Path

from utils.llm import call_llm

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def planner_tool(input: str) -> str:
    template = (_PROMPTS_DIR / "planner_prompt.txt").read_text(encoding="utf-8")
    prompt = f"{template}\n\n---\n\n{input}"
    return call_llm(prompt)
