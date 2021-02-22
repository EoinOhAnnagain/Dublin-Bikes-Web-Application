#JCDecaux API information
APIKEY = "541e273750ef405656887b8db71e95bcd8652a47"
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"


def main():
    '''Function to scrape the JCDecaux API every 5 minutes'''
    while True:
        try:
            r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})

            def get_availability(obj):
                return {'number': obj['number'],
                        'contract_name': obj['contract_name'],
                        'name': obj['name'],
                        'address': obj['address'],
                        'pos_lng': obj['position']['lng'],
                        'pos_lat': obj['position']['lat'],
                        'banking': obj['banking'],
                        'bonus': obj['bonus'],
                        'bike_stands': obj['bike_stands'],
                        'available_bike_stands': obj['available_bike_stands'],
                        'available_bikes': obj['available_bikes'],
                        'status': obj['status'],
                        'last_update': datetime.datetime.fromtimestamp(int(obj['last_update'] / 1e3))
                        }

            values = list(map(get_availability, r.json()))
            ins = availability.insert().values(values)
            engine.execute(ins)

            time.sleep(5 * 60)
        except:
            print('error')
    return

if __name__ == '__main__':
    main()