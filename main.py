"""Entry point: tool-based LangChain agent for the screenplay pipeline."""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from agents.critic import critic_tool as _critic_impl
from agents.planner import planner_tool as _planner_impl
from agents.rewriter import rewriter_tool as _rewriter_impl
from agents.writer import writer_tool as _writer_impl

load_dotenv()


@tool
def planner_tool(input: str) -> str:
    """First step: turn the user's raw screenplay idea into a structured brief (logline, genre, tone, three-act structure). Pass only the user's idea as `input`."""
    return _planner_impl(input)


@tool
def writer_tool(input: str) -> str:
    """Second step: produce a scene-by-scene screenplay plus an ad script (Hook, Body, CTA). Pass the full text returned by `planner_tool` as `input`."""
    return _writer_impl(input)


@tool
def critic_tool(input: str) -> str:
    """Third step: critique the screenplay and ad (weak points, gaps, engagement). Pass the full text returned by `writer_tool` as `input`."""
    return _critic_impl(input)


@tool
def rewriter_tool(input: str) -> str:
    """Fourth step: revise the screenplay and ad using critic feedback. Pass one string: the full `writer_tool` draft, a line with only `--- CRITIC ---`, then the full `critic_tool` output."""
    return _rewriter_impl(input)


TOOLS = [planner_tool, writer_tool, critic_tool, rewriter_tool]

SYSTEM_PROMPT = """You coordinate a screenplay pipeline using the four tools.

For each user message that contains a screenplay idea, call tools in this order:
1) `planner_tool` with the user's idea text.
2) `writer_tool` with the entire output from `planner_tool`.
3) `critic_tool` with the entire output from `writer_tool`.
4) `rewriter_tool` with one string: the entire `writer_tool` output, then a new line containing exactly `--- CRITIC ---`, then the entire `critic_tool` output.

After step 4, do not call more tools. Reply to the user with a short preamble, then the full final revised draft from `rewriter_tool` (reproduce it in full so they can read or copy it)."""


def _build_model() -> ChatOpenAI:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    kwargs: dict = {"model": model_name, "temperature": 0.2}
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    return ChatOpenAI(**kwargs)


def _final_text(messages: list) -> str:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            text = msg.content
            if isinstance(text, str):
                return text
            if isinstance(text, list):
                parts = []
                for block in text:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", ""))
                return "".join(parts)
    return ""


def main() -> None:
    user_idea = input("Enter your screenplay idea: ").strip()
    if not user_idea:
        print("No input provided.")
        return

    model = _build_model()
    agent = create_agent(model, tools=TOOLS, system_prompt=SYSTEM_PROMPT)

    result = agent.invoke({"messages": [HumanMessage(content=user_idea)]})
    messages = result.get("messages", [])
    print(_final_text(messages))


if __name__ == "__main__":
    main()
