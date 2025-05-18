
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def nl_to_logic_gpt(nl_query):
    prompt = f"""You are a logic parser. Convert the following English question into a symbolic Prolog-style logic query.

Use this format:
- Use lowercase atoms only.
- Put the variable (X) **first**, the constant (like 'bart') second.

Question: {nl_query}
Output:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    logic_query = response.choices[0].message.content.strip()
    return logic_query
