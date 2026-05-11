from modules.medical_rag import retrieve_medical_context
from modules.llm import generate_medical_response
from modules.intent_classifier import detect_intent


def build_response(user_message, sentiment):

    intent = detect_intent(user_message)

    if intent == "general":

        if sentiment == "negative":
            response = (
                "I understand your frustration. "
                "I'm still improving and learning to respond more accurately."
            )

        elif sentiment == "positive":
            response = "I'm glad the interaction was helpful."

        else:
            response = "I'm here to help. Please ask any medical question."

        return response, intent

    contexts = retrieve_medical_context(user_message, top_k=5)

    combined_context = "\n\n".join(contexts)

    ai_response = generate_medical_response(
        user_message,
        combined_context
    )

    if sentiment == "negative":
        intro = (
            "I understand your concern. "
            "Here’s some medical information that may help:\n\n"
        )
    elif sentiment == "positive":
        intro = (
            "Glad to assist you. "
            "Here’s the information you requested:\n\n"
        )
    else:
        intro = ""

    return intro + ai_response, intent