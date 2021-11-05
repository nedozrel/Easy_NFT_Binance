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
        time.sleep(10)
    else:
        print('Ссылка не является ссылкой на сайт Binance!')


if __name__ == '__main__':
    main()
    input('Нажмите Enter для завершения работы программы')
