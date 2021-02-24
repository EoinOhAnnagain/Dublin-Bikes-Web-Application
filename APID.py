##This file exists to inport the variables, such as your API ID, into the Dublin Bikes scraper.
##Please do not alter this version. It exists so everyone can copy their own variables into a copy of their own.

from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine

#A = admin name
#B = password
#C = database url
#D = port
#E = Database name


engine = create_engine("mysql+mysqlconnector://A:B@C:D/E", echo=True)


APIKEY = ""
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
