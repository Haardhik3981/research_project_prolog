# Task9_langgraph_rag_judge.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage
from langchain.chains import RetrievalQA
from langgraph.graph import END, StateGraph
from typing import TypedDict, List

# === Load and Embed KB ===
loader = TextLoader("simpsons_kb.pl")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(documents)

embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)
retriever = vectorstore.as_retriever()

llm = ChatOpenAI(model="gpt-4", temperature=0)

# === Define State ===
class GraphState(TypedDict):
    query: str
    context: List[str]
    judgment: str

# === Node 1: RAG Retriever ===
def rag_retrieve(state: GraphState):
    query = state["query"]
    result = retriever.get_relevant_documents(query)
    contents = [doc.page_content for doc in result]
    return {"query": query, "context": contents}

# === Node 2: Judgment ===
def relevance_judger(state: GraphState):
    prompt = f"""You are given a natural language query and a list of text chunks retrieved from a knowledge base.
Your job is to judge whether the retrieved context is relevant to answering the query.

Query: {state['query']}

Retrieved Context:
{chr(10).join(state['context'])}

Answer only 'RELEVANT' or 'IRRELEVANT' with a brief reason."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"query": state["query"], "context": state["context"], "judgment": response.content.strip()}

# === LangGraph Setup ===
builder = StateGraph(GraphState)
builder.add_node("rag_retrieve", rag_retrieve)
builder.add_node("relevance_judger", relevance_judger)

builder.set_entry_point("rag_retrieve")
builder.add_edge("rag_retrieve", "relevance_judger")
builder.add_edge("relevance_judger", END)

graph = builder.compile()

# === Run ===
if __name__ == "__main__":
    user_query = "Who is Bart’s father?"
    final_state = graph.invoke({"query": user_query})

    print("\n🔹 Query:", final_state["query"])
    print("\n📚 Retrieved Context:")
    for c in final_state["context"]:
        print("-", c)
    print("\n🧠 Relevance Judgment:")
    print(final_state["judgment"])
