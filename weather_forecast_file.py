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
    # cache = {
    #     '2023-11-07': {
    #         'min': 40.1,
    #         'max': 50.5
    #     },
    #     '2023-11-08': {
    #         'min': 40.1,
    #         'max': 50.5
    #     }
    # }
    cache = {}
    for item in data:
        # print(json.dumps(item))
        temp_min = item['main']['temp_min']
        temp_max = item['main']['temp_max']
        date_time = item['dt_txt']
        date = date_time.split(' ')[0]
        if cache.get(date):
            current_min = cache[date]['min']
            current_max = cache[date]['max']
        else:
            current_min = 999999
            current_max = -99999
        cache[date] = {
            'min': min(temp_min, current_min),
            'max': max(temp_max, current_max)
        }
    print(json.dumps(cache))
      



    #     dt = datetime.fromtimestamp(item.get('dt'))
    #     temp = item.get('main').get('temp')
    #     if temp <= 32:
    #         no_freeze = False
    #         print(f'{dt} {temp}')
    # if no_freeze:  
    #     print('no freeze')



if __name__ == '__main__':
    main()