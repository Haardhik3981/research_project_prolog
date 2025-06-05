from pyswip import Prolog
from Task8_langchain_logic_converter import nl_to_logic_langchain

prolog = Prolog()
prolog.consult("simpsons_kb.pl")

def run_query(nl_question):
    logic_query = nl_to_logic_langchain(nl_question)
    print(f"\nNL Query: {nl_question}")
    print(f"Prolog Query: {logic_query}")
    
    results = list(prolog.query(logic_query.rstrip(".") + "."))
    if not results:
        print("No results.")
    else:
        for res in results:
            print("Yes: ", res)

# Example queries
run_query("Who are Bart's grandparents?")
run_query("Which males are Bart’s parents?")
run_query("Which females are Lisa’s parents?")
