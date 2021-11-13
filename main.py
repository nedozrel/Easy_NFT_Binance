from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from json.decoder import JSONDecodeError


def get_options():
    options = chrome_options()
    try:
        with open('proxy.txt', 'r') as file:
            proxy = file.read()
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
    except FileNotFoundError as e:
        pass
    options.page_load_strategy = 'eager'
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
    try:
        with open('cookies.json', 'r') as cookies_file:
            cookies = json.load(cookies_file)
    except ValueError:
        with open('cookies.json', 'w') as cookies_file:
            cookies_file.write('{}')
        with open('cookies.json', 'r') as cookies_file:
            cookies = json.load(cookies_file)
    for cookie in cookies:
        driver.add_cookie(cookie)


def check_auth(driver, timeout=5):
    try:
        return WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.1) \
            .until(EC.any_of(EC.visibility_of_element_located((By.CSS_SELECTOR, '#__APP > div > header > div:nth-child(4) > div > svg > use')),
                             EC.visibility_of_element_located((By.CSS_SELECTOR, 'svg.css-6px2js'))))
    except TimeoutException:
        return False


def do_auth(driver):
    print('Ожидание авторизации...')
    get_page(driver, 'https://accounts.binance.com/ru/login')
    WebDriverWait(driver=driver, timeout=600, poll_frequency=1) \
        .until(EC.any_of(EC.visibility_of_element_located((By.CSS_SELECTOR, '#__APP > div > header > div:nth-child(4) > div > svg > use')),
                         EC.visibility_of_element_located((By.CSS_SELECTOR, 'svg.css-6px2js'))))
    save_cookies(driver)


def click_btn(css_selector: str, driver, timeout=5, poll_frequency=0.00000000000000000000000000000001):
    try:
        btn = driver.find_element(By.CSS_SELECTOR, css_selector)
        btn.click()
    except NoSuchElementException:
        btn = WebDriverWait(driver=driver, timeout=timeout, poll_frequency=poll_frequency) \
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        btn.click()
    return btn


def main():
    print('Загрузка браузера...')
    url = 'https://www.binance.com/ru/'
    options = get_options()
    driver = get_driver(options=options)
    get_page(driver, url)
    load_cookies(driver)
    driver.refresh()
    authenticated = check_auth(driver)
    if not authenticated:
        do_auth(driver)
    url = str(input('Вставьте ссылку на минт: ')).strip()
    nft_amount = str(input('Введите количество NFT для покупки: ')).strip()
    driver.get(url)

    # Нажатие на кнопку соглашения с условиями бинанса
    click_btn('button.css-1mtehst', driver=driver)

    print('Ожидание дропа...')

    # Нажатие на поле ввода количества NFT
    nft_num_input = click_btn('button.css-1w6omp2', driver=driver, timeout=60*60*24)
    if nft_amount != '1' or nft_amount != '':
        nft_num_input.clear().send_keys(nft_amount)

    click_btn('button.css-13irzvu', driver)  # Нажатие на кнопку покупки
    click_btn('button.css-d8znws', driver=driver)  # Нажатие на кнопку подтверждения покупки

    input('Нажмите Enter для завершения работы программы')


if __name__ == '__main__':
    main()
