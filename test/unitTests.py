import unittest
from fetch import create_app
from fetch.config import TestingConfig
from fetch.models import User
from app import db
from fetch.controllers import try_change_settings, try_login, try_signup
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
    
    def test_failed_logi_password(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to log in with incorrect credentials
        result = try_login('testuser', 'wrongpassword')
        
        # Check if the result is the error message
        self.assertEqual(result, "Invalid username or password")

        # Clean up the test user
        db.session.delete(test_user)
        db.session.commit()
    
    def test_failed_login_username(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to log in with incorrect credentials
        result = try_login('wronguser', 'testpassword')
        
        # Check if the result is the error message
        self.assertEqual(result, "Invalid username or password")

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
    
    def test_failed_signup_username_exists(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='existinguser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to sign up with an existing username
        result = try_signup('existinguser', 'newpassword', '987654321')
        
        # Check if the result is the error message
        self.assertEqual(result, 'Username already exists. Please choose something else.')

        # Clean up the test user
        db.session.delete(test_user)
        db.session.commit()
    
    def test_failed_signup_player_id_exists(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to sign up with an existing player ID
        result = try_signup('newuser', 'newpassword', '123456789')
        
        # Check if the result is the error message
        self.assertEqual(result, "That Player ID is already linked to another account.")

        # Clean up the test user
        db.session.delete(test_user)
        db.session.commit()

    def test_failed_signup_player_id_wrong_length(self):
        # Attempt to sign up with a player ID that is not 9 digits
        result = try_signup('newuser', 'newpassword', '12345')
        
        # Check if the result is the error message
        self.assertEqual(result, "Player ID must be exactly 9 digits.")
    
    def test_change_settings(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to change settings
        new_username = 'updateduser'
        new_password = 'updatedpassword'
        new_playerID = '987654321'
        result = try_change_settings(new_username, new_password, new_playerID, data_sharing=True, restricted_friends=None, user=test_user)

        # Check if the result is the updated user object
        self.assertEqual(result.username, new_username)
        self.assertEqual(result.player_id, new_playerID)

        # Clean up the test user
        db.session.delete(test_user)
        db.session.commit()
    
    def test_change_settings_invalid_player_id(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Attempt to change settings with an invalid player ID
        new_username = 'updateduser'
        new_password = 'updatedpassword'
        new_playerID = '12345'
        result = try_change_settings(new_username, new_password, new_playerID, data_sharing=True, restricted_friends=None, user=test_user)

        # Check if the result is the error message
        self.assertEqual(result, "Player ID must be exactly 9 digits.")

        # Clean up the test user
        db.session.delete(test_user)
        db.session.commit()
    
    def test_change_settings_username_exists(self):
        # Create a test user
        hashed_password = generate_password_hash('testpassword')
        test_user = User(username='testuser', password=hashed_password, player_id='123456789')
        db.session.add(test_user)
        db.session.commit()

        # Create another test user
        hashed_password2 = generate_password_hash('testpassword2')
        test_user2 = User(username='existinguser', password=hashed_password2, player_id='987654321')
        db.session.add(test_user2)
        db.session.commit()

        # Attempt to change settings with an existing username
        new_username = 'existinguser'
        new_password = 'updatedpassword'
        new_playerID = '123456789'
        result = try_change_settings(new_username, new_password, new_playerID, data_sharing=True, restricted_friends=None, user=test_user)

        # Check if the result is the error message
        self.assertEqual(result, 'Username already exists. Please choose something else.')

        # Clean up the test users
        db.session.delete(test_user)
        db.session.delete(test_user2)
        db.session.commit()

        
    def tearDown(self):
        db.session.remove()  # remove current session
        db.drop_all()        # drop all tables
        self.app_context.pop()  # pop the app context
        return super().tearDown()
    
