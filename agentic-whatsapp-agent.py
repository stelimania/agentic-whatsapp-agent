import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from twilio.rest import Client
from openai import OpenAI

# Load persona configuration
def load_persona_config(config_path: str = "persona_config.json") -> Dict[str, Any]:
    """
    Load persona configuration from JSON file.
    
    Args:
        config_path: Path to the persona configuration file
        
    Returns:
        Dictionary containing persona configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file '{config_path}': {e}")
        raise

# Load configuration
config = load_persona_config()

# Setup logging
logging.basicConfig(
    level=getattr(logging, config['settings']['log_level'].upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Twilio credentials (best to set as environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_AUTH')
TWILIO_WHATSAPP_NUMBER = config['twilio']['whatsapp_number']
RECIPIENT_NUMBER = config['twilio']['recipient_number']

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')

# Initialize clients
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class LLMBackend(ABC):
    """
    Abstract base class for LLM backends.
    This allows easy swapping between different LLM providers (OpenAI, Groq, Hugging Face, etc.).
    """
    
    @abstractmethod
    def generate_response(self, message: str, system_prompt: str = None) -> str:
        """
        Generate a response using the LLM backend.
        
        Args:
            message: User input message
            system_prompt: System prompt to set the persona/context
            
        Returns:
            Generated response string
        """
        pass


class OpenAIBackend(LLMBackend):
    """
    OpenAI GPT backend implementation.
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 150):
        """
        Initialize OpenAI backend.
        
        Args:
            model: OpenAI model name (e.g., "gpt-3.5-turbo", "gpt-4")
            temperature: Response randomness (0.0 to 1.0)
            max_tokens: Maximum response length
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def generate_response(self, message: str, system_prompt: str = None) -> str:
        """
        Generate response using OpenAI GPT API.
        
        Args:
            message: User input message
            system_prompt: System prompt to set the persona/context
            
        Returns:
            Generated response string
        """
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API using new client format
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return config['settings']['fallback_response']


class GroqBackend(LLMBackend):
    """
    Groq backend implementation (placeholder for future implementation).
    To use Groq, install the groq package and implement the API calls.
    """
    
    def __init__(self, model: str = "llama3-8b-8192", temperature: float = 0.7, max_tokens: int = 150):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        # TODO: Initialize Groq client
        
    def generate_response(self, message: str, system_prompt: str = None) -> str:
        """
        Generate response using Groq API.
        
        Note: This is a placeholder. Implement actual Groq API calls here.
        """
        # TODO: Implement Groq API integration
        return "Groq backend not yet implemented. Please use OpenAI backend."


class HuggingFaceBackend(LLMBackend):
    """
    Hugging Face backend implementation (placeholder for future implementation).
    To use Hugging Face, install the transformers package and implement the model calls.
    """
    
    def __init__(self, model: str = "microsoft/DialoGPT-medium", temperature: float = 0.7, max_tokens: int = 150):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        # TODO: Initialize Hugging Face model
        
    def generate_response(self, message: str, system_prompt: str = None) -> str:
        """
        Generate response using Hugging Face model.
        
        Note: This is a placeholder. Implement actual Hugging Face model calls here.
        """
        # TODO: Implement Hugging Face model integration
        return "Hugging Face backend not yet implemented. Please use OpenAI backend."


def get_llm_backend() -> LLMBackend:
    """
    Factory function to create and return the appropriate LLM backend based on configuration.
    
    Returns:
        LLMBackend instance
    """
    backend_type = config['settings']['llm_backend'].lower()
    model = config['settings']['model']
    temperature = config['persona']['temperature']
    max_tokens = config['persona']['max_tokens']
    
    if backend_type == "openai":
        return OpenAIBackend(model=model, temperature=temperature, max_tokens=max_tokens)
    elif backend_type == "groq":
        return GroqBackend(model=model, temperature=temperature, max_tokens=max_tokens)
    elif backend_type == "huggingface":
        return HuggingFaceBackend(model=model, temperature=temperature, max_tokens=max_tokens)
    else:
        logger.warning(f"Unknown backend type: {backend_type}. Defaulting to OpenAI.")
        return OpenAIBackend(model=model, temperature=temperature, max_tokens=max_tokens)


# Initialize LLM backend
llm_backend = get_llm_backend()

def send_whatsapp_message(body: str, to_number: str = None) -> bool:
    """
    Send a WhatsApp message using Twilio.
    
    Args:
        body: Message content to send
        to_number: Recipient number (optional, uses default from config)
        
    Returns:
        True if message sent successfully, False otherwise
    """
    try:
        recipient = to_number or RECIPIENT_NUMBER
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=recipient
        )
        
        if config['settings']['enable_logging']:
            logger.info(f"Sent message: {message.body[:50]}... (SID: {message.sid})")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
        return False


def generate_ai_response(user_message: str) -> str:
    """
    Generate an AI response to a user message using the configured LLM backend.
    
    Args:
        user_message: The user's input message
        
    Returns:
        AI-generated response string
    """
    try:
        system_prompt = config['persona']['system_prompt']
        response = llm_backend.generate_response(user_message, system_prompt)
        
        if config['settings']['enable_logging']:
            logger.info(f"Generated response for message: '{user_message[:30]}...'")
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to generate AI response: {e}")
        return config['settings']['fallback_response']


def handle_incoming_message(user_message: str, from_number: str = None) -> None:
    """
    Handle an incoming WhatsApp message by generating an AI response and sending it back.
    
    Args:
        user_message: The received message content
        from_number: Sender's number (optional, uses default recipient)
    """
    logger.info(f"Received message: '{user_message[:50]}...'")
    
    # Generate AI response
    ai_response = generate_ai_response(user_message)
    
    # Send response back
    success = send_whatsapp_message(ai_response, from_number)
    
    if success:
        logger.info("Response sent successfully")
    else:
        logger.error("Failed to send response")


def demo_conversation():
    """
    Demonstrate the AI chat functionality with a sample conversation.
    This is useful for testing the persona and LLM integration.
    """
    print(f"\n🤖 {config['persona']['name']} Demo Conversation")
    print("=" * 50)
    
    sample_messages = [
        "Hello! How are you?",
        "What can you help me with?",
        "Tell me a joke",
        "What's the weather like?",
        "Thank you for your help!"
    ]
    
    for message in sample_messages:
        print(f"\n👤 User: {message}")
        response = generate_ai_response(message)
        print(f"🤖 Assistant: {response}")
        
        # Simulate sending via WhatsApp (comment out to avoid actual sending)
        # send_whatsapp_message(response)
    
    print("\n" + "=" * 50)
    print("Demo completed! The assistant is ready to use.")
    print("To send actual WhatsApp messages, configure your Twilio credentials and call handle_incoming_message().")

if __name__ == "__main__":
    print(f"🚀 Starting {config['persona']['name']}...")
    print(f"📝 Persona: {config['persona']['description']}")
    print(f"🧠 LLM Backend: {config['settings']['llm_backend']} ({config['settings']['model']})")
    print(f"💬 WhatsApp Number: {TWILIO_WHATSAPP_NUMBER}")
    print("-" * 60)
    
    # Run demo conversation to test the AI functionality
    demo_conversation()
    
    # In a real-world scenario, you would:
    # 1. Set up a webhook to receive incoming WhatsApp messages
    # 2. Parse the incoming message and sender information
    # 3. Call handle_incoming_message() with the received content
    #
    # For now, you can manually test by calling:
    # handle_incoming_message("Your test message here")
    
    print("\n✅ Agent is ready! To integrate with WhatsApp webhooks:")
    print("1. Set up a webhook endpoint (e.g., using Flask/FastAPI)")
    print("2. Configure Twilio to send webhooks to your endpoint")
    print("3. Call handle_incoming_message() when messages are received")
    print("4. See README.md for detailed setup instructions")
