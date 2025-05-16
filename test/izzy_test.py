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
        self.driver.find_element(By.ID, "password").send_keys("Secure123!")
        self.driver.find_element(By.ID, "player_id").send_keys("112233445")  # Must be exactly 9 digits
        self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(1)

        assert "Home" in self.driver.title or "Welcome" in self.driver.page_source

    def test_signup_existing_user(self):
        self.driver.get("http://127.0.0.1:5000/signup")
        time.sleep(1)

        self.driver.find_element(By.ID, "username").send_keys("Pineapples117")  # Already exists
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
