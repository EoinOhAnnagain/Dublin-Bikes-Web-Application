try:
    from app import app
    import unittest
    from sqlalchemy import create_engine
    import pandas as pd
    from APID import *
except Exception as e:
    print("Some modules are missing {} ".format(e))

class FlaskTest(unittest.TestCase):


    ## Tests on pages
    ## This section contains tests on the pages that make up the web app.
    ## Please note I have only provided docstrings and comments on the ones related to index as the map and stations ones are functionally the same.
    
    ## Index tests

    def test_index(self):
        """This test checks that the correct status code is returned when accessing the index page.
            It will fail if the status code returned is not 200."""
        tester = app.test_client(self)
        response = tester.get("/")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        
    def test_index2(self):
        """This is a second test on the status code for index using its second access point of /home
            This route is not checked for the remaining tests on index as if both as successful then the remaining tests will have identical responces."""
        tester = app.test_client(self)
        response = tester.get("/home")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
        """Check on the type of content that is returned.
            Expected return is text/html; charset=utf-8."""
        tester = app.test_client(self)
        response = tester.get("/")

        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_index_data(self):
        """Check on the data returned. Makes several check."""
        tester = app.test_client(self)
        response = tester.get("/")

        self.assertTrue(b'Home Page' in response.data) ## Check that the correct page title is returned.
        self.assertTrue(b'Home' in response.data) ## check that the correct page name is returned.
        
        ## The following checks are for the opening and closing html tags. These are provided by base.html with index extends. If they fail then the pages are not connecting correctly. 
        self.assertTrue(b'<html>' in response.data)
        self.assertTrue(b'</html>' in response.data)



    ## Map tests

    def test_map(self):
        tester = app.test_client(self)

        response = tester.get("/map")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_map_content(self):
        tester = app.test_client(self)
        response = tester.get("/map")

        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_map_data(self):
        tester = app.test_client(self)
        response = tester.get("/map")

        self.assertTrue(b'Map Page' in response.data)
        self.assertTrue(b'Stations Map' in response.data)
        self.assertTrue(b'<html>' in response.data)
        self.assertTrue(b'</html>' in response.data)



    ## Stations tests

    def test_stations(self):
        tester = app.test_client(self)

        response = tester.get("/stations")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_stations_content(self):
        tester = app.test_client(self)
        response = tester.get("/stations")

        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_stations_data(self):
        tester = app.test_client(self)
        response = tester.get("/stations")

        self.assertTrue(b'Stations List' in response.data)
        self.assertTrue(b'Stations' in response.data)
        self.assertTrue(b'<html>' in response.data)
        self.assertTrue(b'</html>' in response.data)





    ## The following are tests run on the database connection and the queries. 
    ## Similar to above there are three main tests run (status code, data type, and data contents) and only the ones for index contain docstrings and comments unless there are major differences.
    
    ## Database Checkes for Index

    def test_index_database_connection_availability(self):
        '''This function tests that a successful status code is retuned from the availability table database search'''
        
        tester = app.test_client(self)
        response = tester.get("/bike_stand_query")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_database_connection_weather(self):
        '''This function tests that a successful status code is retuned from the weather table database search'''
        
        tester = app.test_client(self)
        response = tester.get("/home_weather_query")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_database_return_type_availability(self):
        '''This function tests that the return from the query on the availability database table is of the correct type'''

        tester = app.test_client(self)
        response = tester.get("/bike_stand_query")

        self.assertTrue(type(response), 'string')

    def test_index_database_return_type_weather(self):
        '''This function tests that the return from the query on the weather database table is of the correct type'''

        tester = app.test_client(self)
        response = tester.get("/home_weather_query")

        self.assertTrue(type(response), 'string')

    def test_index_database_data_availability(self):
        '''This function tests that the return from the query on the availability database table contains the expected headings'''

        tester = app.test_client(self)
        response = tester.get("/bike_stand_query")
        data = response.data
        
        ## The returned data is checked for the following which should be the headings of the data's columns.
        self.assertTrue(b'name' in data)
        self.assertTrue(b'available_bikes' in data)
        self.assertTrue(b'available_bike_stands' in data)
        self.assertTrue(b'status' in data)

        ## This line tests that the corrent number of tubles are returned by counting the occurance of one of the headings for the table. It will appear once for each returned row.
        self.assertEqual(data.count(b'name'), 109)

    def test_index_database_data_weather(self):
        '''This function tests that the return from the query on the weather database table contains the expected headings'''

        tester = app.test_client(self)
        response = tester.get("/home_weather_query")
        data = response.data
        
        ## The returned data is checked for the following which should be the headings of the data's columns.
        self.assertTrue(b'WeatherIcon' in data)
        self.assertTrue(b'IconPhrase' in data)
        self.assertTrue(b'Rain' in data)
        self.assertTrue(b'Temperature' in data)
        self.assertTrue(b'RealFeelTemperature' in data)
        self.assertTrue(b'CloudCover' in data)
        self.assertTrue(b'PrecipitationProbability' in data)
        self.assertTrue(b'RelativeHumidity' in data)
        self.assertTrue(b'WindSpeed' in data)

        ## This line tests that the corrent number of tubles are returned by counting the occurance of one of the headings for the table. It will appear once for each returned row.
        self.assertEqual(data.count(b'WeatherIcon'), 1)






        ## Database Checkes for Maps

    def test_maps_database_connection_stations(self):
        tester = app.test_client(self)
        response = tester.get("/mapquery")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_maps_database_return_type_stations(self):
        tester = app.test_client(self)
        response = tester.get("/mapquery")

        self.assertTrue(type(response), 'string')

    def test_maps_database_data_stations(self):
        tester = app.test_client(self)
        response = tester.get("/mapquery")
        data = response.data
        
        self.assertTrue(b'number' in data)
        self.assertTrue(b'contract_name' in data)
        self.assertTrue(b'name' in data)
        self.assertTrue(b'address' in data)
        self.assertTrue(b'pos_lat' in data)
        self.assertTrue(b'pos_lng' in data)
        self.assertTrue(b'banking' in data)
        self.assertTrue(b'bonus' in data)
        self.assertTrue(b'bike_stands' in data)
        self.assertTrue(b'available_bike_stands' in data)
        self.assertTrue(b'available_bikes' in data)
        self.assertTrue(b'status' in data)
        self.assertTrue(b'last_update' in data)
        self.assertTrue(b'post_time' in data)
        
        self.assertEqual(data.count(b'number'), 109)

    def test_maps_database_connection_occupancy(self):
        tester = app.test_client(self)
        response = tester.get("/occupancy/42")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_maps_database_return_type_occupancy(self):
        tester = app.test_client(self)
        response = tester.get("/occupancy/42")

        self.assertTrue(type(response), 'string')

    def test_map_database_data_occupancy(self):
        tester = app.test_client(self)
        response = tester.get("/occupancy/42")
        data = response.data

        self.assertTrue(b'number' in data)
        self.assertTrue(b'last_update' in data)
        self.assertTrue(b'available_bike_stands' in data)
        self.assertTrue(b'available_bikes' in data)
        self.assertTrue(b'name' in data)
        
        self.assertEqual(data.count(b'name'), 32)






        ## Database Checkes for Stations

    def test_stations_database_connection_stations(self):
        tester = app.test_client(self)
        response = tester.get("/stationsquery")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_stations_database_return_type_stations(self):
        tester = app.test_client(self)
        response = tester.get("/stationsquery")

        self.assertTrue(type(response), 'string')

    def test_stations_database_data_stations(self):
        tester = app.test_client(self)
        response = tester.get("/stationsquery")
        data = response.data
        
        self.assertTrue(b'number' in data)
        self.assertTrue(b'contract_name' in data)
        self.assertTrue(b'name' in data)
        self.assertTrue(b'address' in data)
        self.assertTrue(b'pos_lat' in data)
        self.assertTrue(b'pos_lng' in data)
        self.assertTrue(b'banking' in data)
        self.assertTrue(b'bonus' in data)
        self.assertTrue(b'bike_stands' in data)
        self.assertTrue(b'available_bike_stands' in data)
        self.assertTrue(b'available_bikes' in data)
        self.assertTrue(b'status' in data)
        self.assertTrue(b'last_update' in data)
        self.assertTrue(b'post_time' in data)
        
        self.assertEqual(data.count(b'number'), 109)




    
        
    



    

 


        
if __name__ == "__main__":
    unittest.main()