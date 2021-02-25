# Importing packages
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
from IPython.display import JSON
import time

# Import API details and database connection from APID.
# Make sure APID has your details or it will fail.
from APID import *

# Creating table
meta = MetaData()

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
    Column('last_update', DateTime),
    Column('post_time', DateTime)
)
availability.create(engine, checkfirst=True)

# Connecting to JCDecaux API
from APID import *

r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})


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
                        'last_update': datetime.datetime.fromtimestamp(int(anti_none(obj['last_update']) / 1e3)),
                        'post_time': datetime.datetime.now()
                        }

            # This Function just sets the value to 0 if it is None. This prevents crashes if there is an issue with the API.
            def anti_none(result):
                if result is None:
                    result = 0
                return result

            values = list(map(get_availability, r.json()))
            ins = availability.insert().values(values)
            engine.execute(ins)

            time.sleep(5 * 60)

        except:
            print('error')
    return


if __name__ == '__main__':
    main()


