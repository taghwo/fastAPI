from tortoise.models import Model
import requests
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
class City(Model):
    name = fields.CharField(50, blank=False, unique=True)
    timezone = fields.CharField(50, blank=False)
    
    def current_time(self) -> str:
          r = requests.get(f'http://worldtimeapi.org/api/timezone/{self.timezone}')

          time = r.json()['datetime']

          return time

    class PydanticMeta:
        computed = ("current_time",)


city_Pydantic = pydantic_model_creator(City, name='city')
cityIn_Pydantic = pydantic_model_creator(City, name='cityIn', exclude_readonly=True)
