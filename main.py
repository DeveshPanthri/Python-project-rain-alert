import requests
import os
# **************************twilio message *****************************
from twilio.rest import Client


api_key = os.environ.get("api_key")
account_sid = os.environ.get("account_sid")
# for security env setup
# export file name
# variable name=value // ex ->auth_token = e196dfa9db906c57f5a7ed915a8445c2
# env to cheack
# auth_token = 'e196dfa9db906c57f5a7ed915a8445c2'
auth_token = os.environ.get("auth_token")
# client = Client(account_sid, auth_token)

# **********************************************************************
parameter={
    "lat": 22.3193,   # Hong Kong (100% rain today)
    "lon": 114.1694,    
    "appid":api_key,
    "cnt":4 # it's called count tells us thr no entries we want
}

respone=requests.get(url="https://api.openweathermap.org/data/2.5/forecast",params=parameter)
# this api tell you every 3 hours update of weather for 5 days that gives us 40 entries
# this api give weather condition in id (for ex 804- cloudy)
respone.raise_for_status() # for error that 400 code
weather_data=respone.json()
# list=data['list'][0]['weather'][0]['id']
will_rain=False

for hour_data in weather_data['list']:
    condition_code=hour_data["weather"][0]["id"]  # 0 as we want 1st and it has only one value
    if condition_code<700:
        will_rain=True
        break

if will_rain:
    client=Client(account_sid,auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Baarish hogi bhai! Umbrella le liyo. ☔', # Use body instead of content_sid
        to='whatsapp:+919084080626'
    )
    print(f"Message Sent! SID: {message.sid}")


    """
    OPENWEATHERMAP API - WEATHER ID REFERENCE TABLE
    ------------------------------------------------
    Range | Category      | Examples / Description
    ------------------------------------------------
    2xx   | Thunderstorm  | 200 (Light rain), 232 (Heavy drizzle)
    3xx   | Drizzle       | 300 (Light intensity drizzle)
    5xx   | Rain          | 500 (Light rain), 502 (Heavy rain)
    6xx   | Snow          | 600 (Light snow), 615 (Rain & snow)
    7xx   | Atmosphere    | 701 (Mist), 741 (Fog), 781 (Tornado)
    800   | Clear         | 800 (Clear sky)
    80x   | Clouds        | 801 (Few clouds), 804 (Overcast)

    Logic: condition_code < 700 covers Storms, Drizzle, Rain, and Snow.
    """
