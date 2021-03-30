##This file exists to inport the variables, such as your API ID, into the Dublin Bikes scraper.
##Please do not alter this version. It exists so everyone can copy their own variables into a copy of their own.

from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine

A = "admin"
B = "admin1234"
C = "dbikes.ccecuvqpo8jx.us-east-1.rds.amazonaws.com"
D = "3306"
E = "dbikes"


engine = create_engine(f"mysql+mysqlconnector://{A}:{B}@{C}:{D}/{E}", echo=True)

APIKEY = "9514a54c5679aff7255ccc24632f77b9f319a7f8"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

ACCUAPIKEY = "KJboehsXfcHWN6ZfcHm5W8TKN3wlpCV8"
ACCULOCATIONKEY = "207931"
RESOURCEURL = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"