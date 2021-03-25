"""
1. Creates a table in RDS DB using mysqlalchemy
2. Send a request to accuweather API to retrieve hourly forecast information
3. Stores parsed information in DB
Information retrieval occurs periodically every hour.
"""


from sqlalchemy import Boolean
import requests
import datetime
import time
from Master.flaskapp.APID import *


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
            'RealFeelTemperature': obj['RealFeelTemperature']['Value'],
            'WindSpeed': obj['Wind']['Speed']['Value'],
            'RelativeHumidity': obj['RelativeHumidity'],
            'Rain': obj['Rain']['Value'],
            'CloudCover': obj['CloudCover'],
            'Link': obj['Link'],
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
    ins = weather.insert().values(values)
    engine.execute(ins)
    return


#Creating table

meta = MetaData()

weather = Table(
    'weather', meta,
    Column('DateTime', String(128)),
    Column('EpochDateTime', Integer),
    Column('WeatherIcon', Integer),
    Column('IconPhrase', String(128)),
    Column('HasPrecipitation', Boolean),
    Column('IsDaylight', Boolean),
    Column('Temperature', Float),
    Column('PrecipitationProbability', Float),
    Column('RealFeelTemperature', Float),
    Column('WindSpeed', Float),
    Column('RelativeHumidity', Integer),
    Column('Rain', Float),
    Column('CloudCover', Integer),
    Column('Link', String(128)),
    Column('post_time', DateTime)
)

#creatig engine
weather.create(engine, checkfirst=True)




#Inserting data into the weather table

def main():

    # infinite loop to enable continuous data collection
    while True:
        try:
            #sending get request to specified URL
            r = requests.get(f"{RESOURCEURL}{ACCULOCATIONKEY}?apikey={ACCUAPIKEY}&details=true&metric=true")
            store(r)


            #repeat every hour
            time.sleep(60 * 60)


        except:
            print('error')
    return


if __name__ == '__main__':
    main()

