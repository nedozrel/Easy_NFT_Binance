from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def save_cookies(driver):
    with open('cookies.json', 'w') as file:
        json.dump(driver.get_cookies(), file)


def load_cookies(driver):
    with open('cookies.json', 'r') as cookies_file:
        cookies = json.load(cookies_file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(0.1)


def main():
    print('Дождитесь загрузки браузера...')
    url = 'https://www.binance.com/ru'
    driver = get_driver(options=get_options())
    get_page(driver, url)
    load_cookies(driver)
    driver.refresh()
    wait = WebDriverWait(driver=driver, timeout=3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg.css-mykl4n')))
    try:
        driver.find_element(By.CSS_SELECTOR, 'header_register')
        get_page(driver, 'https://accounts.binance.com/ru/login')
        input('Войдите в аккаунт, а затем нажмите Enter')
        save_cookies(driver)
    except NoSuchElementException:
        pass
    input('Нажмите Enter для завершения работы программы')


if __name__ == '__main__':
    main()
