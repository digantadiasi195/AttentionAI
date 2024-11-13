# src/api/endpoints.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..agents.search_agent import SearchAgent
from ..models.llm_manager import LLMManager
from ..database.neo4j_client import Neo4jClient

app = FastAPI()
search_agent = SearchAgent()
llm_manager = LLMManager()
db_client = Neo4jClient()

class SearchRequest(BaseModel):
    topic: str

class QuestionRequest(BaseModel):
    question: str
    paper_ids: List[str]

@app.post("/search")
async def search_papers(request: SearchRequest):
    try:
        papers = search_agent.search_papers(request.topic)
        return {"papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer")
async def answer_question(request: QuestionRequest):
    try:
        # Get papers from database
        papers = []
        for paper_id in request.paper_ids:
            paper = db_client.get_papers_by_id(paper_id)
            if paper:
                papers.append(paper)
        
        answer = llm_manager.answer_question(request.question, papers)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_papers(paper_ids: List[str]):
    try:
        papers = []
        for paper_id in paper_ids:
            paper = db_client.get_papers_by_id(paper_id)
            if paper:
                papers.append(paper)
        
        summary = llm_manager.summarize_papers(papers)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/future-directions")
async def get_future_directions(paper_ids: List[str]):
    try:
        papers = []
        for paper_id in paper_ids:
            paper = db_client.get_papers_by_id(paper_id)
            if paper:
                papers.append(paper)
        
        directions = llm_manager.generate_future_directions(papers)
        return {"future_directions": directions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))