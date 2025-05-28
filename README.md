# LangGraph Learning Lab

This repository contains a series of small experiments I built while learning LangGraph fundamentals.

The goal was to understand how graph-based agent orchestration works by building progressively more complex workflows.

---

## Repo structure (as of now) - 

```
langgraph-learning-lab
│
├── README.md
│
├── basics
│   ├── graph_1_hello_world.py
│   ├── graph_2_state_mutation.py
│   └── graph_3_sequential_nodes.py
│
├── control_flow
│   ├── graph_4_conditional_edges.py
│   └── graph_5_loop_counter.py
│
├── agents
│   ├── simple_agent.py
│   ├── memory_agent.py
│   └── react_style_agent.py
│
└── utils
    └── helpers.py

```

---

## Experiments include:
• Basics
- State graphs exploring basic implementation 
- State mutation
- sequential node execution


• Control Flow
- Exploring conditional edges &
- looped workflows


• Agents 
- Simple LLM Agents and implementation using LangGraph
- agents with memory, utilization, preserving conversations by logging them and reusing next time, etc.
- tool-using ReAct-style agents