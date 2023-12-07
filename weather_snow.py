import json
import requests 
import os

def lambda_handler(event, context):
    # TODO implement
    lat = os.environ.get('lat')
    lon = os.environ.get('lon')
    weather_key = os.environ.get('weather_key')
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_key}&units=imperial'
    resp = requests.get(url)
    data = resp.json()
    data = data.get('list')
    # cache = {
    #     '2023-11-07': {
    #         'snow': 5.5
    #     },
    #     '2023-11-08': {
    #        'snow': 5.4
    #     }
    # }
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
    return {
        'statusCode': 200,
        'body': cache
    }





if __name__ == '__main__':
    lambda_handler(1, 1)