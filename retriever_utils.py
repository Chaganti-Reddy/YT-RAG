# retriever_utils.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings

def split_text(transcript: str, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.create_documents([transcript])

def build_vector_store(chunks, model_choice, api_key=None):
    if model_choice == "OpenAI (GPT)":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
    elif model_choice == "Gemini (Google)":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    elif model_choice == "Ollama (Local)":
        embeddings = OllamaEmbeddings(model="llama3")
    else:
        raise ValueError("Unsupported model for embeddings")

    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def get_retriever_from_transcript(transcript_text: str, model_choice: str, api_key: str = None):
    chunks = split_text(transcript_text)
    vector_store = build_vector_store(chunks, model_choice, api_key)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    return retriever, vector_store

