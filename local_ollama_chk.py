import json
import requests

# If your python script runs on the same Windows machine, use localhost:11434
# (Make sure you mapped port 11434 when running your Ollama container!)
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL_NAME = "gemma4:31b-cloud"

payload = {
    "model": MODEL_NAME,
    "prompt": "Reply with exactly the words: 'Local Ollama Cloud connection is working!'",
    "stream": False,
}

print(f"Connecting to local Ollama at: {OLLAMA_URL}...")
print(f"Requesting cloud model: {MODEL_NAME}...\n")

try:
    response = requests.post(
        OLLAMA_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=30
    )

    if response.status_code == 200:
        result = response.json()
        print("--- SUCCESS ---")
        print("Response from Gemma Cloud:")
        print(result.get("response"))
    else:
        print(f"--- FAILED (Status Code: {response.status_code}) ---")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("--- CONNECTION ERROR ---")
    print("Could not reach your local Ollama container.")
    print("1. Is the container currently running?")
    print("2. Did you expose the port (e.g., -p 11434:11434) when starting it?")
except Exception as e:
    print(f"An unexpected error occurred: {e}")