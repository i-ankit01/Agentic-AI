from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

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

def samplenode(state : State) :
    print("\n\nSample node reached!", state)
    return {"messages" : ["Hey this is the sample node!"]}

graph_builder = StateGraph(State)

# Add nodes to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

# Define edges between nodes
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages" : ["Hi my name is ankit"]}))
print("\n\nFinal state after graph execution:", updated_state)
