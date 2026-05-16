import streamlit as st

from modules.sentiment import detect_sentiment
from modules.language import detect_language

from modules.response_builder import build_response

from modules.medical_ner import extract_medical_entities
from modules.multi_modal import analyze_image

from modules.document_loader import load_pdf
from modules.knowledge_updater import add_document_to_db
from modules.translator import translate_to_english
from scheduler import start_scheduler


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Smart Medical AI Chatbot",
    page_icon="🩺",
    layout="centered"
)
if "scheduler_started" not in st.session_state:

    start_scheduler()

    st.session_state.scheduler_started = True

if "messages" not in st.session_state:

    st.session_state.messages = []
    
st.title("🩺 Smart Medical AI Chatbot")

st.write(
    "Medical chatbot with dynamic knowledge base expansion"
)


# =========================================
# SIDEBAR
# =========================================

st.sidebar.header("📂 Upload Knowledge File")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt"]
)

if uploaded_file:

    text = load_pdf(uploaded_file)

    chunks_added = add_document_to_db(text)

    st.sidebar.success(
        f"Added {chunks_added} chunks to knowledge base."
    )


# =========================================
# IMAGE UPLOADER
# =========================================

st.sidebar.header("🖼 Upload Image")

uploaded_image = st.sidebar.file_uploader(
    "Upload medical image",
    type=["jpg", "jpeg", "png"]
)


# =========================================
# USER INPUT
# =========================================

user_input = st.text_input(
    "Ask a medical or research question"
)


# =========================================
# MAIN LOGIC
# =========================================

if user_input:

    # =========================
    # ANALYSIS
    # =========================

    sentiment = detect_sentiment(user_input)

    language = detect_language(user_input)

    english_query = translate_to_english(
    user_input,
    language)
    st.session_state.messages.append(
    {
        "role": "user",
        "content": user_input,
        "english_query": english_query
    }
)

    entities = extract_medical_entities(english_query)

    # =========================
    # MULTIMODAL
    # =========================

    if uploaded_image:

        response = analyze_image(
            uploaded_image,
            user_input
        )

        intent = "multimodal"

    else:
        conversation_history = "\n".join(
    [
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages[-6:]
    ]
)
        response, intent = build_response(
            english_query,
            sentiment,
            language,
            history=conversation_history
        )

    # =====================================
    # ANALYSIS DISPLAY
    # =====================================

    st.subheader("Analysis")

    # Sentiment Display
    if sentiment == "negative":

        st.error(f"😟 Sentiment: {sentiment}")

    elif sentiment == "positive":

        st.success(f"😊 Sentiment: {sentiment}")

    else:

        st.info(f"😐 Sentiment: {sentiment}")

    st.write(f"🌐 Language: **{language}**")

    st.write(f"🧠 Intent: **{intent}**")

    # =====================================
    # MEDICAL ENTITIES
    # =====================================

    if entities:

        labels = ", ".join(
            [
                f"{e['text']} ({e['label']})"
                for e in entities
            ]
        )

        st.write(
            f"🔬 Medical Entities: **{labels}**"
        )

    # =====================================
    # RESPONSE TITLE
    # =====================================

    if intent == "medical":

        st.subheader("Medical Response")

    elif intent == "research":

        st.subheader("Research Response")

    elif intent == "multimodal":

        st.subheader("Multimodal Response")

    else:

        st.subheader("General Response")

    # =====================================
    # FINAL RESPONSE
    # =====================================

    st.success(response)
    st.session_state.messages.append(
    {
        "role": "assistant",
        "content": response,
        "intent": intent
    }
)