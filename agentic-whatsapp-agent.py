import os
import json
from flask import Flask, request
import openai
from twilio.rest import Client

# Load persona from config
with open('persona_config.json', 'r') as f:
    config = json.load(f)

PERSONA = config.get("persona", "You are a kind and helpful assistant.")
GREETING = config.get("greeting", "Hello!")
LANGUAGE = config.get("language", "en")

# Set your OpenAI API key in an environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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
    # Get the message from Twilio's webhook format
    user_message = request.form.get('Body', '')
    from_number = request.form.get('From', '')
    
    if not user_message:
        return "No message received", 400

    # Initial greeting (optional)
    if user_message.lower() in ["hi", "hello", "hey"]:
        reply = GREETING
    else:
        # Generate response using persona and chat backend
        reply = generate_response(user_message)
    
    # Send reply back via Twilio
    try:
        message = client.messages.create(
            body=reply,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=from_number
        )
        return f"Message sent: {message.sid}", 200
    except Exception as e:
        return f"Error sending message: {str(e)}", 500

if __name__ == '__main__':
    app.run(port=5000)
