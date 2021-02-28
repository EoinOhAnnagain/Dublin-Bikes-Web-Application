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
    print(3.1)
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
    print(3)
    values = list(map(get_weather, request_result.json()))
    print(4)
    ins = weather.insert().values(values)
    print(5)
    engine.execute(ins)
    print(6)
    return

#Connecting to databse


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
    Column('post_time', DateTime)
)

weather.create(engine, checkfirst=True)




#Inserting data into the weather table





def main():

    # infinite loop to enable continuous data collection
    while True:
        try:
            print(1)
            # #sending get request to specified URL
            r = requests.get(f"{RESOURCEURL}{LOCATION}?apikey={APIKEYw}")
            print(2)
            store(r)
            print(7)

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


        except:
            print('error')
    return


if __name__ == '__main__':
    main()
