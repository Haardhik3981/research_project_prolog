import os
from openai import OpenAI
from pyswip import Prolog

# Initialize OpenAI client
client = OpenAI(api_key="my-key")

# Step 1: Call ChatGPT
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Write Prolog rules to represent when depth-first search (DFS) is better than bfs."}
    ]
)

prolog_code = response.choices[0].message.content
print("\nProlog rules returned by GPT:\n")
print(prolog_code)
