import os
from ollama import Client

# Initialize client pointing to Ollama Cloud
client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {os.environ.get('OLLAMA_API_KEY')}"},
)

# Run a cloud model with a valid messages list
response = client.chat(
    model="gemma4:31b:cloud", 
    messages=[
        {
            "role": "user",
            "content": "Write a python function to check if a number is prime."
        }
    ]
)

# Print the response from the model
print(response['message']['content'])