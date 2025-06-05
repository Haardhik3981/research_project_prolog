# Task8_langchain_backchain_runner.py

from Task7_backward_chaining import print_results
from Task8_langchain_logic_converter import nl_to_logic_langchain

def logic_tuple_from_string(logic_str):
    """Converts a logic query string like mother(X, 'lisa') to a tuple ('mother', '?X', 'lisa')."""
    logic_str = logic_str.strip().rstrip('.')
    pred, args = logic_str.split("(", 1)
    args = args.rstrip(")").split(",")

    converted_args = []
    for arg in args:
        arg = arg.strip().strip("'\"")  # remove quotes
        if arg[0].isupper():  # treat uppercase as variable
            converted_args.append(f"?{arg.lower()}")
        else:
            converted_args.append(arg.lower())  # constant

    return tuple([pred.strip().lower()] + converted_args)


# === Run Queries with LangChain ===

queries = [
    "Who are Bart's grandparents?",
    "Who is Lisa's mother?",
    "Who is Homer’s son?",
    "Who is Marge’s daughter?"
]

for question in queries:
    print(f"\n🔹 NL Query: {question}")
    logic_query = nl_to_logic_langchain(question)
    print(f"🔸 Logic Query: {logic_query}")
    try:
        goal = logic_tuple_from_string(logic_query)
        print_results(question, goal)
    except Exception as e:
        print("❌ Failed to parse logic query:", e)