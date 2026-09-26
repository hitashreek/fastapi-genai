from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))
pdf_path = Path(__file__).parent / "data" /"sample.pdf"

# PDF Loader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# Embedding the chunks using OpenAI embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Create a Qdrant Vector Store
vector_store = QdrantVectorStore.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name="sample_collection",
    url="http://localhost:6333"
)

print("Vector store created and documents embedded successfully.")