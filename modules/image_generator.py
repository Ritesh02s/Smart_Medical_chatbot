import os
from turtle import st

import google.generativeai as genai

from dotenv import load_dotenv

import streamlit as st




load_dotenv()

genai.configure(
    api_key=st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
)


def generate_image_from_prompt(
    prompt,
    output_path="generated_image.png"
):
    """
    Image generation placeholder using Gemini/Imagen access.

    Note:
    Imagen access may require paid billing access.
    If unavailable, this function raises a clear error instead of
    breaking the full chatbot.
    """

    try:
        model = genai.ImageGenerationModel(
            "imagen-3.0-generate-002"
        )

        result = model.generate_images(
            prompt=prompt,
            number_of_images=1
        )

        image = result.images[0]
        image.save(output_path)

        return output_path

    except Exception as e:
        raise RuntimeError(
            "Image generation is configured, but the current "
            "Gemini/Imagen account or SDK does not allow image generation. "
            "This usually requires paid billing access. "
            f"Original error: {e}"
        )