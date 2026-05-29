from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
)



class State(TypedDict):
    # Define messages (a list type, with the add_messages function used to append messages)
    messages: Annotated[list, add_messages]

def chatbot(state : State) :
    # print("\n\nChatbot node reached!", state)
    response = llm.invoke(state.get("messages"))
    return {"messages" : [response]}


graph_builder = StateGraph(State)


# Add nodes to the graph
graph_builder.add_node("chatbot", chatbot)

# Define edges between nodes
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# graph = graph_builder.compile()

def compile_graph_with_checkpoint(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


MONGODB_URI = "mongodb+srv://ankit:uDCdC4pOeZqngMjp@cluster0.nxp5e.mongodb.net/AgeticAI"
with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    graph_with_checkpoint = compile_graph_with_checkpoint(checkpointer)

    config = {
            "configurable": {
                "thread_id": "ankit"
            }
        }

    for chunk in graph_with_checkpoint.stream(
        State({"messages" : ["What is my name"]}),
        config, 
        stream_mode="values"
        ):
        chunk["messages"][-1].pretty_print()
    
    # print("\n\nFinal state after graph execution:", updated_state)
