from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def nl_to_logic_gpt(query):
    prompt = f"""Convert the following natural language question into a symbolic Prolog query.
    Use facts like: parent(X,Y), male(X), female(X), grandparent(X,Y), mother(X,Y), etc.

    Question: {query}
    Answer:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()
