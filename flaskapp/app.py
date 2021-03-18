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
#@functools.memoise()
def map():
    df = pd.read_sql_table("stations", engine)
    results = engine.execute("select * from stations")
    print([res for res in results])
    #print(df.head(3).to_json(orient="records"))
    return df.head(3).to_json(orient="records")

@app.route("/stations")
def stations():
    df = pd.read_sql_query("SELECT * FROM availability ORDER BY post_time DESC LIMIT 109", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    return df.to_json(orient='records')

   
#@app.route("/contact")
#def contact():
#    d = {'name': 'Eoin'}
#    return render_template("contact.html", **d)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
