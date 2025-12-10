from fastapi import FastAPI
from backend.data_models import PromptModel, RagResponse
from backend.rag import rag_agent

app = FastAPI(
    title="RAG YouTuber Assistant API",
    description="API for a RAG-based assistant that answers questions about the YouTuber's course content.",
    version="0.1.0",
)

#test
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# endpoint på /rag/query
@app.post("/rag/query", response_model=RagResponse)
# hanterar förfrågningar till endpointen
async def rag_query(prompt_model: PromptModel):
    """
    Process a user query using the RAG agent and return a structured response.
    """
    # anropar rag-agenten med prompten från användaren
    run_result = await rag_agent.run(prompt_model.prompt)

    print("TYPE OF run_result:", type(run_result))

    return run_result.output