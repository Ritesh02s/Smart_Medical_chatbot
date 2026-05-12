import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def generate_rag_response(query, context, domain):

    prompt = f"""
You are an expert AI assistant specialized in {domain}.

Use the provided context to answer the user's question clearly and naturally.

Rules:
- Explain concepts in simple terms first.
- Then provide technical details if relevant.
- Combine information from multiple retrieved contexts.
- Do NOT just summarize papers individually.
- Answer conversationally like a knowledgeable expert.
- If the context is insufficient, say so honestly.

Context:
{context}

User Question:
{query}

Provide a detailed but easy-to-understand response.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception:

        return (
            f"LLM generation unavailable. "
            f"Showing retrieved {domain} context:\n\n"
            + context
        )