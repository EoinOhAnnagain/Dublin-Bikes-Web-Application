from flask import Flask, render_template
#from jinja2 import Template
#from sqlalchemy import create_engine
#import pandas as pd

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def hello():
    return render_template("stationsList.html")

<<<<<<< HEAD
@app.route("/about")
def about():
    return app.send_static_file("about.html")

@app.route("/contact")
def contact():
    d = {'name': 'Matthew'}
    return render_template("contact.html", **d)

@app.route("/stations")
#@functools.memoise()
def stations():
    engine = create_engine(f"mysql+mysqlconnector://admin:admin1234:dbikes.ccecuvqpo8jx.us-east-1.rds.amazonaws.com:3306/dbikes", echo=True)
    df = pd.read_sql_table("stations", engine)
    results = engine.execute("select * from stations")
    print([res for res in results])
    #print(df.head(3).to_json(orient="records"))
    return df.head(3).to_json(orient="records")

@app.route("/stationsList")
def stationsList():
    engine = create_engine("mysql+mysqlconnector://admin:dublinbikes@dublinbikes.ciwb2rbkjl8e.us-east-1.rds.amazonaws.com:3306/dublinbikes", echo=True)
    df = pd.read_sql_query("SELECT * FROM availability ORDER BY post_time DESC LIMIT 109", engine)
    #results = engine.execute("select * from stations")
    #print([res for res in results])
    return df.to_json(orient='records')


if __name__ == "__main__":
    """
    localhost:5000 to access the app!
    """
    #print(__name__)
    app.run(debug=True, port=5000)
=======
@app.route("/map")
def map():
    return render_template("map.html")
    
#@app.route("/contact")
#def contact():
#    d = {'name': 'Eoin'}
#    return render_template("contact.html", **d)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
>>>>>>> Eoin
