from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv
from time import sleep

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

# Connect to KenyaEMR
driver = webdriver.Chrome(options)
driver.get(url)
sleep(5)

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
sleep(5)

try:
    status = driver.find_element(By.CSS_SELECTOR, "div[role='status']")
    print("Invalid username or password")
except NoSuchElementException:
    print("Login successful")
sleep(10)

driver.quit()
