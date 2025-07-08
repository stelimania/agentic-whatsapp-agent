# Agentic WhatsApp Agent

An intelligent AI-powered WhatsApp agent that uses OpenAI's GPT models to generate contextual responses. The agent is designed with a configurable persona system and supports easy swapping between different LLM backends (OpenAI, Groq, Hugging Face).

## Features

- 🤖 **AI-Powered Responses**: Uses OpenAI GPT models to generate intelligent, contextual responses
- 🎭 **Configurable Persona**: Customize the agent's personality, style, and behavior via JSON configuration
- 🔄 **Swappable LLM Backends**: Easy switching between OpenAI, Groq, and Hugging Face models
- 💬 **WhatsApp Integration**: Send and receive messages via Twilio's WhatsApp API
- 📝 **Comprehensive Logging**: Detailed logging for monitoring and debugging
- 🛡️ **Error Handling**: Robust error handling with fallback responses

## Architecture

The agent is structured for easy extensibility:
- **LLM Backend Abstraction**: Abstract base class allows easy swapping of AI providers
- **Persona Configuration**: JSON-based configuration for agent behavior
- **Modular Design**: Clean separation of concerns for messaging, AI generation, and configuration

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/stelimania/agentic-whatsapp-agent.git
   cd agentic-whatsapp-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   export TWILIO_ACCOUNT_SID="your_twilio_account_sid"
   export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

4. **Configure the agent:**
   Edit `persona_config.json` to customize your agent's personality and settings.

5. **Run the agent:**
   ```bash
   python agentic-whatsapp-agent.py
   ```

## Configuration

### Persona Configuration (`persona_config.json`)

The agent's behavior is controlled by a JSON configuration file:

```json
{
  "persona": {
    "name": "WhatsApp Assistant",
    "description": "A helpful and friendly WhatsApp assistant",
    "system_prompt": "You are a helpful WhatsApp assistant...",
    "temperature": 0.7,
    "max_tokens": 150
  },
  "settings": {
    "llm_backend": "openai",
    "model": "gpt-3.5-turbo",
    "enable_logging": true,
    "log_level": "info"
  },
  "twilio": {
    "whatsapp_number": "whatsapp:+14155238886",
    "recipient_number": "whatsapp:+1234567890"
  }
}
```

### Configuration Options

- **persona.name**: Display name for the agent
- **persona.description**: Brief description of the agent's purpose
- **persona.system_prompt**: The system prompt that defines the agent's personality
- **persona.temperature**: Response randomness (0.0 = deterministic, 1.0 = creative)
- **persona.max_tokens**: Maximum response length
- **settings.llm_backend**: LLM provider ("openai", "groq", "huggingface")
- **settings.model**: Model name (e.g., "gpt-3.5-turbo", "gpt-4")
- **settings.enable_logging**: Enable/disable logging
- **settings.log_level**: Logging level ("debug", "info", "warning", "error")

## LLM Backend Support

### OpenAI (Ready to Use)
```json
{
  "settings": {
    "llm_backend": "openai",
    "model": "gpt-3.5-turbo"
  }
}
```

### Groq (Coming Soon)
```json
{
  "settings": {
    "llm_backend": "groq",
    "model": "llama3-8b-8192"
  }
}
```

### Hugging Face (Coming Soon)
```json
{
  "settings": {
    "llm_backend": "huggingface",
    "model": "microsoft/DialoGPT-medium"
  }
}
```

## Usage Examples

### Basic Response Generation
```python
from agentic_whatsapp_agent import generate_ai_response

response = generate_ai_response("Hello, how are you?")
print(response)
```

### Handling Incoming Messages
```python
from agentic_whatsapp_agent import handle_incoming_message

# Process an incoming WhatsApp message
handle_incoming_message("What's the weather like today?", "whatsapp:+1234567890")
```

### Custom Persona
```python
# Modify persona_config.json to change the agent's personality
{
  "persona": {
    "system_prompt": "You are a professional business assistant. Be formal and concise.",
    "temperature": 0.3,
    "max_tokens": 100
  }
}
```

## WhatsApp Integration

To receive incoming messages, you'll need to set up a webhook endpoint:

1. **Create a webhook server** (Flask/FastAPI example):
```python
from flask import Flask, request
from agentic_whatsapp_agent import handle_incoming_message

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '')
    from_number = request.values.get('From', '')
    
    handle_incoming_message(incoming_msg, from_number)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
```

2. **Configure Twilio webhook**: Set your webhook URL in Twilio Console

## Development

### Adding New LLM Backends

1. Create a new class inheriting from `LLMBackend`:
```python
class NewBackend(LLMBackend):
    def generate_response(self, message: str, system_prompt: str = None) -> str:
        # Implement your LLM API call here
        return "Generated response"
```

2. Update the `get_llm_backend()` function to include your new backend.

3. Add the new backend to your configuration.

### Testing

Run the demo conversation to test your configuration:
```bash
python agentic-whatsapp-agent.py
```

The agent will run a sample conversation showing how it responds to different messages.

## Environment Variables

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `OPENAI_API_KEY`: Your OpenAI API Key
- `GROQ_API_KEY`: Your Groq API Key (when using Groq backend)
- `HUGGINGFACE_API_KEY`: Your Hugging Face API Key (when using HF backend)

## Troubleshooting

### Common Issues

1. **"Configuration file not found"**: Ensure `persona_config.json` is in the same directory as the script.

2. **"OpenAI API error"**: Check your API key and ensure you have sufficient credits.

3. **"Twilio authentication failed"**: Verify your Twilio credentials and WhatsApp number configuration.

4. **"Failed to send WhatsApp message"**: Ensure your Twilio WhatsApp number is approved for the recipient.

### Debugging

Enable debug logging in your configuration:
```json
{
  "settings": {
    "log_level": "debug"
  }
}
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Roadmap

- [ ] Complete Groq backend implementation
- [ ] Complete Hugging Face backend implementation
- [ ] Add support for image messages
- [ ] Implement conversation memory
- [ ] Add rate limiting
- [ ] Create web dashboard for configuration
- [ ] Add multi-language support