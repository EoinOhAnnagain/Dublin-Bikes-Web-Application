from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, create_engine

engine = create_engine("mysql+mysqlconnector://admin:admin1234@dublinbikes.co2l5qvrgqx0.us-east-1.rds.amazonaws.com:3306/DublinBikes", echo=True)


APIKEY = "04292f59ce3536eb87c92523bbc4cfcb871b3c8f"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

ACCUAPIKEY = "KJboehsXfcHWN6ZfcHm5W8TKN3wlpCV8"
ACCULOCATIONKEY = "207931"
RESOURCEURL = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"




