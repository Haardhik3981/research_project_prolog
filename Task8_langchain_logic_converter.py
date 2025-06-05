from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

llm = ChatOpenAI(model="gpt-4", temperature=0)

def nl_to_logic_langchain(query):
    prompt = f"""Convert the following natural language question into a symbolic Prolog query.
Use facts like: parent(X,Y), male(X), female(X), grandparent(X,Y), mother(X,Y), etc.

Question: {query}
Answer:"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()