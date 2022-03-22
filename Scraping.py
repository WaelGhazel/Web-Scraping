#selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#other imports
import os
import wget
import time
from pprint import pprint
import csv
from petl import header


#code
driver = webdriver.Chrome(service=Service("./Assets/chromedriver.exe"),options=webdriver.ChromeOptions())
driver.get("https://www.jumia.com.tn/")

closeButton = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='newsletter_popup_close-cta']")))
closeButton.click()
time.sleep(1)


search = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[name='q']")))
search.clear()
search.send_keys("gilet homme")
#in case we need an enter instead of a send button
#search.send_keys(Keys.ENTER)
time.sleep(0.5)

searchButton = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Rechercher')]")))
searchButton.click()
time.sleep(1)

products = []


while(driver.find_elements(by=By.CSS_SELECTOR, value="a[aria-label='Page suivante']")!=None):
    # scroll behavior
    driver.execute_script("window.scrollTo(0,6000);")

    # selecting images
    images = driver.find_elements(by=By.TAG_NAME, value='img')
    imagess = [image.get_attribute('data-src') for image in images]
    if len(imagess) < 1:
        imagess = [image.get_attribute('src') for image in images]
    names = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="name"]')
    namess = [name.get_attribute("innerHTML") for name in names]
    prices = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="prc"]')
    pricess = [price.get_attribute("innerHTML") for price in prices]
    old_prices = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="old"]')
    olds = [old.get_attribute("innerHTML") for old in old_prices]

    for i in range(len(olds)):
        product = {"name": namess[i],
                   "old_price": olds[i],
                   "new_price": pricess[i],
                   "image": imagess[i],
                   }
        products.append(product)

    print("ok")
    print(driver.find_elements(by=By.CSS_SELECTOR, value="a[aria-label='Page suivante']"))
    if len(driver.find_elements(by=By.CSS_SELECTOR, value="a[aria-label='Page suivante']"))>0 :
        next = driver.find_element(by=By.CSS_SELECTOR, value="a[aria-label='Page suivante']")
        driver.execute_script("arguments[0].click();", next)
    else :
        break
    time.sleep(1)



time.sleep(1)
pprint(products)
print(len(products))

#removing old saves
if os.path.exists("./Assets/Result.csv"):
  os.remove("./Assets/Result.csv")

with open('./Assets/Result.csv', 'w', encoding='UTF8', newline='') as f:
    fieldnames = list(header(products))
    # fieldnames= header(dataframe)
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)