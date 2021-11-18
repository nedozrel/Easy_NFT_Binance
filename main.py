from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import requests
import sys
import traceback


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
    with open('data/error.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    input('Произошла фатальная ошибка, нажмите кнопку Enter или крестик для завершения работы.')


sys.excepthook = log_uncaught_exceptions


def get_options():
    options = chrome_options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        with open('data/proxy.txt', 'r') as file:
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
    with open('data/cookies.json', 'w') as file:
        json.dump(driver.get_cookies(), file)


def load_cookies(driver):
    try:
        with open('data/cookies.json', 'r') as cookies_file:
            cookies = json.load(cookies_file)
    except ValueError:
        with open('data/cookies.json', 'w') as cookies_file:
            cookies_file.write('{}')
        with open('data/cookies.json', 'r') as cookies_file:
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


def wait_purchase_btn(driver, timeout=60*60*24*3, poll_frequency=0.00000000000000000000000000000001):
    WebDriverWait(driver=driver, timeout=timeout, poll_frequency=poll_frequency)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.css-13irzvu')))


def send_num_of_nfts(driver, nft_amount):
    if nft_amount != '1' or nft_amount != '' or nft_amount != '0':
        try:
            nft_num_input = driver.find_element(By.CSS_SELECTOR, 'input.css-1w6omp2')
            nft_num_input.click()
            nft_num_input.send_keys(Keys.DELETE, Keys.BACK_SPACE)
            nft_num_input.send_keys(nft_amount)
        except NoSuchElementException:
            pass
        except ElementClickInterceptedException:
            pass


def click_btn(css_selector: str, driver, timeout=5, poll_frequency=0.00000000000000000000000000000001):
    try:
        btn = WebDriverWait(driver=driver, timeout=timeout, poll_frequency=poll_frequency) \
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        btn.click()
    except ElementClickInterceptedException:
        btn = click_btn(css_selector, driver)
    except TimeoutException:
        return False
    return btn


def main():
    print('Загрузка браузера...')
    url = 'https://www.binance.com/ru/'
    options = get_options()
    driver = get_driver(options=options)
    get_page(driver, url)
    load_cookies(driver)
    driver.refresh()
    authenticated = check_auth(driver, timeout=10)
    if not authenticated:
        do_auth(driver)
    url = str(input('Вставьте ссылку на минт: ')).strip()
    nft_amount = str(input('Введите количество NFT для покупки: ')).strip()
    driver.get(url)

    click_btn('button.css-1mtehst', driver=driver) # Нажатие на кнопку соглашения с условиями бинанса
    print('Ожидание дропа...')
    wait_purchase_btn(driver)
    send_num_of_nfts(driver, nft_amount)
    click_btn('button.css-13irzvu', driver)  # Нажатие на кнопку покупки
    click_btn('button.css-d8znws', driver=driver)  # Нажатие на кнопку подтверждения покупки

    input('Нажмите Enter для завершения работы программы')


if __name__ == '__main__':
    with open('data/personal_key.txt', 'r') as f:
        key = f.read()
    if key:
        r = requests.get(f'https://snkrs.na4u.ru/{key.strip()}:binance_nft_bot')
        if r.text == 'yes':
            main()
        else:
            input('Проверьте правильность введеного ключа!')
    else:
        input('Добавьте персональный ключ доступа в personal_key.txt в папке data и перезапустите программу.')
