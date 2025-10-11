from typing import List

import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

RAW_DIR = os.path.join("data", "raw")
INDEX_PATH = os.path.join("data", "faiss_index_langchain")


def load_documents() -> List:
    documents = []
    for file_name in os.listdir(RAW_DIR):
        loader = TextLoader(os.path.join(RAW_DIR, file_name), encoding="utf-8")
        documents.extend(loader.load())

    print(f"Loaded {len(documents)} documents.")
    return documents


from langchain_text_splitters import RecursiveCharacterTextSplitter

# TODO: Add type hint
def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap=100,
        length_function=len
    )

    split_docs = splitter.split_documents(docs)
    print(f"Created {len(split_docs)} chunks.")
    return split_docs


def embed_documents(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    vectorstore.save_local(INDEX_PATH)
    print(f"✅ FAISS index saved to {INDEX_PATH}")

def main():
    docs = load_documents()
    chunks = chunk_documents(docs)
    embed_documents(chunks)

if __name__ == "__main__":
    main()