##This file exists to inport the variables, such as your API ID, into the Dublin Bikes scraper.
##Please do not alter this version. It exists so everyone can copy their own variables into a copy of their own.

from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine

USER = "admin"
PASSWORD = "dublinbikes"
URI = "dublinbikes.ciwb2rbkjl8e.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dublinbikes"

engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

APIKEY = "541e273750ef405656887b8db71e95bcd8652a47"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"


ACCUAPIKEY = "nMc7AXHaW5AJMglz5tWLMMYZImwBGMMi"
ACCULOCATIONKEY = "207931"
RESOURCEURL = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"