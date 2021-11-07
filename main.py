from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
# import os


def get_options():
    options = chrome_options()
    # path = os.path.abspath("selenium")
    # options.add_argument("user-data-dir=" + path)
    return options


def get_driver(options):
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


def check_auth(driver, timeout=5):
    try:
        wait = WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.1) \
            .until(EC.any_of(EC.presence_of_element_located((By.ID, 'account-f')),
                             EC.presence_of_element_located((By.CSS_SELECTOR, 'svg.css-6px2js'))))
    except TimeoutException:
        return False
    return True


def do_auth(driver):
    get_page(driver, 'https://accounts.binance.com/ru/login')
    print('Ожидание авторизации...')
    wait = WebDriverWait(driver=driver, timeout=600, poll_frequency=1) \
        .until(EC.any_of(EC.presence_of_element_located((By.ID, 'account-f')),
                         EC.presence_of_element_located((By.CSS_SELECTOR, 'svg.css-6px2js'))))
    save_cookies(driver)


def main():
    print('Загрузка браузера...')
    url = 'https://www.binance.com/ru/'
    option = get_options()
    driver = get_driver(options=option)
    get_page(driver, url)
    load_cookies(driver)
    driver.refresh()
    authenticated = check_auth(driver, 5)
    if not authenticated:
        do_auth(driver)
    url = input('Вставьте ссылку на минт: ')
    number_of_nfts = int(input('Введите количество NFT для покупки: '))
    get_page(driver, url)
    wait = WebDriverWait(driver=driver, timeout=5, poll_frequency=0.1) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.css-1mtehst')))
    if EC.presence_of_element_located((By.CSS_SELECTOR, 'button.css-1mtehst')):
        accept_terms = driver.find_element(By.CSS_SELECTOR, 'button.css-1mtehst')
        accept_terms.click()

    input('Нажмите Enter для завершения работы программы')


if __name__ == '__main__':
    main()
