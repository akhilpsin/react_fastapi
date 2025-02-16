import unittest
import json
from user_mng import read_dictionary_from_file, update_local_file, register_user, login, remove_user, toggle_user_status

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        """Set up a test file and dictionary."""
        self.test_file = 'test_log_users.json'
        self.test_db = {}
        update_local_file(self.test_file, self.test_db)
    
    def tearDown(self):
        """Clean up test file."""
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_register_user(self):
        """Test user registration."""
        result = register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        self.assertEqual(result, "User registered successfully")
        self.assertIn("testuser", self.test_db)
    
    def test_register_existing_user(self):
        """Test registering a user that already exists."""
        register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        result = register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        self.assertEqual(result, "Username already exists")
    
    def test_login_success(self):
        """Test successful login."""
        register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        result = login(self.test_db, "testuser", "securepassword")
        self.assertEqual(result, "Login successful")
    
    def test_login_invalid_username(self):
        """Test login with an invalid username."""
        result = login(self.test_db, "nonexistent", "password")
        self.assertEqual(result, "Invalid username")
    
    def test_login_incorrect_password(self):
        """Test login with an incorrect password."""
        register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        result = login(self.test_db, "testuser", "wrongpassword")
        self.assertEqual(result, "Incorrect password")
    
    def test_remove_user(self):
        """Test removing a user."""
        register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        result = remove_user(self.test_db, self.test_file, "testuser")
        self.assertEqual(result, "User removed successfully")
        self.assertNotIn("testuser", self.test_db)
    
    def test_toggle_user_status(self):
        """Test enabling and disabling a user."""
        register_user(self.test_db, self.test_file, "testuser", "Test", "User", "test@example.com", "1234567890", "securepassword")
        result_disable = toggle_user_status(self.test_db, self.test_file, "testuser", True)
        self.assertEqual(result_disable, "User disabled successfully")
        self.assertTrue(self.test_db["testuser"]["disabled"])
        
        result_enable = toggle_user_status(self.test_db, self.test_file, "testuser", False)
        self.assertEqual(result_enable, "User activated successfully")
        self.assertFalse(self.test_db["testuser"]["disabled"])

if __name__ == "__main__":
    unittest.main()
