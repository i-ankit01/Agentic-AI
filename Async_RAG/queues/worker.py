from dotenv import load_dotenv
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from functools import lru_cache
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "learning_rag")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


@lru_cache(maxsize=1)
def get_openai_client():
    return OpenAI()


@lru_cache(maxsize=1)
def get_vector_db():
    embedding_model = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )
    return QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        collection_name=QDRANT_COLLECTION,
        url=QDRANT_URL,
    )

def process_query(query : str):

    print("Received query and searching for chunks >> : ", query)

    # Performing similarity search on the vector store
    vector_db = get_vector_db()
    results = vector_db.similarity_search(query=query , k=3) 

    retrieved_docs = []
    for result in results:
        retrieved_docs.append(
            {
                "page_number": result.metadata["page_label"],
                "page_content": result.page_content,
            }
        )

    # Convert retrieved documents to string format for better readability and to use it in the prompt
    retrieved_docs_str = ""
    for doc in retrieved_docs:
        retrieved_docs_str += f"Page Number: {doc['page_number']}\nContent: {doc['page_content']}\n\n"

    SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions based on the following retrieved documents with page number and page_contents.

context:
{retrieved_docs_str}
"""

    openai_client = get_openai_client()
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    print("Response from OpenAI >> : ", response.choices[0].message.content)
    return response.choices[0].message.content