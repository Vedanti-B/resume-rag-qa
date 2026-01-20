import streamlit as st
import tempfile

from pdf_utils import load_pdf_text
from section_splitter import split_resume_sections
from personal_info import extract_personal_info
from embedding_store import build_faiss_index
from rag_engine import ask_question

st.set_page_config(page_title="Resume Q&A (ATS)", layout="centered")

st.title("📄 Resume Question Answering (ATS + RAG)")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    resume_text = load_pdf_text(pdf_path)
    chunks = split_resume_sections(resume_text)
    personal_info = extract_personal_info(resume_text)

    embedder, index = build_faiss_index(chunks)

    st.success("Resume processed successfully!")

    question = st.text_input("Ask a question about the resume")

    if st.button("Get Answer") and question:
        answer = ask_question(
            question,
            personal_info,
            chunks,
            embedder,
            index
        )
        st.write("### Answer:")
        st.write(answer)
