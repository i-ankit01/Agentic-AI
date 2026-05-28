from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Optional, Literal
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_response: Optional[str]
    is_good : Optional[bool]

def chatbot(state : State) :
    print("\n\nChatbot node reached! Current state:", state)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": state["user_query"]}]
    )

    state["llm_response"] = response.choices[0].message.content
    return state

def evaluate_response(state : State) -> Literal["gemini_chatbot", "endnode"]:
    print("\n\nEvaluating response! Current state:", state)
    if True:
        return 'endnode'
    
    return 'gemini_chatbot'

def endnode(state : State) :
    print("\n\nEnd node reached! Final state:", state)
    return state

def gemini_chatbot(state : State) :
    print("\n\nGemini chatbot node reached! Current state:", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("evaluate_response", evaluate_response)
graph_builder.add_node("endnode", endnode)
graph_builder.add_node("gemini_chatbot", gemini_chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("gemini_chatbot", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query" : "Hi my name is ankit"}))
print("\n\nFinal state after graph execution:", updated_state)