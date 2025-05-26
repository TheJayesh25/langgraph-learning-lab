from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b:int):
    """Addition function that adds 2 numbers only"""
    return a + b 

@tool
def subtract(a: int, b: int):
    """Subtraction function that subtracts 2 numbers only"""
    return a - b

@tool
def multiply(a: int, b: int):
    """Multiplication function that multiplies 2 numbers only"""
    return a * b

tools = [add, subtract, multiply]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my AI assistant. Please answer the query using tools when necessary.")
    response = model.invoke([system_prompt] + state["messages"])
    state["messages"].append(response)
    return {"messages": state["messages"]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"

graph = StateGraph(AgentState)
graph.add_node("Agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))
graph.set_entry_point("Agent")

graph.add_conditional_edges(
    "Agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)
graph.add_edge("tools", "Agent")

app = graph.compile()

# Conversational Loop (Replaces stream)
messages = []
user_input = input("🧑 Human: ")
while user_input.lower() != "exit":
    messages.append(HumanMessage(content=user_input))
    result = app.invoke({"messages": messages})
    messages = result["messages"]

    for msg in messages:
        if isinstance(msg, AIMessage) and msg.content.strip():
            print(f"\n🤖 AI: {msg.content}\n")

    user_input = input("🧑 Human: ")
