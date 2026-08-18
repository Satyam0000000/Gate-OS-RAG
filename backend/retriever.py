import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from sentence_transformers import CrossEncoder

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")  # free, local

COLLECTION_NAME = "gate_os"

def embed_query(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding

def retrieve(query, top_k=20, final_k=5):
    query_vector = embed_query(query)
    results = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=top_k
).points

    candidates = [(r.payload["text"], r.payload) for r in results]

    # rerank
    pairs = [[query, text] for text, _ in candidates]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(scores, candidates), key=lambda x: x[0], reverse=True)
    top_results = [payload for _, (text, payload) in ranked[:final_k]]

    return top_results