def detect_intent(text):

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
        "chest",
        "fever",
        "blood",
        "medical",
        "health"
    ]

    text_lower = text.lower()

    for keyword in medical_keywords:

        if keyword in text_lower:
            return "medical"

    return "general"