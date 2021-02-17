import requests
import json

NAME="Dublin"
STATIONS="https://api.jcdecaux.com/vls/v1/stations"
APIKEY = "9514a54c5679aff7255ccc24632f77b9f319a7f8"

r= requests.get(STATIONS, params ={"apiKey": APIKEY, "contract": NAME})
print(r.text)

with open('data.txt',"w") as json_file:
    data = json.load(r)
    for p in data['people']:
        print('Name: ' + p['name'])
        print('Website: ' + p['website'])
        print('From: ' + p['from'])
        print('')