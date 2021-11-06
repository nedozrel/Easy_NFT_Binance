from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chrome_options
import time
import json


def get_options():
    options = chrome_options()
    return options


def get_driver(options=None):
    driver = webdriver.Chrome(options=options)
    return driver


def get_page(driver, url):
    if url.find('binance') != -1:
        try:
            driver.get(url)
        except Exception:
            print('Что то пошло не так :(')
    else:
        print('Ссылка не является ссылкой на сайт Binance!')
    time.sleep(2)


def save_cookies(driver):
    with open('cookies.json', 'w') as file:
        json.dump(driver.get_cookies(), file)


def load_cookies(driver):
    with open('cookies.json', 'r') as cookies_file:
        cookies = json.load(cookies_file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(2)


def main():
    print('Дождитесь загрузки браузера и залогиньтесь на бинанс...')
    url = 'https://www.binance.com/ru'
    driver = get_driver(options=get_options())
    get_page(driver, url)
    load_cookies(driver)
    driver.refresh()
    input('Если вы уже залогинены нажмите Enter')
    save_cookies(driver)
    input('Нажмите Enter для завершения работы программы')


if __name__ == '__main__':
    main()
