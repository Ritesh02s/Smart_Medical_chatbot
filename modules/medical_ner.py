try:
    import spacy

    try:
        # Try loading spaCy/scispaCy model
        nlp = spacy.load("en_core_web_sm")
        USE_SPACY = True

    except Exception:
        USE_SPACY = False

except Exception:
    USE_SPACY = False


def extract_medical_entities(text):

    entities = []

    # =========================
    # spaCy-based extraction
    # =========================
    if USE_SPACY:

        doc = nlp(text)

        for ent in doc.ents:
            entities.append(
                {
                    "text": ent.text,
                    "label": ent.label_
                }
            )

        return entities

    # =========================
    # Fallback lightweight NER
    # =========================

    medical_terms = {
        # Diseases
        "diabetes": "DISEASE",
        "asthma": "DISEASE",
        "cancer": "DISEASE",
        "heart attack": "DISEASE",
        "stroke": "DISEASE",
        "infection": "DISEASE",
        "hypertension": "DISEASE",

        # Symptoms
        "fever": "SYMPTOM",
        "chest pain": "SYMPTOM",
        "breathing difficulty": "SYMPTOM",
        "shortness of breath": "SYMPTOM",
        "cough": "SYMPTOM",
        "headache": "SYMPTOM",
        "fatigue": "SYMPTOM",
        "pain": "SYMPTOM",
        "blurry vision": "SYMPTOM",

        # Treatments
        "treatment": "TREATMENT",
        "medicine": "TREATMENT",
        "insulin": "TREATMENT",
        "therapy": "TREATMENT",
        "surgery": "TREATMENT"
    }

    text_lower = text.lower()

    for term, label in medical_terms.items():

        if term in text_lower:

            entities.append(
                {
                    "text": term,
                    "label": label
                }
            )

    return entities