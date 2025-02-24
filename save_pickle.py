import pickle
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time 
import random

def save_pickle():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)

    driver.get("https://www.facebook.com/")

    tk = input("nhap tk: ")
    mk = input("nhap mk")

    username = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Email address or phone number"]'))
        )
    username.click()

    ActionChains(driver).send_keys(tk).perform()

    password = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Password"]'))
        )
    password.click()


    ActionChains(driver).send_keys(mk).send_keys(Keys.ENTER).perform()

    time.sleep(random.randint(2,3))

    pickle_name = "pickle/" + tk + ".pickle"

    with open(pickle_name, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    if driver.current_url == "https://www.facebook.com/":
        print("lưu pickle thành công")
    else:
        print("sai tk hoặc mk")

    driver.quit()
