from fastapi import FastAPI 
from pydantic import BaseModel

import requests

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str

@app.get('/')
async def index():
    return {'key' : 'value'}

@app.get('/cities')
def get_cities():
    #return db
    
    results = []
    for city in db:
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        #print(r.json)
        current_time = r.json()['datetime']
        results.append({'name' : city['name'], 'timezone': city['timezone'], 'current_time': current_time})
    return results
    

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    print(r,'  next')
    current_time = r.json()['datetime']
    print(current_time)
    return {'name' : city['name'], 'timezone': city['timezone'], 'current_time': current_time}

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    #print(city)
    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}

   