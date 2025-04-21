import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .loader import load_and_split_pdf
from .config import GOOGLE_API_KEY

# Directory to store the vector database
PERSIST_DIRECTORY = "chroma_db"

def load_and_split_markdown(file_path):
    """Load and split markdown file for embeddings"""
    loader = UnstructuredMarkdownLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    split_documents = text_splitter.split_documents(documents)
    print(f"Split markdown into {len(split_documents)} chunks")
    return split_documents

def initialize_chain():
    # LLM and embedding model setup
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Initialize Chroma vector store
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"}
    )

    # Check if Chroma DB is already populated
    if not os.path.exists(PERSIST_DIRECTORY) or not os.listdir(PERSIST_DIRECTORY):
        print("Vector store is empty. Creating new one...")

        # Load and split documents
        handbook_docs = load_and_split_pdf("Handbook_Travelling_Allowances_2023.pdf")
        faq_docs = load_and_split_markdown("pcda_FAQ.md")
        all_docs = handbook_docs + faq_docs

        # Add documents and persist
        vectorstore.add_documents(all_docs)
        print("Documents embedded and added to vector store.")
    else:
        print("Vector store found. Skipping re-embedding.")

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "score_threshold": 0.65}
    )

    return llm, retriever
