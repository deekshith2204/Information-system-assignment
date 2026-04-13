import os
import sys
import unittest

BACKEND_ROOT = r"C:\Users\thadv\OneDrive\Desktop\programming\babla-cars-project\backend"

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
sys.path.insert(0, BACKEND_ROOT)

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY  # noqa: E402
from utils.helper_functions import safe_int  # noqa: E402


class HelperFunctionTests(unittest.TestCase):
    def test_safe_int_returns_integer_value(self):
        self.assertEqual(safe_int("42"), 42)

    def test_safe_int_returns_fallback_for_invalid_input(self):
        self.assertEqual(safe_int("abc", fallback=7), 7)
        self.assertEqual(safe_int(None, fallback=3), 3)


class ConfigTests(unittest.TestCase):
    def test_security_config_defaults_are_defined(self):
        self.assertEqual(ALGORITHM, "HS256")
        self.assertTrue(isinstance(SECRET_KEY, str) and len(SECRET_KEY) > 0)
        self.assertGreater(ACCESS_TOKEN_EXPIRE_MINUTES, 0)


if __name__ == "__main__":
    unittest.main()
