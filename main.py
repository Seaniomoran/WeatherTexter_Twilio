import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_ENDPOINT = f"https://api.openweathermap.org/data/2.5/onecall"
ACCOUNT_SID = os.getenv("WEATHER_ACCOUNT")
API_KEY = os.getenv("WEATHER_KEY")
AUTH_TOKEN = os.getenv("WEATHER_TOKEN")
MY_PHONE_NUM = f"+1{os.getenv('MY_PHONE_NUM')}"
TWILIO_PHONE_NUM = os.getenv("TWILIO_PHONE_NUM")

owm_params = {
    "lat": 40.765690,
    "lon": -73.642357,
    "exclude": "current,minutely,daily",
    "appid": API_KEY,
}

response = requests.get(OWM_ENDPOINT, params=owm_params)
response.raise_for_status()
weather_data = response.json()

weather_id = [weather_data["hourly"][x]["weather"][0]["id"] for x in range(12) if x > 700]
if len(weather_id) > 0:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=proxy_client)
    message = client.messages \
        .create(body="It's going to rain today. Remember to bring an umbrella! ☂️🌂",
                from_=f'{TWILIO_PHONE_NUM}',
                to=f'{MY_PHONE_NUM}')
    print(message.status)
