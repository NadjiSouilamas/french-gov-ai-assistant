import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA


load_dotenv("../.env")

DATA_PATH = os.path.join("..", "data")
INDEX_PATH = os.path.join(DATA_PATH, "faiss_index_langchain")

# Load embeddings & retriever
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})

# Set up Claude model
llm = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",  # or claude-3-opus / claude-3-haiku
    temperature=0.2,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Build RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)


def get_answer(question: str) -> str:
    result = qa_chain.invoke({"query": question})
    sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]

    return {"answer": result["result"], "sources": sources}

