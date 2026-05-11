import spacy


# Load biomedical NLP model
nlp = spacy.load("en_core_sci_sm")


def extract_medical_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities