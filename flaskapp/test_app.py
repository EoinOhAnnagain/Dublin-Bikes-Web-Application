try:
    from app import app
    import unittest
except Exception as e:
    print("Some modules are missing {} ".format(e))

class FlaskTest(unittest.TestCase):



    ## Index tests

    def test_index(self):
        tester = app.test_client(self)

        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        
    def test_index2(self):
        tester = app.test_client(self)

        response = tester.get("/home")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)



    ## Map tests

    def test_map(self):
        tester = app.test_client(self)

        response = tester.get("/map")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)



    ## Stations tests

    def test_stations(self):
        tester = app.test_client(self)

        response = tester.get("/stations")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)




        
if __name__ == "__main__":
    unittest.main()