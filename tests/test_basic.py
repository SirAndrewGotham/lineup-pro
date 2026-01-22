"""Basic tests for LineUp Pro"""
import unittest

class TestBasic(unittest.TestCase):
    def test_imports(self):
        """Test that core modules can be imported"""
        try:
            from core import models
            from data import database
            from utils import config_manager
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")

if __name__ == '__main__':
    unittest.main()
