from pydantic import BaseModel, Field
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

embedding_model = get_registry().get("gemini-text").create(
    name="models/text-embedding-004"
)

class Article(LanceModel):
    """
    Representerar ett dokument (en kurs-/video-fil) i min LanceDB-tabell.
    """
    doc_id: str
    file_name: str
    content: str = embedding_model.SourceField()
    embedding: Vector(embedding_model.ndims()) = embedding_model.VectorField() # type: ignore

class PromptModel(BaseModel):
    prompt: str = Field(description="User question about the course content")

class RagResponse(BaseModel):
    file_name: str = Field(
        description="File name of the retrieved source file (without extension or with, depending on design)."
    )
    file_path: str = Field(
        default="N/A", # Lägg till default-värde här
        description="Absolute or logical path to the retrieved source file."
    )
    answer: str = Field(
        description="Answer based on the retrieved knowledge from the source file."
    )