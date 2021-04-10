try:
    from app import app
    import unittest
except Exception as e:
    print("Some modules are missing {} ".format(e))

class FlaskTest(unittest.TestCase):


    ## Tests on pages
    ## This section contains tests on the pages that make up the web app.
    ## Please note I have only provided docstrings and comments on the ones related to index as the map and stations ones are functionally the same.
    
    ## Index tests

    def test_index(self):
        '''This test checks that the correct status code is returned when accessing the index page.
            It will fail if the status code returned is not 200'''
        tester = app.test_client(self)
        response = tester.get("/")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        
    def test_index2(self):
        '''This is a second test on the status code for index using its second access point of /home
            This route is not checked for the remaining tests on index as if both as successful then the remaining tests will have identical responces'''
        tester = app.test_client(self)
        response = tester.get("/home")

        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
        '''Check on the type of content that is returned.
            Expected return is text/html; charset=utf-8'''
        tester = app.test_client(self)
        response = tester.get("/")

        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_index_data(self):
        '''Check on the data returned. Makes several check.'''
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

    


        
if __name__ == "__main__":
    unittest.main()