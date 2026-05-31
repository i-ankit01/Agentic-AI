from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json

load_dotenv()

openai_client = OpenAI() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    "embedder" : {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": OPENAI_API_KEY
        }
    },
    "llm" : {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "api_key": OPENAI_API_KEY
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("Ask AI >> ")

    search_memory = mem_client.search(query=user_query, filters={"user_id": "ankit"})

    memories = [
        f"ID : {mem.get("id")} \n Memory : {mem.get("memory")}\n\n"
        for mem in search_memory.get("results")
    ]

    print("Relevant Memories >> ", memories)

    SYSTEM_PROMPT = f"""Here are some relevant memories from the past interactions with the user :
    \n\n {json.dumps(memories)} \n\n Use these memories to answer the user's query.
    If the memories are not relevant, you can ignore them. 
    Always try to use the memories to provide a better answer to the user query."""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ])

    ai_response = response.choices[0].message.content

    print("AI Response >> ", ai_response)

    mem_client.add(
        user_id="ankit",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("Memory added to vector store!")
