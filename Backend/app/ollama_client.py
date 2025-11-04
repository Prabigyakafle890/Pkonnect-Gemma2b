import requests
import json

def ollama_chat(user_message, model="gemma:2b"):
    """
    Sends a prompt to the Ollama API and returns the model's full response.
    Handles streaming NDJSON from Ollama and combines all response chunks.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": user_message,
        "stream": True  # Ensures streaming (NDJSON) response
    }
    try:
        with requests.post(url, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()
            result = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        # Append the streamed chunk of the response, if present
                        result += data.get("response", "")
                    except Exception as e:
                        print("Ollama partial parse error:", e)
            return result if result else "No response from Ollama."
    except requests.exceptions.RequestException as e:
        return f"Ollama API error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"