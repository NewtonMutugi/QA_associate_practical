from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()

# Define variables
chrome_location = os.getenv("GOOGLE_CHROME_LOCATION")
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
url = os.getenv("URL")

print(f"username: {username}\nPassword: {password}")

options = webdriver.ChromeOptions()
options.add_argument(chrome_location)
options.add_argument("--no-sand-box")
options.add_argument("--start-maximised")
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Connect to KenyaEMR
driver = webdriver.Chrome(options)
driver.get(url)
driver.implicitly_wait(5)

# Navigate to username field
username_field = driver.find_element(By.ID, "username")
username_field.click()
username_field.send_keys(username)
button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
button.click()

# Navigate to password field
password_field = driver.find_element(By.ID, "password")
password_field.click()
password_field.send_keys(password)
login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_btn.click()
driver.implicitly_wait(5)

try:
    # xpath = '//*[@id="single-spa-application:@kenyaemr/esm-login-app-page-0"]/div/div[1]/div[1]/div/div/div/div[2]'
    error_msg = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".cds--inline-notification__subtitle")
        )
    ).get_attribute("innerText")
    error_msg = error_msg.strip()

    # Confirm whether error message text is for invalid username or password
    assert error_msg == "Invalid username or password"
    print(error_msg)
except (NoSuchElementException, TimeoutException):
    print("Login successful")
except AssertionError:
    print(f"Unexpected output: {error_msg}")


driver.quit()
