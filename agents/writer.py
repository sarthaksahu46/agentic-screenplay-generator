"""Writer agent: drafts screenplay content from plans and constraints."""

from pathlib import Path

from utils.llm import call_llm

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def writer_tool(input: str) -> str:
    template = (_PROMPTS_DIR / "writer_prompt.txt").read_text(encoding="utf-8")
    prompt = f"{template}\n\n---\n\n{input}"
    return call_llm(prompt)
