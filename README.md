# Agentic WhatsApp Agent

This is an agentic AI Python script that sends context-aware WhatsApp messages using Twilio and weather data.

## Features

- Checks the weather at a set interval (default: every hour)
- If it’s hot, sends a WhatsApp hydration reminder
- Easily customizable

## Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/agentic-whatsapp-agent.git
   cd agentic-whatsapp-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install twilio requests schedule
   ```

3. **Set your credentials:**  
   Add these environment variables or edit the script with your details:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `OPENWEATHER_API_KEY`

4. **Edit `agentic_whatsapp_agent.py`:**
   - Set your city and WhatsApp numbers

5. **Run the script:**
   ```bash
   python agentic_whatsapp_agent.py
   ```

## License

MIT
