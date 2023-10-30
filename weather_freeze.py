import requests
from datetime import datetime, timedelta, timezone
import json
from settings import weather_key, lon, lat



def main(): 
    """lets see if it will freeze in the next four days"""
    
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_key}&units=imperial'
    resp = requests.get(url)
    data = resp.json()
    data = data.get('list')
    no_freeze = True
    for item in data:
        dt = datetime.fromtimestamp(item.get('dt'))
        temp = item.get('main').get('temp')
        if temp <= 32:
            no_freeze = False
            print(f'{dt} {temp}')
    if no_freeze:  
        print('no freeze')



if __name__ == '__main__':
    main()