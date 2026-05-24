import os

import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv


load_dotenv()


def get_gemini_api_key():
    """
    Works both locally and on Streamlit Cloud.
    Local: reads from .env
    Cloud: reads from Streamlit secrets
    """

    try:
        return st.secrets["GEMINI_API_KEY"]

    except Exception:
        return os.getenv("GEMINI_API_KEY")


genai.configure(
    api_key=get_gemini_api_key()
)


def generate_image_from_prompt(
    prompt,
    output_path="generated_image.png"
):
    """
    Generates an image using Gemini/Imagen if the account supports it.

    Note:
    Imagen access may require paid billing access.
    If unavailable, the app will show a clean error instead of crashing.
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
            "Image generation is configured, but your current Gemini/Imagen "
            "account or SDK does not allow image generation. This usually "
            "requires paid billing access. "
            f"Original error: {e}"
        )