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

## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/arpitm1037/Smart-Study-Assistant.git
cd SmartStudyAssistant

---

### 2. Create Virtual Environment (Recommended)

python3 -m venv venv
source venv/bin/activate

(On Windows)
venv\Scripts\activate

---

### 3. Install Dependencies

pip install -r requirements.txt

---

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

OPENROUTER_API_KEY=your_api_key_here

(Optional if using Gemini)
GEMINI_API_KEY=your_api_key_here

⚠️ Do NOT push this file to GitHub

---

### 5. Run Backend Server

uvicorn main:app --reload

Server will start at:
http://127.0.0.1:8000

You can test APIs here:
http://127.0.0.1:8000/docs

---

### 6. Run Frontend

Open the frontend manually:

frontend/index.html

OR run a simple local server:

cd frontend
python3 -m http.server 5500

Then open:
http://localhost:5500

---

### 📦 Dependencies Used

* fastapi
* uvicorn
* python-dotenv
* numpy
* faiss-cpu
* sentence-transformers
* openai

---

### ✅ System Requirements

* Python 3.9+
* Internet connection (for API calls)
* macOS / Linux / Windows

---

### ⚠️ Important Notes

* Ensure `.env` is not committed (use `.gitignore`)
* First API call may be slightly slow due to model loading
* FAISS runs in-memory (no external database required)

---

### 🎯 Quick Start Summary

1. Install dependencies
2. Add API key in `.env`
3. Run backend
4. Open frontend
5. Start asking questions 🚀


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
