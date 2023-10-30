import requests
from datetime import datetime, timedelta, timezone
import json
from settings import weather_key, lon, lat



def main(): 
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)
    time = int(yesterday.timestamp())
    """going to fetch the current weather for my area code"""
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_key}&units=imperial'
    resp = requests.get(url)
    print(json.dumps(resp.json()))


if __name__ == '__main__':
    main()