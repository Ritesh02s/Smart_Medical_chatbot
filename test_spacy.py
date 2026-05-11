import spacy

nlp = spacy.load("en_core_sci_sm")

text = "The patient has chest pain, diabetes, and shortness of breath."

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)