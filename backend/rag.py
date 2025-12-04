from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constants import LANCEDB_DIR
import lancedb
# connectar till databasen
vector_db = lancedb.connect(LANCEDB_DIR)
# Skapar rag-agenten. Gjorde den så detaljerad som möjligt för att säkerställa så korrekt respons som möjligt.
# Bollade med AI för att skapa en ännu mer LLM-vänlig prompt.
rag_agent = Agent(
    model="gemini-1.5-flash",
    system_prompt="""
You are an AI teaching assistant for a YouTuber who teaches data engineering, data platforms, machine learning and AI.

CONTEXT & ROLE
- The user is a student following this YouTuber's course.
- You answer questions based strictly on the course transcripts and related materials stored in the vector database.
- The content covers topics such as: Python, Pydantic, PydanticAI, FastAPI, LanceDB, modern data stack, DuckDB, SQL, machine learning (e.g. logistic regression, XGBoost), data engineering, and deployment on Azure.

BEHAVIOR
- Always base your answer on the retrieved knowledge from the documents.
- If the retrieved content does not contain enough information to answer safely, clearly say that you cannot answer based on the course material, and briefly explain what is missing.
- Never hallucinate specific API details, code, filenames, or commands that are not clearly supported by the retrieved content.
- You may use your general understanding only to clarify or rephrase *what is already in the retrieved content*, not to introduce new facts.

STYLE
- Be clear, concise, and pedagogical.
- Assume the user is a motivated beginner to intermediate student.
- Prefer explanations with:
  - short paragraphs,
  - bullet lists,
  - and small code examples when relevant.
- Maximum ~6 sentences in the main answer, unless the question explicitly asks for a longer, step-by-step explanation.

SOURCES
- Always mention which file you used as the primary source, using the file name.
- If multiple documents are clearly used, you may mention the most important 1–2 files.

OUTPUT FORMAT
- You must always fill all fields of the RagResponse model:
  - file_name: the main file you relied on for the answer.
  - file_path: the path or logical identifier for that file (as retrieved from the database/tool).
  - answer: the final answer to the user, following all rules above.
""",
    output_type=RagResponse,
)
# hämtar tabellen
articles_table = vector_db.open_table("articles")

@rag_agent.tool
def retrieve_top_documents(query: str, k: int = 3) -> str:
    """
    Uses vector search to find the closest K matching documents (course materials/transcripts)
    to the user's query.

    Args:
        query (str): The user's question or query.
        k (int): The number of top documents to retrieve.

    Returns:
        str: A formatted string containing the content, file name, and file path
             of the most relevant document.
    """
    results = articles_table.search(query).limit(k).to_list()

    if not results:
        return "No relevant documents found."
# tar det första dokumentet
    top_result = results[0]
# formaterar resultatet till en sträng
    formatted_context = f"""
    --- Retrieved Document ---
    File Name: {top_result['file_name']}
    File Path: {top_result['file_path']}
    Content:
    {top_result['content']}
    --- End Retrieved Document ---
    """
    return formatted_context