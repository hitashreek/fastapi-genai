from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()  # Load environment variables from .env file
import os

pdf_path = Path(__file__).parent / "data" / "sample.pdf"

# PDF Loader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=400
)
chunks = text_splitter.split_documents(docs)

# Embedding the chunks using OpenAI embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create a Qdrant Vector Store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"
)

print("Vector store created and documents embedded successfully.")  # python -m app.index req to run Lecture 46. 09:05