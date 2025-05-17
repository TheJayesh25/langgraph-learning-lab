from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, Union
from dotenv import load_dotenv
import os

load_dotenv()  # Loads your .env file

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# Define a single node that processes input and returns output
def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])
    state['messages'].append(AIMessage(content = response.content))
    print(f"\nAI: {response.content}")
    return state

# Construct a simple LangGraph with one node
graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []

if 'logging.txt' in os.listdir():
    file = open('logging.txt','r',encoding='utf-8')
    lines =  file.readlines()
    for line in lines:
        if line.split(':')[0] == 'You':
            conversation_history.append(HumanMessage(content = line[5:].strip()))
        
        if line.split(':')[0] == 'AI':
            conversation_history.append(AIMessage(content = line[5:].strip()))

    file.close()

user_input = input("Enter: ")
while user_input.lower() != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    print(result['messages'])
    conversation_history = result['messages']
    user_input = input("Enter: ")


with open('logging.txt','w',encoding='utf-8') as file:
    for message in conversation_history:
        if isinstance(message,HumanMessage):
            file.write(f'You: {message.content}\n')
        if isinstance(message,AIMessage):
            file.write(f'AI: {message.content}\n')
    file.write('End of Conversation')

print('Conversation saved to logging.txt')