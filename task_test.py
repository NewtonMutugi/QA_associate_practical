import logging
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import HtmlTestRunner


class TestChromeLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        chrome_location = os.getenv("GOOGLE_CHROME_LOCATION")
        options = webdriver.ChromeOptions()
        options.add_argument(chrome_location)
        options.add_argument("--no-sand-box")
        options.add_argument("--start-maximised")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(options)
        cls.driver.implicitly_wait(5)

    def test_valid_login(self):
        username = os.getenv("USER_NAME")
        password = os.getenv("PASSWORD")
        self.login_logic(username, password)

    def test_invalid_login(self):
        username = "invalid_username"
        password = "invalid_password"
        self.login_logic(username, password)

    # Login logic
    def login_logic(self, username, password):
        driver = self.driver
        url = os.getenv("URL")
        driver.get(url)
        driver.implicitly_wait(5)
        username_field = driver.find_element(By.ID, "username")
        username_field.click()
        username_field.send_keys(username)
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()
        password_field = driver.find_element(By.ID, "password")
        password_field.click()
        password_field.send_keys(password)
        login_btn = driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        driver.implicitly_wait(5)

        # Check for login success or failure
        try:
            error_msg_xpath = '//*[@id="single-spa-application:@kenyaemr/esm-login-app-page-0"]/div/div[1]/div[1]/div/div/div/div[2]'
            error_msg = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, error_msg_xpath))
            ).get_attribute("innerText").strip()
            self.assertEqual(
                error_msg, "Invalid username or password", "Unexpected error message found")
        except (NoSuchElementException, TimeoutException):
            print("Login successful")
        except AssertionError:
            self.fail(f"Unexpected output: {error_msg}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))
