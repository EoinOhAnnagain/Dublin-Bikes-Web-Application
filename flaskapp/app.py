from flask import Flask, render_template, request
from jinja2 import Template
from sqlalchemy import create_engine
import pandas as pd
from APID import *
from functools import lru_cache

from datetime import datetime
import pickle
import sklearn

app = Flask(__name__)






## Index Page

@app.route("/home")
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/bike_stand_query")
def bike_stand_query():
    dfe = pd.read_sql_query("SELECT name, available_bikes, available_bike_stands, status FROM availability ORDER BY post_time DESC LIMIT 109", engine)
    return dfe.to_json(orient='records')

@app.route("/home_weather_query")
def home_weather_query():
    dfw = pd.read_sql_query("SELECT WeatherIcon, IconPhrase, Rain, Temperature, RealFeelTemperature, CloudCover, PrecipitationProbability, RelativeHumidity, WindSpeed FROM weather ORDER BY post_time DESC LIMIT 1", engine)
    return dfw.to_json(orient='records')






## Maps Page

@app.route("/map")
def map_integrated():
    return render_template("map.html")

@app.route("/mapquery")
#@functools.memoise()
@lru_cache
def mapquery():
    print('calling stations')
    df = pd.read_sql_query("select * from stations", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    return df.to_json(orient="records")

@app.route("/occupancy/<int:station_id>")
@lru_cache # temporarily cache result
def get_occupancy(station_id):
    sql = f"""
        SELECT number, last_update, available_bike_stands, available_bikes, name FROM availability 
        where number = {station_id}
    """
    df = pd.read_sql_query(sql, engine)
    df = df[(df['last_update'].dt.year != 1970)]
    res_df = df.set_index('last_update').resample('1d').mean()
    res_df['name'] = df['name'][0]
    res_df['last_update'] = res_df.index
    res_df = res_df.tail(32)
    return res_df.to_json(orient='records')


@app.route("/prediction", methods=['POST'])
def prediction():

    #gettting the selected predicted values
    if request.method == "POST":
        #assigning to variables
        number = request.form['a']
        date = request.form['b']
        hour = request.form['c']

        #retreving predicted weather forecast for input date
        sql = f""" SELECT RealFeelTemperature, WindSpeed, HasPrecipitation, Rain, CloudCover FROM weatherForecast WHERE STR_TO_DATE(DateTime, '%Y-%d-%m') = "{date}";"""

        df = pd.read_sql_query(sql, engine)

        #adding selected values to datafame
        df['number'] = number
        df['day'] = request.form['b'].split("-")[2]
        df['hour'] = request.form['c']


        #reordering columns as per model
        df = df[['number', 'hour', 'day', 'RealFeelTemperature', 'WindSpeed', 'HasPrecipitation',
                 'Rain', 'CloudCover']]

        #loading in model and predicting aviability percentage
        mp = pickle.load(open('finalized_model.sav', 'rb'))
        result = mp.predict(df)

        #getting number of bike stands available for station number
        sql = f"""SELECT bike_stands FROM stations WHERE number = "{number}" ;"""
        df = pd.read_sql_query(sql, engine)
        bike_stands = df["bike_stands"][0]

        #returning the result and populating page
        return render_template("map.html", data = f"Bikes available: {int(result * bike_stands)} \n Stands available = {bike_stands- (int(result * bike_stands))}")







## Stations Page

@app.route("/stations")
def stations():
    return render_template("stations.html")

@app.route("/stationsquery")
def stationsquery():
    df = pd.read_sql_query("SELECT * FROM availability ORDER BY post_time DESC LIMIT 109", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    return df.to_json(orient='records')



    




if __name__ == "__main__":
    app.run(debug=True, port=5000)
    