import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

@pytest.fixture
def driver():
    chrome_options = Options()
    service = Service('C:/xampp/htdocs/Phpcode/eCommerceSite-PHP/drivers/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get('http://localhost/Phpcode/eCommerceSite-PHP')
    yield driver
    driver.quit()