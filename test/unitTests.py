import unittest
from fetch import create_app
from fetch.config import TestingConfig
from fetch.models import User
from app import db
from fetch.controllers import try_login, try_signup
from werkzeug.security import generate_password_hash

class UnitTests(unittest.TestCase):
    
    def setUp(self):
        test_app = create_app(TestingConfig)
        self.app_context = test_app.app_context()
        self.app_context.push()
        db.create_all()

        return super().setUp()

    
    def test_successful_login(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to log in with the correct credentials
        result = try_login('testuser', 'testpassword')
        
        # Check if the result is the user object
        self.assertEqual(result, test_user)

        # Clean up the test user
        db.session.delete(test_user)
        db.session.commit()

    def test_successful_signup(self):
        # Attempt to sign up with valid credentials
        result = try_signup('newuser', 'newpassword', '987654321')
        
        # Check if the result is the user object
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, 'newuser')
        self.assertEqual(result.player_id, '987654321')

        # Clean up the test user
        db.session.delete(result)
        db.session.commit()

    def tearDown(self):
        db.session.remove()  # remove current session
        db.drop_all()        # drop all tables
        self.app_context.pop()  # pop the app context
        return super().tearDown()
    
