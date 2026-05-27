from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()  # Initialize the OpenAI client

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

# Taking input from the user
query = input("Ask AI >> :  ")

# Performing similarity search on the vector store
results = vector_db.similarity_search(query=query , k=3) 
# what is k here? k is the number of similar documents (chunks) we want to retrieve from the vector store based on the query. 

# is it okay to have this in array or should be converted to string? It depends on how you want to use the retrieved documents in the next steps. If you want to pass them as context to a language model, it might be better to convert them into a string format that can be easily incorporated into the prompt. However, if you want to keep them structured for further processing, keeping them in an array format could be beneficial.

retrieved_docs = []
for result in results:
    retrieved_docs.append(
        {
            "page_number": result.metadata["page_label"],
            "page_content": result.page_content,
        }
    )

#convert this to string format for better readability and to use it in the prompt
retrieved_docs_str = ""
for doc in retrieved_docs:
    retrieved_docs_str += f"Page Number: {doc['page_number']}\nContent: {doc['page_content']}\n\n"


# print("Retrieved Documents >> : ", retrieved_docs_str)

SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions based on the following retrieved documents with page number and page_contents.

context:
{retrieved_docs_str}

"""

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ],
)

print("AI Response >> : ", response.choices[0].message.content)