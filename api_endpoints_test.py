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


if __name__ == "__main__":
    unittest.main()