"""
1. Creates a table in RDS DB using mysqlalchemy
2. Send a request to accuweather API to retrieve hourly forecast information
3. Stores parsed information in DB

Information retrieval occurs periodically every hour.
"""


from sqlalchemy import Table, Column, Integer, Float, String,Boolean, MetaData, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
from IPython.display import JSON
import time


def get_weather(obj):
    """
    Takes the API JSON object retrieved from the API weather request and returns a python dictionary to facilitate
    further commands and manipulations.

    :param obj: API JSON object
    :return: dictionary mapping each JSON object to relevant key header
    """
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

#Inserting data into the weather table

# def store (request_result):
#     values = list(map(get_weather, request_result.json()))
#     ins = weather.insert().values(values)
#     engine.execute(ins)
#     return



def main():

    # infinite loop to enable continuous data collection
    while True:
        try:
            #sending get request to specified URL
            r = requests.get(f"{RESOURCEURL}{LOCATION}?apikey={APIKEY}")
            print(r.json())

            #storing the values from returned json to a list
            values = list(map(get_weather, r.json()))

            #creating insert command for sqlalchemy engine
            ins = weather.insert().values(values)

            #executing insert command
            engine.execute(ins)

            #repeat every hour
            time.sleep(60 * 60)


        except:
            print('error')
    return


if __name__ == '__main__':
    main()
