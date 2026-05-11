import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def generate_medical_response(query, medical_context):
    prompt = f"""
You are a helpful medical AI assistant.

Use ONLY the provided medical context.

Medical Context:
{medical_context}

User Question:
{query}

Give a clear and concise answer.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return (
            "Gemini quota is currently unavailable, so I am showing the retrieved "
            "medical information directly:\n\n"
            + medical_context
        )