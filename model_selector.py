# model_selector.py

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

def get_llm(model_choice: str, api_key: str = None):
    if model_choice == "OpenAI (GPT)":
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        return ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key, temperature=0.2)

    elif model_choice == "Gemini (Google)":
        if not api_key:
            raise ValueError("Gemini API key is required.")
        return "direct"  # Custom logic handled via gemini_direct.py

    elif model_choice == "Ollama (Local)":
        return ChatOllama(model="llama3")

    else:
        raise ValueError("Invalid model selected.")

