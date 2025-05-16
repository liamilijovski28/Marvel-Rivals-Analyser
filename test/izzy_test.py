from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest

class TestSignupLogin:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # Correct usage of ChromeDriverManager
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def teardown_method(self):
        self.driver.quit()

    def test_signup_success(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)
        self.driver.find_element(By.ID, "username").send_keys("testuser123")
        self.driver.find_element(By.ID, "password").send_keys("Secure123!")
        self.driver.find_element(By.ID, "player_id").send_keys("112233445")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)
        assert "Home" in self.driver.title or "Welcome" in self.driver.page_source

    def test_signup_existing_user(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)
        self.driver.find_element(By.ID, "username").send_keys("Pineapples117")
        self.driver.find_element(By.ID, "password").send_keys("Security123!")
        self.driver.find_element(By.ID, "player_id").send_keys("123456789")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)
        errors = self.driver.find_elements(By.CLASS_NAME, "form-error")
        assert any("already exists" in e.text.lower() for e in errors)

    def test_signup_missing_fields(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)
        self.driver.find_element(By.ID, "username").send_keys("")
        self.driver.find_element(By.ID, "password").send_keys("")
        self.driver.find_element(By.ID, "player_id").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)
        errors = self.driver.find_elements(By.CLASS_NAME, "form-error")
        assert len(errors) >= 1
        assert any("required" in e.text.lower() for e in errors)

    def test_login_redirect_from_signup(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Log in here").click()
        time.sleep(1)
        assert "/login" in self.driver.current_url
        assert "Login" in self.driver.title or "Login" in self.driver.page_source

    def test_signup_input_field_types(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)
        assert self.driver.find_element(By.ID, "username").get_attribute("type") == "text"
        assert self.driver.find_element(By.ID, "password").get_attribute("type") == "password"
        assert self.driver.find_element(By.ID, "player_id").get_attribute("type") == "text"


class TestHomePage:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def teardown_method(self):
        self.driver.quit()

    def login_as_existing_user(self):
        self.driver.get("http://127.0.0.1:5000/login")
        self.driver.find_element(By.ID, "username").send_keys("Pineapples117")
        self.driver.find_element(By.ID, "password").send_keys("Security123!")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)

    def test_home_redirects_if_not_logged_in(self):
        self.driver.get("http://127.0.0.1:5000/home")
        time.sleep(1)
        assert "/login" in self.driver.current_url or "Login" in self.driver.title

    def test_logged_in_user_can_access_home(self):
        self.login_as_existing_user()
        self.driver.get("http://127.0.0.1:5000/home")
        assert "Welcome" in self.driver.page_source or "Stats" in self.driver.page_source

    def test_logout_prevents_home_access(self):
        self.login_as_existing_user()
        self.driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)
        self.driver.get("http://127.0.0.1:5000/home")
        assert "/login" in self.driver.current_url

    def test_deleted_cookie_blocks_home(self):
        self.login_as_existing_user()
        self.driver.delete_all_cookies()
        self.driver.get("http://127.0.0.1:5000/home")
        assert "/login" in self.driver.current_url

    def test_user_cannot_access_other_user_home(self):
        self.login_as_existing_user()
        self.driver.get("http://127.0.0.1:5000/user/other_user_id/home")
        assert "Access Denied" in self.driver.page_source or "/home" in self.driver.current_url

    def test_username_escaping_on_home(self):
        self.login_as_existing_user()
        self.driver.get("http://127.0.0.1:5000/home")
        page = self.driver.page_source
        assert "<script>" not in page

    def test_protected_routes_redirect_if_not_logged_in(self):
        protected_routes = ["/home", "/compare", "/settings", "/matches"]
        for route in protected_routes:
            self.driver.get(f"http://127.0.0.1:5000{route}")
            assert "/login" in self.driver.current_url
    

class TestFriendsPage:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def teardown_method(self):
        self.driver.quit()

    def login_as_existing_user(self):
        self.driver.get("http://127.0.0.1:5000/login")
        self.driver.find_element(By.ID, "username").send_keys("Pineapples117")
        self.driver.find_element(By.ID, "password").send_keys("security")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)
        assert "/home" in self.driver.current_url or "Welcome" in self.driver.page_source


    def test_friends_redirects_if_not_logged_in(self):
        self.driver.get("http://127.0.0.1:5000/friends")
        assert "/login" in self.driver.current_url

    def test_logged_in_user_can_view_friends_page(self):
        self.login_as_existing_user()
        self.driver.get("http://127.0.0.1:5000/friends")
        assert "Friends" in self.driver.page_source

def test_accept_friend_request(self):
    # Setup: Create another user and send a friend request to Pineapples117
    from fetch.models import FriendRequest, User
    from app import db

    # Log in as Pineapples117
    self.login_as_existing_user()

    # Ensure another user exists
    another_user = User.query.filter_by(username="AnotherUser").first()
    if not another_user:
        from werkzeug.security import generate_password_hash
        another_user = User(username="AnotherUser", password=generate_password_hash("password"), player_id="987654321")
        db.session.add(another_user)
        db.session.commit()

    # Add a friend request from AnotherUser to Pineapples117
    incoming = FriendRequest(sender_id="AnotherUser", receiver_id="Pineapples117", status="pending")
    db.session.add(incoming)
    db.session.commit()

    # Go to friends page and accept the request
    self.driver.get("http://127.0.0.1:5000/friends")
    time.sleep(1)
    accept_buttons = self.driver.find_elements(By.CLASS_NAME, "accept")
    if accept_buttons:
        accept_buttons[0].click()
        time.sleep(1)
        assert "Accepted" in self.driver.page_source or "Remove" in self.driver.page_source
    else:
        pytest.fail("No accept button found — friend request setup may have failed.")



    def test_accept_friend_request(self):
        self.login_as_existing_user()
        self.driver.get("http://127.0.0.1:5000/friends")
        accept_buttons = self.driver.find_elements(By.CLASS_NAME, "accept")
        if accept_buttons:
            accept_buttons[0].click()
            time.sleep(1)
            assert "Accepted" in self.driver.page_source or "Remove" in self.driver.page_source
        else:
            pytest.skip("No friend requests to accept.")
