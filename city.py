from fastapi import FastAPI, Path
from pydantic import BaseModel
import requests

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'FastAPI test is success'}

db = []

class City(BaseModel):
    name: str
    timezone: str
    
@app.get('/cities/')    
def get_cities():
    results = []
    for city in db:
        
        # Fetch current time from World Time API
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        current_time = r.json()['datetime']
        
        # Fetch weather information from Weatherstack API
        weather_response = get_weather(city['name'])

        results.append({'name':city['name'],'timezone':city['timezone'],'current_time':current_time,'weather': weather_response})
    return results


@app.get('/cities/{city_id}/')
def get_city(city_id: int):
    return db[city_id-1]

@app.post('/cities/')
def add_city(city:City):
    db.append(city.dict())
    return db[-1]

@app.delete('/cities/{city_id}/')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}

def get_weather(city_name: str):
    # Using Weatherstack API access key
    access_key = '427bafb22064e41779ba65285ee1e68b'
    url = f'http://api.weatherstack.com/current?access_key={access_key}&query={city_name}'
    response = requests.get(url)
    weather_data = response.json()
    
    # Extracting relevant weather information
    if 'current' in weather_data:
        return {
            'temperature': weather_data['current']['temperature'],
            'humidity': weather_data['current']['humidity'],
            'weather_condition': weather_data['current']['weather_descriptions'][0],
            'wind_speed': weather_data['current']['wind_speed'],
            'wind_direction': weather_data['current']['wind_dir'],
            'pressure': weather_data['current']['pressure'],
            'precipitation': weather_data['current']['precip'],
            'uv_index': weather_data['current']['uv_index'],
            'visibility': weather_data['current']['visibility'],
            'feels_like': weather_data['current']['feelslike']
        }
    else:
        return {'error': 'Weather information not available'}