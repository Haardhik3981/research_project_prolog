# backward_chaining.py

# === Knowledge Base ===

facts = [
    ("male", "homer"), ("male", "bart"), ("male", "abe"),
    ("female", "marge"), ("female", "lisa"), ("female", "maggie"), ("female", "mona"),
    ("parent", "homer", "bart"), ("parent", "homer", "lisa"), ("parent", "homer", "maggie"),
    ("parent", "marge", "bart"), ("parent", "marge", "lisa"), ("parent", "marge", "maggie"),
    ("parent", "abe", "homer"), ("parent", "mona", "homer")
]

rules = [
    (("mother", "?X", "?Y"), [("parent", "?X", "?Y"), ("female", "?X")]),
    (("father", "?X", "?Y"), [("parent", "?X", "?Y"), ("male", "?X")]),
    (("son", "?X", "?Y"), [("parent", "?Y", "?X"), ("male", "?X")]),
    (("daughter", "?X", "?Y"), [("parent", "?Y", "?X"), ("female", "?X")]),
    (("grandparent", "?X", "?Y"), [("parent", "?X", "?Z"), ("parent", "?Z", "?Y")])
]

# === Utilities ===

def unify(pattern, datum, env):
    """Attempt to unify a pattern with a datum given the environment."""
    if len(pattern) != len(datum):
        return None
    new_env = env.copy()
    for p, d in zip(pattern, datum):
        val_p = new_env.get(p, p)
        val_d = new_env.get(d, d)
        if val_p.startswith("?"):
            new_env[val_p] = val_d
        elif val_d.startswith("?"):
            new_env[val_d] = val_p
        elif val_p != val_d:
            return None
    return new_env

def substitute(term, env):
    return tuple(env.get(arg, arg) for arg in term)

# === Recursive Backward Chaining Engine ===

def backward_chain(goal, env):
    print(f"Goal: {goal} with env {env}")

    # Check all matching facts
    for fact in facts:
        if fact[0] != goal[0]: continue
        new_env = unify(goal, fact, env)
        if new_env:
            yield new_env

    # Try matching rules
    for head, body in rules:
        if head[0] != goal[0]: continue
        rule_env = unify(goal, head, env)
        if not rule_env:
            continue
        body_substituted = [substitute(term, rule_env) for term in body]
        yield from prove_all(body_substituted, rule_env)

def prove_all(goals, env):
    if not goals:
        yield env
    else:
        first, *rest = goals
        for new_env in backward_chain(first, env):
            yield from prove_all(rest, new_env)

# === Query Runner ===

def print_results(query_text, goal):
    print(f"\nQuery: {query_text}")
    found = False
    for result in backward_chain(goal, {}):
        found = True
        answer = {k: v for k, v in result.items() if k.startswith("?")}
        if answer:
            print("Answer:", ", ".join(f"{k} = {v}" for k, v in answer.items()))
    if not found:
        print("No answer found.")

# === Run Sample Queries ===

if __name__ == "__main__":
    print_results("Who are Bart's grandparents?", ("grandparent", "?X", "bart"))
    print_results("Who is Lisa's mother?", ("mother", "?X", "lisa"))
    print_results("Who is Homer’s son?", ("son", "?X", "homer"))
    print_results("Who is Marge’s daughter?", ("daughter", "?X", "marge"))