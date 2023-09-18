import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By

from DataStore import CSVWritter


def getHTML(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.implicitly_wait(20)

    page_source = driver.page_source


    return page_source
def cleanSalary(salary):
    if salary[0:11] =="Undisclosed":
        return "-"
    else:
        salaryParts = salary.split(' ')
        firstPart = ''.join(salaryParts[:2])
        secondPart = ''.join(salaryParts[3:5])
        return firstPart + " " + secondPart
def extractLinks(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.implicitly_wait(20)

    linkArray = []

    for i in range(0, 30):
        iframe = driver.find_element(By.CLASS_NAME, "jss244")
        scroll_origin = ScrollOrigin.from_element(iframe)
        ActionChains(driver) \
            .scroll_from_origin(scroll_origin, 0, 1200 * i) \
            .perform()
        print(1200 * i)
        if i==0:
            time.sleep(30)
        time.sleep(5)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")
        resultsBox = soup.find("div",class_="css-110u7ph")
        results = resultsBox.find_all("a")
        for index in range(3, len(results)):
            link = results[index]
            href = link.get("href")
            hrefFinal = "https://justjoin.it" + str(href)
            print(hrefFinal)
            linkArray.append(hrefFinal)

    print(linkArray)
    print(len(linkArray))
    return linkArray
def getInfo(link):
    jobInfo = []

    soup = BeautifulSoup(getHTML(link), "html.parser")
    position = soup.find("div",class_="css-1id4k1").text
    company = soup.find("a",class_="css-l4opor").text
    experience = soup.find_all("div",class_="css-1ji7bvd")[1].text
    salaryInfo = soup.find("div",class_="css-1wla3xl").text
    salary = cleanSalary(salaryInfo)

    jobInfo.append(position)
    jobInfo.append(company)
    jobInfo.append(experience)
    jobInfo.append(salary)

    techDictionary = {}
    resultsBox = soup.find("div",class_="css-1ikoimk")
    technologyBox = resultsBox.find_all("div", class_="css-1q98d5e")
    for field in technologyBox:
        tech = field.find("div", class_="css-1eroaug").text
        level = field.find("div", class_="css-19mz16e").text
        techDictionary[tech] = level
    jobInfo.append(techDictionary)
    jobInfo.append('-')
    print(jobInfo)
    return jobInfo
if __name__ == "__main__":
    URL = "https://justjoin.it"
    linkBox = extractLinks(URL)

    scrappedInfo =[]
    for link in linkBox:
        scrappedInfo.append(getInfo(link))
    print(scrappedInfo)
    CSVWritter.justITWritter(scrappedInfo)
    print(len(linkBox))