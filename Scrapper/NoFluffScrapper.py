import time

from selenium import webdriver
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from DataStore import CSVWritter


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
def cleanSalary(salary):
    salary = salary.replace(" ","")
    salary = salary[:-3]
    salary = salary.replace("–"," ")
    return salary
def makeArray(techList):
    helper = techList.split(' ')
    helper = ", ".join(helper)
    return helper
def getInfo(link):
    infoBox=[]
    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    position = driver.find_element(By.TAG_NAME, "h1").text
    company = driver.find_element(By.ID, "postingCompanyUrl").text
    exp = driver.find_element(By.XPATH, """//*[@id="posting-seniority"]/div[1]/span""").text
    salary = driver.find_element(By.TAG_NAME, "h4").text
    salary = cleanSalary(salary)

    try:
        techStack = driver.find_element(By.XPATH, """//*[@id="posting-requirements"]/section[1]/ul""").text
    except NoSuchElementException:
        techStack = ''
    techStack = makeArray(techStack)
    try:
        optTech = driver.find_element(By.XPATH, """//*[@id="posting-nice-to-have"]/ul""").text
    except NoSuchElementException:
        optTech = ''
    optTech = makeArray(optTech)

    infoBox.append(position)
    infoBox.append(company)
    infoBox.append(exp)
    infoBox.append(salary)
    infoBox.append(techStack)
    infoBox.append(optTech)

    driver.quit()
    print(infoBox)
    return infoBox


finalList = []
for x in range(1,3):
    linkBox = extractLinks("https://nofluffjobs.com/pl/backend?page="+str(x)+"&criteria=category%3Dfrontend,fullstack,mobile,embedded,testing,devops,architecture,security,gaming,artificial-intelligence,big-data,it-administrator,agile,support,erp,telecommunication")
    i = 0
    for link in linkBox:
        i = i+1
        finalList.append(getInfo(link))
        if(i==2): break

CSVWritter.justITWritter(finalList)