from selenium import webdriver

from time import sleep
from datetime import datetime

import json


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Remote(command_executor="http://standalone-chromium:4444/wd/hub", options=chrome_options)
driver.get("https://www.coincap.io")

sleep(3)

units = {'t':1000000000000, 'b':1000000000, 'm':1000000}

def scraping_coincap():
    tokens_to_json = []
    for i in range(1, 21, 1):
        token = {}
        token_names = driver.find_element_by_xpath(f"/html/body/div[2]/main/div[4]/div/table/tbody/tr[{i}]/td[2]/div/a").text
        token['name'] = token_names.split('\n')[0]
        token['symbol'] = token_names.split('\n')[1]
        token_value = driver.find_element_by_xpath(f"/html/body/div[2]/main/div[4]/div/table/tbody/tr[{i}]/td[3]/span").text
        token['currency'] = token_value[0]
        token['value'] = float(token_value[1:].replace(',', ''))
        token_market_cap = driver.find_element_by_xpath(f"/html/body/div[2]/main/div[4]/div/table/tbody/tr[{i}]/td[4]/span").text
        token['market_cap'] = int(float(token_market_cap[1:-1])*units[token_market_cap[-1]])
        token_volume = driver.find_element_by_xpath(f"/html/body/div[2]/main/div[4]/div/table/tbody/tr[{i}]/td[7]/span").text
        token['volume'] = int(float(token_volume[1:-1])*units[token_volume[-1]])
        scrap_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        token_to_li = {"measurement":f"{token['symbol']}", "tags":{"crypto_name":token['name'], "crypto_symbol":token['symbol']}, "time":scrap_time , "fields":token}
        tokens_to_json.append(token_to_li)
    return tokens_to_json

while True:
    print("Init record.")
    file_name = datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace('/', '-' ).replace(':', '-')
    export_to_json = scraping_coincap()
    print("Scraping success.")
    with open(f'./app/json_files/{file_name}.json', 'w') as f:
        json.dump(export_to_json, f)
    print(f"New record: {file_name}")
    sleep(30)
    