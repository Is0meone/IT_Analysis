import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://nofluffjobs.com/pl/job/remote-mid-senior-automation-qa-matrix-global-services")
driver.maximize_window()
try:
    position = driver.find_element(By.TAG_NAME, "h1").text
    company = driver.find_element(By.ID, "postingCompanyUrl").text
    exp = driver.find_element(By.XPATH, """//*[@id="posting-seniority"]/div[1]/span""").text
    salary = driver.find_element(By.TAG_NAME, "h4").text
    tech
    optTech
    print(company)
    print(position +"\n"+ company +"\n"+exp+"\n"+ salary)

finally:
    driver.quit()
