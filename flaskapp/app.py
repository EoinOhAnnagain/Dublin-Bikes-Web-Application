from flask import Flask, render_template
from jinja2 import Template
from sqlalchemy import create_engine
import pandas as pd
from APID import *


app = Flask(__name__)

@app.route("/home")
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/test")
def hi():
    return render_template("test.html")

@app.route("/about")
def about():
    return app.send_static_file("about.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/mapquery")
#@functools.memoise()
def mapquery():
    df = pd.read_sql_query("select * from stations", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    return df.to_json(orient="records")

@app.route("/stations")
def stations():
    return render_template("stations.html")

@app.route("/stationsquery")
def stationsquery():
    df = pd.read_sql_query("SELECT * FROM availability ORDER BY post_time DESC LIMIT 109", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    return df.to_json(orient='records')

@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    sql = f"""
        SELECT number, last_update, available_bike_stands, available_bikes FROM availability
        where number = {station_id}
    """
    df = pd.read_sql_query(sql, engine)
    df = df[(df['last_update'].dt.year != 1970)]
    res_df = df.set_index('last_update').resample('1d').mean()
    res_df['last_update'] = res_df.index
    return res_df.to_json(orient='records')


#@app.route("/contact")
#def contact():
#    d = {'name': 'Eoin'}
#    return render_template("contact.html", **d)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
