from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pytest

class TestSignupLogin:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def teardown_method(self):
        self.driver.quit()

    def test_signup_success(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)

        self.driver.find_element(By.ID, "username").send_keys("testuser123")
        self.driver.find_element(By.ID, "password").send_keys("securepassword")
        self.driver.find_element(By.ID, "player_id").send_keys("1122334455")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)

        assert "Home" in self.driver.title or "Welcome" in self.driver.page_source

    def test_signup_existing_user(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)

        self.driver.find_element(By.ID, "username").send_keys("Pineapples117")  # already exists
        self.driver.find_element(By.ID, "password").send_keys("security")
        self.driver.find_element(By.ID, "player_id").send_keys("123456789")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)

        assert "already exists" in self.driver.page_source or "danger" in self.driver.page_source

    def test_signup_missing_fields(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)

        self.driver.find_element(By.ID, "username").send_keys("")
        self.driver.find_element(By.ID, "password").send_keys("")
        self.driver.find_element(By.ID, "player_id").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)

        assert "form-error" in self.driver.page_source or "This field is required" in self.driver.page_source

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