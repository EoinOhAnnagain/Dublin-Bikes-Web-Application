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
from APID import *


def get_weather(obj):
    """
    Takes the API JSON object retrieved from the API weather request and returns a python dictionary to facilitate
    further commands and manipulations.
    :param obj: API JSON object
    :return: dictionary mapping each JSON object to relevant key header
    """
    return {'DateTime': obj['Dailyforecasts']['Date'],
            #'EpochDateTime': obj['DailyForecasts']['EpochDate'],
            #'WeatherIcon': obj['DailyForecasts']['Day']['Icon'],
            #'IconPhrase': obj['DailyForecasts']['Day']['IconPhrase'],
            #'HasPrecipitation': obj['DailyForecasts']['Day']['HasPrecipitation'],
            #'MinTemperature': obj['DailyForecasts']['Temperature']['Minimum']['Value'],
            #'MaxTemperature': obj['DailyForecasts']['Temperature']['Maximum']['Value'],
            #'PrecipitationProbability': obj['DailyForecasts']['Day']['PrecipitationProbability'],
            #'MinRealFeelTemperature': obj['DailyForecasts']['RealFeelTemperature']['Minimum']['Value'],
            #'MaxRealFeelTemperature': obj['DailyForecasts']['RealFeelTemperature']['Maximum']['Value'],
            #'WindSpeed': obj['DailyForecasts']['Day']['Wind']['Speed']['Value'],
            #'Rain': obj['DailyForecasts']['Day']['Rain']['Value'],
            #'CloudCover': obj['DailyForecasts']['Day']['CloudCover'],
            'post_time': datetime.datetime.now()
           }



def store (request_result):
    """
    1. Maps the JSON object to returned from Accuweather API to a list
    2. Creates an insertion instruction to be passed to the engine execute method
    3. Runs execution method of the engine on the insertion instruction
    :param request_result: JSON request result pulled from accuweather API
    :return: None, as function simple executes the insert instruction to the RDS
    """
    values = list(map(get_weather, request_result.json()))
    ins = weather_forecast.insert().values(values)
    engine.execute(ins)
    return


#Creating table

meta = MetaData()

weather_forecast = Table(
    'weather_forecast', meta,
    Column('DateTime', String(128)),
   # Column('EpochDateTime', Integer),
   # Column('WeatherIcon', Integer),
   # Column('IconPhrase', String(128)),
   # Column('HasPrecipitation', Boolean),
   # Column('MinTemperature', Float),
   # Column('MaxTemperature', Float),
   # Column('PrecipitationProbability', Integer),
   # Column('MinRealFeelTemperature', Float),
   # Column('MaxRealFeelTemperature', Float),
   # Column('WindSpeed', Float),
   # Column('Rain', Float),
   # Column('CloudCover', Integer),
    Column('post_time', DateTime)
)

weather_forecast.create(engine, checkfirst=True)




#Inserting data into the weather table





def main():

    # infinite loop to enable continuous data collection
    while True:
        #try:
            # #sending get request to specified URL
            r = requests.get(f"{RESOURCEURLFORECAST}{ACCULOCATIONKEY}?apikey={ACCUAPIKEYFORECAST}&details=true&metric=true")
            store(r)

            #keeping non functionalized code in case of error as I am sure it works
            # print(r.json())
            #
            # #storing the values from returned json to a list
            # values = list(map(get_weather, r.json()))
            #
            # #creating insert command for sqlalchemy engine
            # ins = weather.insert().values(values)
            #
            # #executing insert command
            # engine.execute(ins)


            #repeat every hour
            time.sleep(60 * 60)


        #except:
            #print('error')
    return


if __name__ == '__main__':
    main()
