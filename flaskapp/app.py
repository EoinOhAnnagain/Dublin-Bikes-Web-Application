from flask import Flask, render_template
#from jinja2 import Template
#from sqlalchemy import create_engine
#import pandas as pd

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("map.html")
    
#@app.route("/contact")
#def contact():
#    d = {'name': 'Eoin'}
#    return render_template("contact.html", **d)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
