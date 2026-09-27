from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from fastapi import APIRouter
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()
import os

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Embedding the chunks using OpenAI Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"
)
    
@router.post("/")
async def query(question: str):
    search_results =  vector_db.similarity_search(question)
    print(f"Search results: {search_results}")
    
    context = " ".join(
        [
            f"Page {result.metadata.get('page', 'unknown')}: {result.page_content}"
            for result in search_results
        ]
    )
        
    SYSTEM_PROMPT = f"""
    You are a helpful assistant that answers questions based on the provided context.
    If the context does not contain the answer, say "I don't know".
    
    Also include the page number and the context in your answer if applicable.
    
    Context:
    {context}
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
    )
    
    return {"question": question, "results": response.choices[0].message.content}
    