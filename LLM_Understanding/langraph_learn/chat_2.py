from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

openai_llm = init_chat_model(
    model="gpt-5-nano",
    model_provider="openai"
)

gemini_llm = init_chat_model(
    model="gemini-2.0-flash",
    model_provider="google_genai"
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot_openai(state: State):
    print("\n\nchatbot_openai Node", state)
    messages = [{"role": "user", "content": state.get("user_query")}]
    response = openai_llm.invoke(messages)
    state["llm_output"] = response.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("\n\nevaluate_response ", state)
    if True: #hardcoded just for learning
        return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print("\n\nchatbot_gemini Node", state)
    messages = [{"role": "user", "content": state.get("user_query")}]
    response = gemini_llm.invoke(messages)
    state["llm_output"] = response.content
    return state

def endnode(state: State):
    print("\n\nendnode Node", state)
    return state

graph_builder = StateGraph(State)

# Adding/Registering nodes to langgraph graphBuilder
graph_builder.add_node("chatbot_openai", chatbot_openai)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

# Adding/creating the edges/connections on langgraph graphBuilder
graph_builder.add_edge(START, "chatbot_openai")
graph_builder.add_conditional_edges("chatbot_openai", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "If 3x-7=20, find x^2-4x"}))
print(f"\n\n", updated_state)
