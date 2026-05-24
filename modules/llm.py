import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def get_gemini_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")


genai.configure(
    api_key=get_gemini_api_key()
)

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def generate_rag_response(query, context, domain, language, history=""):

    prompt = f"""
You are an expert AI assistant specialized in {domain}.

IMPORTANT:
- The user's language is: {language}
- Your ENTIRE response MUST be in {language}
- Do NOT answer in English unless language == 'en'
- Explain clearly and naturally
- Use ONLY the provided context
- If context is insufficient, say so honestly

Context:
{context}

Conversation History:
{history}

User Question:
{query}

Generate the response completely in {language}.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception:

        return (
            f"LLM generation is currently unavailable. "
            f"Based on the retrieved {domain} knowledge, here is the relevant information:\n\n"
            + context[:2000]
        )