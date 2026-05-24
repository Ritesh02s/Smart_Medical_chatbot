import spacy


# Load biomedical NLP model
try:
    nlp = spacy.load("en_core_sci_sm")

except:
    nlp = spacy.load("en_core_web_sm")


def extract_medical_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities