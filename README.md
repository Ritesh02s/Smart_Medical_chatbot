# Smart Medical AI Chatbot

An AI-powered medical and research assistant built using Streamlit, ChromaDB, NLP pipelines, and Gemini API.

This project started as a medical Q&A chatbot and gradually evolved into a unified AI system capable of:

- Medical question answering
- Research paper retrieval
- Multilingual interaction
- Sentiment-aware responses
- Conversational memory
- Dynamic knowledge base expansion
- Multimodal image understanding

The goal of this project was to explore how modern AI systems combine Retrieval-Augmented Generation (RAG), vector databases, embeddings, LLMs, and multimodal AI into a single application.

---

# Features

## Medical Question Answering
- Uses MedQuAD dataset
- Semantic retrieval using embeddings + ChromaDB
- Medical entity extraction
- Context-aware medical responses

## Research Expert Chatbot
- Uses arXiv AI/ML papers
- Research paper retrieval
- Related paper search UI
- Concept relevance visualization

## Multilingual Support
Supports:
- English
- Hindi
- Spanish
- French

Uses:
- language detection
- translation-based routing
- multilingual response generation

## Sentiment Analysis
Detects:
- positive
- negative
- neutral sentiment

Responses adapt based on emotional tone.

## Conversational Memory
Uses Streamlit session state to:
- remember previous messages
- handle follow-up questions
- improve contextual understanding

## Dynamic Knowledge Base Expansion
Users can:
- upload PDFs/TXT files
- automatically chunk documents
- generate embeddings
- update vector database dynamically

## Multimodal AI
Supports:
- medical image upload
- image understanding using Gemini Vision
- report explanation

---

# Tech Stack

Frontend:
- Streamlit

Backend / AI:
- Python
- Google Gemini API
- NLP pipelines
- Transformers

Vector Database:
- ChromaDB

Libraries:
- langdetect
- sentence-transformers
- matplotlib
- pandas
- nltk
- APScheduler

---

# Project Structure

Smart_chatbot/
│
├── app.py
├── scheduler.py
├── requirements.txt
│
├── modules/
│   ├── chatbot.py
│   ├── embeddings.py
│   ├── medical_ner.py
│   ├── multilingual.py
│   ├── sentiment.py
│   ├── research_chatbot.py
│   ├── image_analyzer.py
│   ├── image_generator.py
│   └── memory.py
│
├── data/
│   ├── medquad/
│   └── arxiv/
│
├── chroma_db/
│
└── uploads/


# Installation

Clone the repository:

git clone https://github.com/Ritesh02s/Smart_Medical_chatbot.git
cd Smart_Medical_chatbot

Create virtual environment:

python -m venv venv

Activate environment:

Windows
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file:

GEMINI_API_KEY=your_api_key_here
Run the Application
streamlit run app.py

## Example Queries

Medical:

What are symptoms of diabetes?
I have chest pain and breathing difficulty.

Research:

What are transformers in deep learning?

Multilingual: 

मधुमेह के लक्षण क्या हैं?

¿Cuáles son los síntomas de la diabetes?

# Challenges Faced

Some major issues encountered during development:

multilingual intent routing failures
Gemini API quota limitations
Streamlit rerun issues
vector database duplication
research retrieval inaccuracies
conversational memory handling
package compatibility issues

Most of these were solved through:

translation-based routing
retrieval fallback mechanisms
session-state memory
dataset filtering
modular architecture improvements
Future Improvements

Planned improvements:

better medical intent classification
improved research retrieval ranking
stronger conversational memory
full deployment support
better multimodal reasoning
hybrid search (BM25 + semantic retrieval)