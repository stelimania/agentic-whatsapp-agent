import os
import json
from flask import Flask, request
import openai

# Load persona from config
with open('persona_config.json', 'r') as f:
    config = json.load(f)

PERSONA = config.get("persona", "You are a kind and helpful assistant.")
GREETING = config.get("greeting", "Hello!")
LANGUAGE = config.get("language", "en")

# Set your OpenAI API key in an environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_message, persona=PERSONA, backend="openai"):
    """
    Generates a chat response using an LLM backend.
    Swap 'backend' param to change providers (e.g., 'groq', 'huggingface').
    """
    if backend == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": user_message}
            ]
        )
        return response["choices"][0]["message"]["content"]
    # Extend here for other backends
    else:
        return "Sorry, no chat backend configured."

# Flask app for WhatsApp webhook
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return {"reply": "No message received."}

    # Initial greeting (optional)
    if user_message.lower() in ["hi", "hello", "hey"]:
        return {"reply": GREETING}
    
    # Generate response using persona and chat backend
    reply = generate_response(user_message)
    return {"reply": reply}

if __name__ == '__main__':
    app.run(port=5000)
