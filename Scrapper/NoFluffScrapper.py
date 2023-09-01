import time

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

def extractLinks(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    try:

        element = driver.find_element(By.CSS_SELECTOR, ".list-container")
        results = element.find_elements(By.CSS_SELECTOR, ".posting-list-item")
        linkBox = []
        for link in results:
            href = link.get_attribute("href")
            if href:
                print(href)
                linkBox.append(href)

    finally:
        driver.quit()
    return linkBox

linkBox = extractLinks("https://nofluffjobs.com/pl/backend?page=1&criteria=category%3Dfrontend,fullstack,mobile,embedded,testing,devops,architecture,security,gaming,artificial-intelligence,big-data,it-administrator,agile,support,erp,telecommunication")

for link in linkBox:
    print(link)
    driver = webdriver.Chrome()
    driver.get(link)
    try:
        position = driver.find_element(By.TAG_NAME, "h1").text
        company = driver.find_element(By.XPATH,"""//*[@id="posting-header"]/div[2]/div[1]/p""").text
        exp = driver.find_element(By.XPATH,"""//*[@id="posting-seniority"]/div[1]/span""").text
        salary = driver.find_element(By.TAG_NAME,"h4").text
        print(company)
        print(position + company + exp +salary)

    finally:
        driver.quit()
