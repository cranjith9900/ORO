import os
from sqlalchemy.orm import Session
from openai import AzureOpenAI

from .models import Document

# ---------- Azure Client ----------
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


# ---------- EMBEDDINGS ----------
def get_embeddings(texts: list[str]):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [d.embedding for d in response.data]


# ---------- STORE ----------
def store_chunks(db: Session, chunks: list[str], source: str):
    embeddings = get_embeddings(chunks)

    for chunk, embedding in zip(chunks, embeddings):
        doc = Document(
            content=chunk,
            source=source,
            embedding=embedding
        )
        db.add(doc)

    db.commit()


# ---------- SEARCH ----------
def search_chunks(db: Session, query: str):
    query_embedding = get_embeddings([query])[0]

    results = db.query(Document).order_by(
        Document.embedding.l2_distance(query_embedding)
    ).limit(5).all()

    return [r.content for r in results]


# ---------- GENERATE ----------
def generate_answer(query: str, chunks: list[str]):
    if not chunks:
        return "No relevant information found in documents."

    context = "\n\n".join(chunks)

    prompt = f"""
You are a strict assistant.

Rules:
- Answer ONLY from the provided context
- If answer not found, say "I don't know based on the provided data"

Context:
{context}

Question:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # ✅ your Azure deployment
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", str(e))
        return "Error generating response"