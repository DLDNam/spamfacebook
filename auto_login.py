import requests 
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time 
import random
import os
import threading

driver_lock = threading.Lock()

def get_token(ip):
    url = "https://2fa.live/tok/" + ip 
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        token = data["token"]
    else:
        print(f"Error: {response.status_code}")
    return token


def main(index,text):
    options = uc.ChromeOptions()
    profile_directory = f"Profile_{index}"
    if not os.path.exists(profile_directory):
        os.makedirs(profile_directory)

    with driver_lock:
        try:
            options.user_data_dir = profile_directory
            driver = uc.Chrome(options=options)
        except Exception:
            print(f"Lỗi 1 ở luồng {index + 1}")
            time.sleep(180)

    driver.get("https://www.facebook.com/")

    a = text.split("|")
    tk, mk, token = a[0], a[1], a[2]


    time.sleep(4)
    username = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id="email"]'))
        )
    username.click()

    ActionChains(driver).send_keys(tk).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(mk).send_keys(Keys.ENTER).perform()

   
    ActionChains(driver).send_keys(token).send_keys(Keys.ENTER).perform()

    time.sleep(random.randint(2,3))

    trust_device = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Tin cậy thiết bị này"]'))
        )
    trust_device.click()


