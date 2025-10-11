from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag_pipeline import get_answer


app = FastAPI(
    title="AI Assistant for French Government Services",
    description="RAG-powered API using Claude + LangChain + FAISS",
    version="1.0"
)

class Question(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(item: Question):
    try:
        result = get_answer(item.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
