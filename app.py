import streamlit as st

from modules.sentiment import detect_sentiment
from modules.language import detect_language
from modules.response_builder import build_response

from modules.document_loader import load_pdf, load_txt
from modules.knowledge_updater import add_document_to_db


st.set_page_config(
    page_title="Smart Medical AI Chatbot",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Smart Medical AI Chatbot")

st.write(
    "Medical chatbot with dynamic knowledge base expansion"
)


# =========================
# FILE UPLOAD SECTION
# =========================

st.sidebar.header("📂 Upload Knowledge Documents")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt"]
)


if uploaded_file:

    try:

        # Load file text
        if uploaded_file.type == "application/pdf":

            document_text = load_pdf(uploaded_file)

        else:

            document_text = load_txt(uploaded_file)

        # Add to vector DB
        num_chunks = add_document_to_db(document_text)

        st.sidebar.success(
            f"Document added successfully. "
            f"Created {num_chunks} chunks."
        )

    except Exception as e:

        st.sidebar.error(f"Error processing file: {e}")


# =========================
# CHATBOT SECTION
# =========================

user_input = st.text_input(
    "Ask a medical question"
)


if user_input:

    sentiment = detect_sentiment(user_input)

    language = detect_language(user_input)

    response, intent = build_response(
    user_input,
    sentiment
 )

    st.subheader("Analysis")

    st.write(f"Detected Sentiment: **{sentiment}**")
    st.write(f"Detected Language: **{language}**")
    st.write(f"Detected Intent: **{intent}**")

    if intent == "medical":
        st.subheader("Medical Response")
    
    else:
        st.subheader("General Response")

    st.success(response)