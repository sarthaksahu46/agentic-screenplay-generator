# Agentic Screenplay Generator

Multi-agent LLM system for generating and refining screenplays using an iterative pipeline.

---
## How it works

Input idea → Planner → Writer → Critic → Rewriter → Final Output

---
## Stack
- LLM: Groq (LLaMA)
- Framework: LangChain
- UI: Streamlit
- Language: Python

---
## Why this approach?

Instead of a single prompt:
- Breaks problem into steps
- Adds feedback loop (critic)
- Improves output quality

---
## Run
URL: https://agentic-screenplay-generator-4crqza9iexfq9qmvkcei9e.streamlit.app/
```bash
pip install -r requirements.txt
streamlit run app.py
