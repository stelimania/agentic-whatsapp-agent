import os
import requests
from twilio.rest import Client
import schedule
import time

# Twilio credentials (best to set as environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_AUTH')
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio sandbox number
RECIPIENT_NUMBER = 'whatsapp:+1234567890'         # Your WhatsApp number

# Weather API credentials and settings
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_KEY')
CITY = 'London'
TEMP_THRESHOLD_C = 30  # Celsius

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_weather(city):
    url = (
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
    )
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        print(f"Weather API error: {data}")
        return None, None
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    return temp, desc

def send_whatsapp_message(body):
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=body,
        to=RECIPIENT_NUMBER
    )
    print(f"Sent message: {message.body} (SID: {message.sid})")

def agentic_check_and_remind():
    temp, desc = get_weather(CITY)
    if temp is None:
        return
    print(f"Current temperature in {CITY}: {temp}°C ({desc})")
    if temp >= TEMP_THRESHOLD_C:
        send_whatsapp_message(
            f"It's {temp}°C and {desc} in {CITY}. Stay hydrated! 💧"
        )
    else:
        print("No need to send a hydration reminder.")

# Schedule: every hour
schedule.every(1).hours.do(agentic_check_and_remind)

if __name__ == "__main__":
    print("Agent started. Checking weather and sending WhatsApp reminders if needed...")
    agentic_check_and_remind()  # Run once at start
    while True:
        schedule.run_pending()
        time.sleep(1)
