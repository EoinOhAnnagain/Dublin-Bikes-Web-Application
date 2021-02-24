#Importing packages

from sqlalchemy import Table, Column, Integer, Float, String,Boolean, MetaData, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
from IPython.display import JSON
import time

#Connecting to databse

engine = create_engine("mysql+mysqlconnector://admin:admin1234@dbikes.ccecuvqpo8jx.us-east-1.rds.amazonaws.com:3306/dbikes", echo=True)

#Creating table

meta = MetaData()

weather = Table(
    'weather', meta,
    Column('DateTime', String(128), primary_key = True),
    Column('EpochDateTime', String(128)),
    Column('WeatherIcon', String(128)),
    Column('IconPhrase', String(128)),
    Column('HasPrecipitation', Boolean),
    Column('IsDaylight', Boolean),
    Column('Temperature', Float),
    Column('PrecipitationProbability', Float),
    Column('MobileLink', String(128)),
    Column('Link', String(128)),
)

try:
    weather.drop(engine)
except:
    pass


meta.create_all(engine)


#Connecting to Accuweather API

APIKEY = "v7sO8DZEJ6XOtWZmAhoG9Ikv2XQTmnro"
LOCATION = "207931"
RESOURCEURL = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"

#using line for testing currently
r = requests.get(f"{RESOURCEURL}{LOCATION}?apikey={APIKEY}")

#JSON is pulling correctly however mapping to database leads to keyerrors
print(r.json())



#Inserting data into the weather table

def get_weather(obj):
    return {'DateTime': obj['DateTime'],
            'EpochDateTime': obj['EpochDateTime'],
           'WeatherIcon': obj['WeatherIcon'],
            'IconPhrase': obj['IconPhrase'],
            'HasPrecipitation': obj['HasPrecipitation'],
            'IsDaylight': obj['IsDaylight'],
            'Temperature': obj['Temperature']['Value'],
            'PrecipitationProbability': obj['PrecipitationProbability'],
            'MobileLink': obj['MobileLink'],
            'Link': obj['Link']
           }

values = list(map(get_weather, r.json()))
ins = weather.insert().values(values)
engine.execute(ins)


# Inserting data into the availability table every 60 minutes

def main():
    while True:
        try:
            r = requests.get(RESOURCEURL, params={"apiKey": APIKEY, "location": LOCATION})

            values = list(map(get_weather, r.json()))
            ins = weather.insert().values(values)
            engine.execute(ins)

            time.sleep(60 * 60)

        except:
            print('error')
    return


if __name__ == '__main__':
    main()
