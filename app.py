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
from modules.arxiv_rag import search_research_papers
from modules.image_generator import generate_image_from_prompt


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Multi-Domain AI Chatbot",
    page_icon="🩺",
    layout="centered"
)
if "scheduler_started" not in st.session_state:

    start_scheduler()

    st.session_state.scheduler_started = True

if "messages" not in st.session_state:

    st.session_state.messages = []
    
st.title("🩺 Multi-Domain AI Chatbot")

st.write(
    "Chatbot with dynamic knowledge base expansion"
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
st.sidebar.header("🎨 Generate Image")

image_prompt = st.sidebar.text_area(
    "Enter image generation prompt"
)

generate_btn = st.sidebar.button("Generate Image")

if generate_btn and image_prompt:

    try:
        generated_path = generate_image_from_prompt(
            image_prompt,
            output_path="generated_image.png"
        )

        st.sidebar.success("Image generated successfully.")
        st.image(
            generated_path,
            caption="Generated Image",
            use_container_width=True
        )

    except Exception as e:
        st.sidebar.error(
            f"Image generation failed: {e}"
        )
# =========================================
# MULTILINGUAL DEMO TESTS
# =========================================

st.sidebar.header("🌐 Multilingual Demo")

demo_language = st.sidebar.selectbox(
    "Choose demo language",
    ["Hindi", "Spanish", "French"]
)

demo_queries = {
    "Hindi": "मधुमेह के लक्षण क्या हैं?",
    "Spanish": "¿Cuáles son los síntomas de la diabetes?",
    "French": "Quels sont les symptômes du diabète ?"
}

if st.sidebar.button("Load Demo Query"):

    st.session_state.demo_query = demo_queries[demo_language]


# =========================================
# USER INPUT
# =========================================

user_input = st.text_input(
    "Ask a medical or research question",
    value=st.session_state.get("demo_query", "")
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
    enhanced_query = english_query
    
    current_message = {
    "role": "user",
    "content": user_input,
    "english_query": english_query
}

    if (
        not st.session_state.messages
        or st.session_state.messages[-1] != current_message
    ):
        st.session_state.messages.append(current_message)

        entities = extract_medical_entities(english_query)

        entity_terms = " ".join(
            [entity["text"] for entity in entities]
        )

        enhanced_query = english_query

        if entity_terms:
            enhanced_query = f"{english_query} {entity_terms}"

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
            enhanced_query,
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

# =====================================
# RESEARCH PAPER SEARCH UI
# =====================================

    if intent == "research":

        st.subheader("📄 Related Research Papers")

        papers = search_research_papers(
            english_query,
            top_k=5
        )

        for i, paper in enumerate(papers, 1):

            with st.expander(
                f"{i}. {paper['title']} | Score: {paper['score']}"
            ):

                st.write(paper["content"])

        st.subheader("📊 Concept Relevance Visualization")

        chart_data = {
            "Paper": [
                paper["title"][:40]
                for paper in papers
            ],
            "Relevance Score": [
                paper["score"]
                for paper in papers
            ]
        }

        st.bar_chart(
            chart_data,
            x="Paper",
            y="Relevance Score"
        )