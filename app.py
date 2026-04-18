import streamlit as st
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

import main as core

from fpdf import FPDF
import tempfile


st.set_page_config(page_title="Agentic Screenplay Generator")
st.title("Agentic Screenplay Generator")

idea = st.text_area("Your screenplay idea", placeholder="Enter a story idea, premise, or concept...")
generate = st.button("Generate", type="primary")

if generate:
    if not idea.strip():
        st.warning("Please enter a screenplay idea first.")
    else:
        with st.spinner("Generating..."):
            model = core._build_model()
            agent = create_agent(model, tools=core.TOOLS, system_prompt=core.SYSTEM_PROMPT)
            result = agent.invoke({"messages": [HumanMessage(content=idea.strip())]})
            output = core._final_text(result.get("messages", []))

        # ----------- UPDATED DISPLAY (SAFE) -----------

        def split_sections(text: str):
            if "Ad Script" in text:
                parts = text.split("Ad Script", 1)
                screenplay = parts[0].strip()
                ad = "Ad Script" + parts[1].strip()
            else:
                screenplay = text
                ad = None
            return screenplay, ad

        screenplay, ad = split_sections(output)

        st.subheader("🎬 Screenplay")
        st.markdown(screenplay if screenplay else "_No screenplay generated._")

        if ad:
            st.subheader("📢 Ad Script")
            st.markdown(ad)

        # ----------- PDF EXPORT -----------

        def clean_text(text):
            return (
                text.replace("“", '"')
                    .replace("”", '"')
                    .replace("‘", "'")
                    .replace("’", "'")
                    .replace("—", "-")
                    .replace("–", "-")
            )

        def generate_pdf(text: str) -> str:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=10)
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            for line in text.split("\n"):
                pdf.multi_cell(0, 5, line)

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(temp_file.name)
            return temp_file.name

        cleaned_output = clean_text(output)
        pdf_path = generate_pdf(cleaned_output)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download as PDF",
                data=f,
                file_name="screenplay.pdf",
                mime="application/pdf"
            )