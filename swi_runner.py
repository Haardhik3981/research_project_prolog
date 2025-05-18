from pyswip import Prolog
from nl_to_logic_gpt import nl_to_logic_gpt

prolog = Prolog()
prolog.consult("simpsons_kb.pl")

def run_query(nl_question):
    logic_query = nl_to_logic_gpt(nl_question)
    if logic_query == "UNKNOWN":
        print("Unknown query.")
        return
    results = list(prolog.query(logic_query.rstrip(".") + "."))
    if not results:
        print("No results.")
    for res in results:
        print(res)

# Example query
run_query("Who are Bart's grandparents?")
run_query("Which males are Bart’s parents?")
run_query("Which females are Lisa’s parents?")