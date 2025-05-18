from openai import OpenAI
import os

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load facts from simpsons_kb.txt
with open("simpsons_kb.txt", "r") as f:
    facts = f.read()

# Questions and expected answers
questions = {
    "Who are Bart's grandparents?": ["Abe", "Mona"],
    "Who is Bart’s mother?": ["Marge"],
    "Is Homer Lisa's father?": ["Yes", "Homer"],
    "List all males.": ["Homer", "Bart", "Abe"],
    "List all females.": ["Marge", "Lisa", "Maggie", "Mona"],
    "Who is Maggie's father?": ["Homer"],
    "Is Marge Lisa’s mother?": ["Yes", "Marge"],
    "Does Abe have any grandchildren?": ["Bart", "Lisa", "Maggie"]
}

log_file = open("results/output_log.txt", "w")

# Query GPT
for q, expected in questions.items():
    prompt = f"""
You are a logical reasoner. Use the facts below to answer the question.

{facts}

Question: {q}
Answer:
"""
    print(f"\n🔹 {q}")
    log_file.write(f"\n🔹 {q}\n")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    answer = response.choices[0].message.content.strip()
    print(f"LLM Answer: {answer}")
    print(f"Expected: {expected}")
    print("✅ Match" if all(e.lower() in answer.lower() for e in expected) else "❌ Mismatch")

    log_file.write(f"LLM Answer: {answer}\nExpected: {expected}\n")
    log_file.write("✅ Match\n" if all(e.lower() in answer.lower() for e in expected) else "❌ Mismatch\n")

log_file.close()