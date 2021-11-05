from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = str(input('Введите ссылку на mint: '))
driver = webdriver.Chrome()
driver.get(url)
