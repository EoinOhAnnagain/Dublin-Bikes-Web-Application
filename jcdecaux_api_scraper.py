#Importing packages

from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
from IPython.display import JSON
import time

#Connecting to databse

engine = create_engine("mysql+mysqlconnector://admin:dublinbikes@dublinbikes.ciwb2rbkjl8e.us-east-1.rds.amazonaws.com:3306/dublinbikes", echo=True)

#Creating tables

meta = MetaData()

stations = Table(
    'stations', meta,
    Column('number', Integer, primary_key = True),
    Column('contract_name', String(128)),
    Column('name', String(128)),
    Column('address', String(128)),
    Column('pos_lat', Float),
    Column('pos_lng', Float),
    Column('banking', Integer),
    Column('bonus', Integer),
    Column('bike_stands', Integer),
    Column('available_bike_stands', Integer),
    Column('available_bikes', Integer),
    Column('status', String(128)),
    Column('last_update', DateTime)
)

availability = Table(
    'availability', meta,
    Column('number', Integer),
    Column('contract_name', String(128)),
    Column('name', String(128)),
    Column('address', String(128)),
    Column('pos_lat', Float),
    Column('pos_lng', Float),
    Column('banking', Integer),
    Column('bonus', Integer),
    Column('bike_stands', Integer),
    Column('available_bike_stands', Integer),
    Column('available_bikes', Integer),
    Column('status', String(128)),
    Column('last_update', DateTime)
)
try:
    stations.drop(engine)
    availability.drop(engine)
except:
    pass
meta.create_all(engine)


#Connecting to JCDecaux API

APIKEY = "541e273750ef405656887b8db71e95bcd8652a47"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})


#Inserting data into the stations table

def get_station(obj):
    return {'number': obj['number'],
            'contract_name': obj['contract_name'],
           'name': obj['name'],
            'address': obj['address'],
            'pos_lng': obj['position']['lng'],
            'pos_lat': obj['position']['lat'],
            'banking': obj['banking'],
            'bonus': obj['bonus'],
            'bike_stands': obj['bike_stands'],
            'available_bike_stands': obj['available_bike_stands'],
            'available_bikes': obj['available_bikes'],
            'status': obj['status'],
            'last_update': datetime.datetime.fromtimestamp( int(obj['last_update'] / 1e3) )
           }

values = list(map(get_station, r.json()))
#print(values)
ins = stations.insert().values(values)
engine.execute(ins)


# Inserting data into the availability table every 5 minutes

def main():
    while True:
        try:
            r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})

            def get_availability(obj):
                return {'number': obj['number'],
                        'contract_name': obj['contract_name'],
                        'name': obj['name'],
                        'address': obj['address'],
                        'pos_lng': obj['position']['lng'],
                        'pos_lat': obj['position']['lat'],
                        'banking': obj['banking'],
                        'bonus': obj['bonus'],
                        'bike_stands': obj['bike_stands'],
                        'available_bike_stands': obj['available_bike_stands'],
                        'available_bikes': obj['available_bikes'],
                        'status': obj['status'],
                        'last_update': datetime.datetime.fromtimestamp(int(obj['last_update'] / 1e3))
                        }

            values = list(map(get_availability, r.json()))
            ins = availability.insert().values(values)
            engine.execute(ins)

            time.sleep(5 * 60)

        except:
            print('error')
    return


if __name__ == '__main__':
    main()