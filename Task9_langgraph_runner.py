from langgraph.graph import StateGraph
from Task7_backward_chaining import print_results
from Task8_langchain_logic_converter import nl_to_logic_langchain
from Task8_Langchain_InferenceEngine import logic_tuple_from_string

class InferenceState:
    def __init__(self, question, logic_query=None):
        self.question = question
        self.logic_query = logic_query

def nl_to_logic_node(state: InferenceState):
    print(f"\n🔹 NL Question: {state.question}")
    state.logic_query = nl_to_logic_langchain(state.question)
    print(f"🔸 Logic Query: {state.logic_query}")
    return state

def logic_executor_node(state: InferenceState):
    goal = logic_tuple_from_string(state.logic_query)
    print_results(state.question, goal)
    return state

def done_node(state: InferenceState):
    return state

# Define graph
builder = StateGraph(InferenceState)
builder.add_node("nl_to_logic", nl_to_logic_node)
builder.add_node("logic_engine", logic_executor_node)
builder.add_node("done", done_node)
builder.set_entry_point("nl_to_logic")
builder.add_edge("nl_to_logic", "logic_engine")
builder.add_edge("logic_engine", "done")
builder.set_finish_point("done")

graph = builder.compile()

# Run
initial = InferenceState("Who are Bart's grandparents?")
graph.invoke(initial)