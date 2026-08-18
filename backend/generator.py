import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a GATE CSE Operating Systems tutor. Answer using ONLY the provided context.
If the context doesn't contain the answer, say so honestly.
When explaining a concept with a natural diagram (state transitions, process flow, resource allocation graphs),
include a Mermaid diagram in a ```mermaid code block after your explanation.
Always cite which section/page your answer comes from."""

def generate_answer(query, retrieved_chunks):
    context = "\n\n".join(
        f"[Section: {c['section']}, Page: {c['page']}]\n{c['text']}"
        for c in retrieved_chunks
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )

    sources = [{"section": c["section"], "page": c["page"]} for c in retrieved_chunks]
    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }