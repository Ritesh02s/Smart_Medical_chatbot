from PIL import Image

import google.generativeai as genai


def analyze_image(image_file, user_query):

    image = Image.open(image_file)

    prompt = f"""
Analyze the uploaded image.

User question:
{user_query}

Provide a helpful explanation.
"""

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    response = model.generate_content(
        [prompt, image]
    )

    return response.text