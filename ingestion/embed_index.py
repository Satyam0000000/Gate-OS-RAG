import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))

COLLECTION_NAME = "gate_os"

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def build_index(chunks_path="data/chunks.jsonl"):
    chunks = []
    with open(chunks_path) as f:
        for line in f:
            chunks.append(json.loads(line))

    # create collection (1536 dims for text-embedding-3-small)
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

    BATCH_SIZE = 50
    points = []

    for i, chunk in enumerate(chunks):
        vector = embed_text(chunk["text"])

        points.append(PointStruct(
            id=i,
            vector=vector,
            payload=chunk,
        ))

        if (i + 1) % 20 == 0:
            print(f"Embedded {i + 1}/{len(chunks)}")

        # Upload each group immediately, then clear it from memory
        if len(points) == BATCH_SIZE or i == len(chunks) - 1:
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
            )
            print(f"Uploaded {i + 1}/{len(chunks)} to Qdrant")
            points = []

    print(f"Indexed {len(chunks)} chunks into Qdrant")

if __name__ == "__main__":
    build_index()