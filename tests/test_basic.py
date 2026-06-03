import unittest
from app import create_app
from config import TestingConfig

class BasicTestCase(unittest.TestCase):
    """
    Basic verification test suite.
    Validates Flask factory setup, page loads, and configurations.
    """
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_is_testing(self):
        """Verify testing configuration is applied."""
        self.assertTrue(self.app.config["TESTING"])

    def test_home_page(self):
        """Verify that the home page (Bootstrap dashboard) loads successfully."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"QueryLens Dashboard", response.data)

    def test_api_schema_endpoint(self):
        """Verify that the api/schema placeholder endpoint functions."""
        response = self.client.get("/api/schema")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["status"], "success")

if __name__ == "__main__":
    unittest.main()
