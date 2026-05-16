from modules.llm import model


def translate_to_english(text, language):

    if language == "en":
        return text

    prompt = f"""
Translate this to English.

Text:
{text}

Return ONLY English translation.
"""

    response = model.generate_content(prompt)

    translated = response.text.strip()

    print("TRANSLATED:", translated)

    return translated