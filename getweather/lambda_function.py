import json
import requests 
import os
from twilio.rest import Client

def lambda_handler(event, context):
    # TODO implement
    lat = os.environ.get('lat')
    lon = os.environ.get('lon')
    weather_key = os.environ.get('weather_key')
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_key}&units=imperial'
    resp = requests.get(url)
    data = resp.json()
    data = data.get('list')
    cache = {}
    for item in data:
        # print(json.dumps(item))
        snow = item.get('snow', {}).get('3h', 0.0)
        date_time = item['dt_txt']
        date = date_time.split(' ')[0]
        if cache.get(date):
            snow_sum = cache[date]['snow']
        else:
            snow_sum = 0.0
        cache[date] = {
            'snow': snow_sum + snow
        }
    snow_cache = {}
    for day in cache:
        if cache[day]['snow'] > 0:
            print(f"{day} = {cache[day]['snow']}")
            snow_cache[day] = cache[day]['snow']
    incident = {}
    if snow_cache:
        resp = send_pagerduty(snow_cache)
        incident = resp.json()
        t = send_twilio(snow_cache)
    return {
        'statusCode': 200,
        'body': incident
    }
    
def send_pagerduty(snow_cache):
    pagerduty_key = os.environ.get('pagerduty_key')
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'From': 'me@robertkoopman.com',
        'Authorization': f"Token token={pagerduty_key}"
    }
    body = {
        "incident": {
            "type": "incident",
            "title": "Snow in the forecast!",
            "service": {
                "id": "PT0VEZK",
                "type": "service_reference"
            },
            "body": {
                "type": "incident_body",
                "details": json.dumps(snow_cache)
            }
        }
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp
    

def send_twilio(snow_cache):
    account_sid = os.environ.get('twilio_account_sid')
    auth_token = os.environ.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+18886883216',
        body=json.dumps(snow_cache),
        to='+16026161315'
    )

    return message.sid