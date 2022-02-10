import unittest
from app import app

class NewsletterTestCases(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "StefansWebshop.com"
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["WTF_CSRF_METHODS"] = []
        app.config["TESTING"] = True
    
    def test_fail_if_already_subscribed(self):
        test_client = app.test_client()
        url = "/"
        with test_client:
            response = test_client.post(url, data= dict(email = "admin@example.com") )
            assert response.status_code != 302


if __name__ == "__main__":
    unittest.main()
