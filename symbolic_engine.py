# symbolic_engine.py

from nl_to_logic_gpt import nl_to_logic_gpt
# STEP 1: Load and parse the KB facts (simulating Prolog)

# Male and female sets
male = {"homer", "bart", "abe"}
female = {"marge", "lisa", "maggie", "mona"}

# Parent relationships
parent = {
    ("homer", "bart"),
    ("homer", "lisa"),
    ("homer", "maggie"),
    ("marge", "bart"),
    ("marge", "lisa"),
    ("marge", "maggie"),
    ("abe", "homer"),
    ("mona", "homer")
}

# Print results to verify
print("✅ Knowledge base loaded:")
print("Males:", male)
print("Females:", female)
print("Parents:", parent)

# STEP 2: Test GPT-based conversion
query = "Who are Bart's grandparents?"
logic_query = nl_to_logic_gpt(query)
# Normalize GPT output
logic_query = logic_query.strip().lower().rstrip(".")
logic_query = logic_query.replace("grandparents", "grandparent")
print("🧠Logic Query:", logic_query)