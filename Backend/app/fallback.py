from app.ollama_proxy import query_ollama

def fallback_with_phi(user_message: str) -> str:
    # Use the same gemma model as the main chatbot
    return query_ollama(user_message)
