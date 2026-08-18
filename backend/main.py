from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retriever import retrieve
from generator import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # vite default
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query(req: QueryRequest):
    chunks = retrieve(req.query)
    result = generate_answer(req.query, chunks)
    return result

@app.get("/health")
def health():
    return {"status": "ok"}