try:
    from app import app
    import unittest
except Exception as e:
    print("Some modules are missing {} ".format(e))

class FlaskTest(unittest.TestCase):

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
        
if __name__ == "__main__":
    unittest.main()