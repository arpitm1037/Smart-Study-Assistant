import os
import json
import re
import numpy as np
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- OPENROUTER CLIENT ----------------

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8000",  # REQUIRED
        "X-Title": "SmartStudyAssistant"          # REQUIRED
    }
)

# ---------------- REQUEST MODELS ----------------

class TopicRequest(BaseModel):
    topic: str

class NotesRequest(BaseModel):
    notes: str

class SearchRequest(BaseModel):
    query: str

class AskRequest(BaseModel):
    query: str


# ---------------- GENERATION (GROK via OpenRouter) ----------------

def generate_text(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


@app.post("/explain")
def explain(data: TopicRequest):
    prompt = f'Explain "{data.topic}" in one simple sentence.'
    return {"result": generate_text(prompt)}


@app.post("/summarize")
def summarize(data: NotesRequest):
    prompt = f"Summarize in 5 bullet points:\n{data.notes}"
    return {"result": generate_text(prompt)}


@app.post("/quiz")
def quiz(data: TopicRequest):
    prompt = f"""
Generate 3 quiz questions with answers on "{data.topic}".

Return ONLY JSON:
{{
  "questions": [
    {{"question": "...", "answer": "..."}}
  ]
}}
"""
    try:
        return json.loads(generate_text(prompt))
    except:
        return {"error": "Invalid JSON"}


# ---------------- EMBEDDINGS (OPENROUTER) ----------------

def get_embedding(text):
    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# ---------------- CHUNKING ----------------

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


def chunk_sentences(text, max_sentences=2):
    sentences = split_sentences(text)
    return [
        " ".join(sentences[i:i+max_sentences])
        for i in range(0, len(sentences), max_sentences)
    ]


# ---------------- DOCUMENTS ----------------

documents = []
index = None


def build_documents():
    global documents

    raw_texts = [
        "Recursion is a programming technique where a function calls itself. It must include a base case.",
        "Stack follows LIFO principle. It is used in recursion.",
        "Queue follows FIFO principle.",
        "Binary search works on sorted arrays.",
        "Process is a program in execution.",
        "Thread is a lightweight process.",
        "Database stores structured data.",
        "HTTP is a web communication protocol.",
        "TCP ensures reliable data transfer.",
        "Encapsulation hides internal details."
    ]

    documents = []
    for text in raw_texts:
        documents.extend(chunk_sentences(text))


# ---------------- FAISS ----------------

def initialize_faiss():
    global index

    if index is None:
        embeddings = [get_embedding(doc) for doc in documents]
        vectors = np.array(embeddings).astype("float32")

        dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)

        print("FAISS ready:", index.ntotal)


# ---------------- QUERY IMPROVEMENT ----------------

def improve_query(query):
    prompt = f"Rewrite this query clearly:\n{query}"
    return generate_text(prompt).strip()


# ---------------- SEARCH ----------------

@app.post("/search")
def search(data: SearchRequest):
    initialize_faiss()

    query = improve_query(data.query)
    query_embedding = get_embedding(query)

    q = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(q, 5)

    best_idx = indices[0][0]
    best_doc = documents[best_idx]

    return {
        "query": data.query,
        "improved_query": query,
        "result": best_doc
    }


# ---------------- HYBRID RAG ----------------

@app.post("/ask")
def ask(data: AskRequest):
    initialize_faiss()

    query = improve_query(data.query)
    query_embedding = get_embedding(query)

    q = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(q, 5)

    results = [
        (documents[idx], float(distances[0][i]))
        for i, idx in enumerate(indices[0])
    ]

    # 🔹 Threshold filtering
    THRESHOLD = 1.5
    filtered = [(doc, score) for doc, score in results if score < THRESHOLD]

    # ---------------- CASE 1: NO CONTEXT ----------------
    if not filtered:
        fallback_prompt = f"""
Answer clearly and simply:

Question: {query}
"""
        answer = generate_text(fallback_prompt)

        return {
            "answer": answer,
            "context": [],
            "mode": "LLM"
        }

    # ---------------- CASE 2: USE RAG ----------------

    top_docs = [doc for doc, _ in filtered[:3]]

    context = "\n".join([f"{i+1}. {d}" for i, d in enumerate(top_docs)])

    prompt = f"""
Answer using ONLY the context below.

Context:
{context}

Question:
{query}

Rules:
- Answer in 1–2 sentences
- Do NOT use outside knowledge
- If not found, say "I don't know"
"""

    answer = generate_text(prompt)

    # 🔥 FIX: fallback if weak answer
    if "i don't know" in answer.lower():
        fallback_prompt = f"""
Answer clearly using your knowledge:

Question: {query}
"""
        fallback_answer = generate_text(fallback_prompt)

        return {
            "answer": fallback_answer,
            "context": [],
            "mode": "LLM"
        }

    # ✅ Valid RAG answer
    return {
        "answer": answer,
        "context": top_docs,
        "mode": "RAG"
    }


# ---------------- INIT ----------------
build_documents()