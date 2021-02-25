##This file exists to inport the variables, such as your API ID, into the Dublin Bikes scraper.
##Please do not alter this version. It exists so everyone can copy their own variables into a copy of their own.

from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine

#USER = admin name
#PASSWORD = password
#URL = database url
#PORT = port
#DB = Database name


engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URL, PORT, DB), echo=True)


APIKEY = ""
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
