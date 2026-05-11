from modules.medical_ner import extract_medical_entities


text = """
I have chest pain, diabetes, fever,
and breathing difficulty.
"""


entities = extract_medical_entities(text)


for entity in entities:

    print(entity)