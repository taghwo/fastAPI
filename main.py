from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel


from Model import City, city_Pydantic, cityIn_Pydantic

from tortoise.contrib.fastapi import register_tortoise
import requests


app = FastAPI()



@app.get('/')
def read_root():
    return {"hello":"world"}

@app.get('/cities')
async def get_cities():
    return await city_Pydantic.from_queryset(City.all())

@app.post('/cities')
async def create_city(city: cityIn_Pydantic):
     city_obj = await City.create(**city.dict(exclude_unset=True))
     return await city_Pydantic.from_tortoise_orm(city_obj)


@app.get("/cities/{id}")
async def get_city(id: int):
    return await city_Pydantic.from_queryset_single(City.get(id=id))


@app.delete('/cities/{city_id}')
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
    return 'deleted'

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
