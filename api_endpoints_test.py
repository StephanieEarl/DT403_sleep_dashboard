import unittest
from app import app

class TestApiEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_sessions_attended(self):
        # test the sessions attended endpoint
        response = self.app.get("api/sessions_attended")
        # Check the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Test if the response is in JSON format
        self.assertTrue(response.is_json)

        # Test if the response contains the expected keys
        self.assertTrue("dates" in response.json)
        self.assertTrue("attended" in response.json)

        # Test if the dates response is in the list
        self.assertIsInstance(response.json["dates"], list)

        # Test to see if attended response is an integer
        self.assertTrue(all(isinstance(x, int) for x in response.json["attended"]))


if __name__ == "__main__":
    unittest.main()