# Task9_langgraph_cot_refinement.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from typing import TypedDict

# === Setup ===
llm = ChatOpenAI(model="gpt-4", temperature=0)

# === Define state schema ===
class GraphState(TypedDict):
    query: str
    thought: str
    refinement: str

# === Node 1: Chain-of-Thought Reasoning ===
def generate_thought(state: GraphState):
    prompt = f"""You are a symbolic reasoner using a knowledge base of facts and rules.

Start by thinking step-by-step about the logical steps needed to answer the query.

Query: {state['query']}

Reasoning:"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"query": state["query"], "thought": response.content.strip()}

# === Node 2: Self-Refinement ===
def refine_thought(state: GraphState):
    prompt = f"""You are reviewing the following reasoning steps made to answer a query:

Query: {state['query']}

Reasoning:
{state['thought']}

Now refine the reasoning and finalize the answer.

Refined Reasoning and Final Answer:"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "query": state["query"],
        "thought": state["thought"],
        "refinement": response.content.strip()
    }

# === LangGraph Setup ===
builder = StateGraph(GraphState)
builder.add_node("generate_thought", generate_thought)
builder.add_node("refine_thought", refine_thought)

builder.set_entry_point("generate_thought")
builder.add_edge("generate_thought", "refine_thought")
builder.add_edge("refine_thought", END)

graph = builder.compile()

# === Run ===
if __name__ == "__main__":
    query = "Who is Bart’s father?"
    final = graph.invoke({"query": query})

    print("🔹 Query:", final["query"])
    print("\n🧠 Chain of Thought:\n", final["thought"])
    print("\n✅ Refined Answer:\n", final["refinement"])