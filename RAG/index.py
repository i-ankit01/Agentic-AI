from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()


# Path to the PDF located in the same folder as this script
pdf_path = Path(__file__).parent / "Ankit_CV.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# print(docs[0])

# Chunk the documents using a recursive character splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents=docs)


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

print("Vector store created successfully!")
