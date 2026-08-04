from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.fetch import fetch_papers
from src.summarize import summarize_papers
from src.cluster import cluster_papers


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ml-research-agent.vercel.app",
        "https://ml-research-agent.onrender.com"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LandscapeRequest(BaseModel):
    query: str
    max_results: int = 10

@app.post("/api/landscape")
async def get_landscape(request: LandscapeRequest):
    papers = fetch_papers(request.query, max_results=request.max_results)
    summarized_papers = summarize_papers(papers)
    clustered_papers = cluster_papers(summarized_papers)
    return {"papers": clustered_papers}