import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
ollama_api_key = os.getenv("OLLAMA_API_KEY")


def query_ollama(question, context):
    url = ollama_api_key
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1",  # Change the model name if different
        "prompt": f"Context: {context}\nQuestion: {question}\nAnswer:",
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json().get("response", "")
