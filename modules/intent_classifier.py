def detect_intent(text):

    text_lower = text.lower()

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
    # RESEARCH / AI KEYWORDS
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
    # CHECK MEDICAL
    # =========================
    for keyword in medical_keywords:

        if keyword in text_lower:
            return "medical"

    # =========================
    # CHECK RESEARCH
    # =========================
    for keyword in research_keywords:

        if keyword in text_lower:
            return "research"

    return "general"