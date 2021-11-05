from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chrome_options
import time


def get_options():
    options = chrome_options
    return options


def main():
    url = str(input('Введите ссылку на mint: '))
    if url.find('binance') != -1:
        driver = webdriver.Chrome()
        driver.get(url)
        try:
            accept_terms_button = driver.find_element(value='button.css-1mtehst', by='css selector')
            accept_terms_button.click()
            time.sleep(0.2)
        except Exception:
            print('accept terms button is not found')
            raise Exception

        try:
            mint_button = driver.find_element(value='button.css-18fem9b', by='css selector')
            mint_button.click()
        except Exception:
            print('mint button is not found')
            raise Exception
    else:
        print('Ссылка не является ссылкой на сайт Binance!')

    input('Нажмите Enter для завершения работы программы')


if __name__ == '__main__':
    main()
