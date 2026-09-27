import os
import re
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

from legalEaseAPI.generator import (
    format_docx,
    format_html_preview,
    format_pdf,
    format_txt,
)

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "image" / "logo.png"

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 900px; padding-top: 2rem;}
    .legal-preview {
        background: #171923;
        border: 1px solid #303341;
        border-radius: 10px;
        padding: 28px;
        color: #f4f4f5;
        line-height: 1.65;
        max-height: 650px;
        overflow-y: auto;
    }
    .legal-preview h3 {color: #ffffff; margin-top: 20px;}
    .legal-preview p {margin-bottom: 10px;}
    .legal-preview li {margin-bottom: 6px;}
    </style>
    """,
    unsafe_allow_html=True,
)

left, center, right = st.columns([1, 2, 1])
with center:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown(
    "<h1 style='text-align:center;'>AI Legal Document Generator</h1>",
    unsafe_allow_html=True,
)

st.caption(
    "Generate an editable draft, preview it, and export it as TXT, DOCX, or PDF."
)

document_type = st.text_input(
    "Document Type",
    placeholder="Freelance Work Contract",
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
    height=100,
)

terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Payment to be made within 30 days of invoice; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    ),
    height=140,
)

dates = st.text_input(
    "Effective Date",
    placeholder="April 15, 2025",
)

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "editing" not in st.session_state:
    st.session_state.editing = False

if st.button("Generate Document", type="primary", use_container_width=True):
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Fill in Document Type, Parties, Terms & Conditions, and Effective Date.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }

        try:
            with st.spinner("Generating document..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )
            if response.ok:
                st.session_state.generated_text = response.json()["document"]
                st.session_state.editing = False
                st.success("Document generated successfully.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to FastAPI. Start the backend first. "
                f"Details: {exc}"
            )

if st.session_state.generated_text:
    st.subheader("Document Generated")

    if st.button("Edit Document", use_container_width=True):
        st.session_state.editing = True

    if st.session_state.editing:
        edited = st.text_area(
            "Edit Document Below",
            value=st.session_state.generated_text,
            height=500,
        )
        if st.button("Apply Changes", use_container_width=True):
            st.session_state.generated_text = edited
            st.session_state.editing = False
            st.rerun()

    preview = format_html_preview(st.session_state.generated_text)
    st.markdown(
        f'<div class="legal-preview">{preview}</div>',
        unsafe_allow_html=True,
    )

    text_data = format_txt(st.session_state.generated_text)
    docx_data = format_docx(st.session_state.generated_text, document_type or "Legal Document")
    pdf_data = format_pdf(st.session_state.generated_text, document_type or "Legal Document")

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", document_type.strip() or "legal_document")

    st.subheader("Download")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.download_button(
            "Download as TXT",
            data=text_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with c2:
        st.download_button(
            "Download as DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with c3:
        st.download_button(
            "Download as PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption(
    "LegalEase generates drafts for informational and drafting purposes. "
    "AI output should be reviewed by a qualified legal professional before use."
)
