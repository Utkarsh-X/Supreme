import unittest
from auth_service import AuthService

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.service = AuthService()

    def test_valid_registration(self):
        result = self.service.register_user("alice@example.com", "Password123")
        self.assertIsNotNone(result)
        self.assertIn("token", result)
        self.assertIn("alice@example.com", self.service.users)

    def test_short_password(self):
        with self.assertRaises(ValueError):
            self.service.register_user("bob@example.com", "short1")

    def test_no_digit_password(self):
        with self.assertRaises(ValueError):
            self.service.register_user("charlie@example.com", "NoDigitsHere")

if __name__ == "__main__":
    unittest.main()
