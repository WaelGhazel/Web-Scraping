import csv
import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from petl import header

driver = webdriver.Chrome(service=Service("./Assets/chromedriver.exe"),options=webdriver.ChromeOptions())

with open('./Assets/ResultCleaned.csv', 'r', encoding='UTF8', newline='') as f:
    reader = csv.DictReader(f)
    data = list(reader)

    counter = 0
    path = os.getcwd()
    path = os.path.join(path,"Assets")
    path = os.path.join(path,"images")
    for product in data:
        print(product["image"])
        save_as = os.path.join(path,str(counter)+".jpg")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(product["image"],headers=headers)
        if response.status_code == 200:
            with open(save_as, 'wb') as f:
                f.write(response.content)
        product.update({"image":save_as})
        counter +=1
        time.sleep(1)
    print(data)
    with open('./Assets/Resultfinal.csv', 'w', encoding='UTF8', newline='') as f:
        fieldnames = list(header(data))
        # fieldnames= header(dataframe)
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
