from modules import language
from modules.intent_classifier import detect_intent

from modules.medical_rag import retrieve_medical_context
from modules.arxiv_rag import retrieve_research_context

from modules.llm import generate_rag_response


def build_response(user_message, sentiment, language,history=""):
    """
    Builds chatbot response based on detected intent.

    Flow:
    - general  -> normal conversational response
    - medical  -> medical RAG pipeline
    - research -> arXiv research RAG pipeline
    """

    intent = detect_intent(user_message,history)

    # =========================
    # GENERAL CONVERSATION
    # =========================
    if intent == "general":

        if sentiment == "negative":
            response = (
                "I understand your frustration. "
                "I'm still improving and learning to respond more accurately."
            )

        elif sentiment == "positive":
            response = (
                "I'm glad the interaction was helpful."
            )

        else:
            response = (
                "I'm here to help with medical or research questions."
            )

        return response, intent

    # =========================
    # MEDICAL RAG PIPELINE
    # =========================
    elif intent == "medical":

        contexts = retrieve_medical_context(
            user_message,
            top_k=5
        )

        combined_context = "\n\n".join(contexts)

        response = generate_rag_response(
            user_message,
            combined_context,
            domain="medical", 
            language=language,
            history=history
        )

        if sentiment == "negative":
            response = (
                "I understand your concern. "
                "Here’s some medical information that may help:\n\n"
                + response
            )

        return response, intent

    # =========================
    # RESEARCH RAG PIPELINE
    # =========================
    elif intent == "research":

        contexts = retrieve_research_context(
            user_message,
            top_k=3
        )

        combined_context = "\n\n".join(contexts)

        response = generate_rag_response(
            user_message,
            combined_context,
            domain="research", 
            language=language,
            history=history
        )

        return response, intent

    # =========================
    # FALLBACK
    # =========================
    else:
        return (
            "I'm not sure how to classify this query yet.",
            "general"
        )