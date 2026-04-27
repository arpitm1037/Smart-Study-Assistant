# 📌 Smart Study Assistant (GenAI + RAG)

## 🚀 Overview

Smart Study Assistant is a GenAI-powered application that helps students understand computer science concepts using a **Retrieval-Augmented Generation (RAG)** pipeline.

It combines semantic search, embeddings, and LLM responses to generate accurate, context-aware answers while maintaining explainability.

---

## ✨ Features

* 💬 Chat-based AI interface
* 🔍 Semantic search using embeddings
* 📚 Context-aware answers (RAG)
* 🧠 Hybrid mode (documents + LLM fallback)
* 📝 Notes summarization
* ❓ Quiz generation (structured JSON)
* ⚡ FastAPI backend
* 🧾 Source visibility (Documents vs AI Knowledge)

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **LLM:** Gemini / OpenRouter (configurable)
* **Embeddings:** SentenceTransformers
* **Vector Database:** FAISS
* **Frontend:** HTML, CSS, JavaScript

---

## 🧠 How It Works (RAG Pipeline)

User Query
↓
Query Improvement
↓
Text → Embedding (SentenceTransformer)
↓
FAISS Vector Search (Top-K Retrieval)
↓
Similarity Filtering (Threshold)
↓
If relevant context found → RAG Response
Else → LLM Fallback
↓
Final Answer Returned

---

## 📸 Demo / Screenshots

<img width="1280" height="800" alt="Screenshot 2026-04-27 at 19 53 35" src="https://github.com/user-attachments/assets/419cd1a6-2da8-4774-9cb0-8265987d9c3a" />


Suggested:

* Chat interface
* RAG-based answer (with context)
* LLM fallback example

---

## ⚙️ Setup Instructions

Clone the repository:

git clone <your-repo-url>
cd SmartStudyAssistant

Install dependencies:

pip install -r requirements.txt

Run backend:

uvicorn main:app --reload

Open frontend:

frontend/index.html

---

## 📂 Project Structure

* main.py → FastAPI backend
* frontend/ → UI (HTML, CSS, JS)
* embeddings + FAISS → semantic search
* routes → /explain, /summarize, /quiz, /search, /ask

---

## 🔮 Future Improvements

* Streaming responses (real-time typing)
* Improved UI (React-based chat interface)
* Larger domain-specific dataset
* Authentication & user sessions

---

## 🧠 Key Learnings

* Implemented full RAG pipeline
* Understood embeddings and vector search
* Built hybrid AI system (RAG + LLM fallback)
* Designed explainable AI responses
* Integrated backend + frontend system

---

## 📌 Summary

This project demonstrates how modern AI systems combine retrieval and generation to produce accurate, context-aware responses, forming the foundation of real-world AI assistants.
