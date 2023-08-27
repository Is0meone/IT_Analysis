from selenium import webdriver
from bs4 import BeautifulSoup

def getHTML(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.implicitly_wait(20)
    page_source = driver.page_source
    driver.quit()
    return page_source
def extractLinks(URL):     #TODO: przewijanie strony ciężka rzecz
    soup = BeautifulSoup(getHTML(URL), "html.parser")
    resultsBox = soup.find("div",class_="css-110u7ph")
    results = resultsBox.find_all("a")
    linkArray = []
    for index in range(3, len(results)):
        link = results[index]
        href = link.get("href")
        hrefFinal = "https://justjoin.it" + str(href)
        linkArray.append(hrefFinal)

    print(linkArray)
    return linkArray
def getInfo(link):
    soup = BeautifulSoup(getHTML(link), "html.parser")
    position = soup.find("div",class_="css-1id4k1").text
    resultsBox = soup.find("div",class_="css-1ikoimk")
    technologyBox = resultsBox.find_all("div", class_="css-1q98d5e")
    for field in technologyBox:
        tech = field.find("div", class_="css-1eroaug").text
        level = field.find("div", class_="css-19mz16e").text
        print(position+" "+ tech + " " + level)


URL = "https://justjoin.it"
linkBox = extractLinks(URL)

for link in linkBox:
    print(link)
    getInfo(link)
    break
