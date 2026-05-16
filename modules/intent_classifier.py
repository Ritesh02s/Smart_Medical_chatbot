import re


def detect_intent(text, history=""):

    # =========================
    # CLEAN TEXT
    # =========================

    text_lower = re.sub(
        r"[^\w\s]",
        "",
        text.lower()
    )

    history_lower = history.lower()

    # =========================
    # FOLLOW-UP DETECTION
    # =========================

    follow_up_phrases = [
        "it",
        "they",
        "them",
        "this",
        "that",
        "how is it treated",
        "can it",
        "why is it",
        "how does it"
    ]

    is_follow_up = any(
        phrase in text_lower
        for phrase in follow_up_phrases
    )

    # =========================
    # MEDICAL KEYWORDS
    # =========================

    medical_keywords = [
        "symptom",
        "disease",
        "treatment",
        "pain",
        "diabetes",
        "cancer",
        "asthma",
        "infection",
        "medicine",
        "doctor",
        "fever",
        "health",
        "blood"
    ]

    # =========================
    # RESEARCH KEYWORDS
    # =========================

    research_keywords = [
        "transformer",
        "attention",
        "neural network",
        "machine learning",
        "deep learning",
        "reinforcement learning",
        "llm",
        "language model",
        "diffusion",
        "computer vision",
        "nlp",
        "research paper",
        "artificial intelligence",
        "ai"
    ]

    # =========================
    # DIRECT MEDICAL MATCH
    # =========================

    for keyword in medical_keywords:

        if keyword in text_lower:
            return "medical"

    # =========================
    # DIRECT RESEARCH MATCH
    # =========================

    for keyword in research_keywords:

        if keyword in text_lower:
            return "research"

    # =========================
    # FOLLOW-UP ROUTING
    # =========================

    if is_follow_up:

        if any(
            word in history_lower
            for word in medical_keywords
        ):
            return "medical"

        if any(
            word in history_lower
            for word in research_keywords
        ):
            return "research"

    # =========================
    # DEFAULT
    # =========================

    return "general"