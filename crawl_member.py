import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import pickle
import random


def get_links(link,file_pickle,file_csv):
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.get("https://www.facebook.com/")
    time.sleep(random.randint(1,3))
    file_pickle = "pickle/" + file_pickle 

    try: 
        with open(file_pickle, 'rb') as file:
            cookies = pickle.load(file)
        for cookie in cookies: 
            driver.add_cookie(cookie)
    except FileNotFoundError:
        print("File cookies.pkl không tìm thấy. Hãy lưu cookietrước khi chạy đoạn mã này.")
    driver.get(link)
    page_length = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            print("page = ",page_length)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait = WebDriverWait(driver, 20)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')


            time.sleep(5)
            new_page_length =  driver.execute_script("return document.body.scrollHeight")
            print("new_page = ",new_page_length)
            if new_page_length == page_length:
                break
            else:
                page_length = new_page_length
        except Exception:
            continue

    members = driver.find_elements(By.XPATH, "//div[@role='listitem']")

    links_user = []
    for member in members:
        profile_element = member.find_element(By.XPATH, ".//a[@href]")
        links_user.append(profile_element.get_attribute("href"))

    df_existing = pd.read_csv(file_csv)
    df_new = pd.DataFrame({
        "link": links_user,
        "status": 0
    })

    df_filtered = df_new[~df_new['link'].isin(df_existing['link'])]

    if not df_filtered.empty:
        df_combined = pd.concat([df_existing, df_filtered], ignore_index=True)
        df_combined.to_csv("link_face.csv", index=False)



