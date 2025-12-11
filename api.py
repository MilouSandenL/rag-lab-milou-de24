from fastapi import FastAPI
from backend.data_models import PromptModel, RagResponse
from backend.rag import rag_agent

app = FastAPI(
    title="RAG YouTuber Assistant API",
    description="API for a RAG-based assistant that answers questions about the YouTuber's course content.",
    version="0.1.0",
)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/rag/query", response_model=RagResponse)
async def rag_query(prompt_model: PromptModel):
    """
    Process a user query using the RAG agent and return a structured response.
    """
    run_result = await rag_agent.run(prompt_model.prompt)
    print("TYPE OF run_result:", type(run_result))
    return run_result.output