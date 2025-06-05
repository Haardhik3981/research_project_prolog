# rag_chain.py

import os
# Updated imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Load your KB file
loader = TextLoader("simpsons_kb.pl")
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(documents)

# Create vectorstore using OpenAI embeddings
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)

# Create retriever from vector store
retriever = vectorstore.as_retriever()

# Setup LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create RetrievalQA chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# === Sample Query ===
query = "Which females are Lisa’s parents?"
result = rag_chain.invoke(query)

print("🔹 Query:", query)
print("✅ Answer:", result["result"])
print("📚 Retrieved Context:")
for doc in result["source_documents"]:
    print(doc.page_content.strip())