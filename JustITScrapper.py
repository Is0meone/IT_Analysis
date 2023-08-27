from selenium import webdriver
from bs4 import BeautifulSoup

def getHTML(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.implicitly_wait(20)
    page_source = driver.page_source
    driver.quit()
    return page_source
def extractLinks(URL):
    soup = BeautifulSoup(getHTML(URL), "html.parser")
    # Znalezienie wszystkich linków o klasie "jss840 jss1033"
    resultsBox = soup.find("div",class_="css-110u7ph")
    results = resultsBox.find_all("a")

    # Wyświetlenie liczby znalezionych linków
    #print(resultsBox.prettify())
    linkArray = []
    # Przetworzenie znalezionych linków
    for link in results:
        href = link.get("href")
        hrefFinal = "https://justjoin.it"+str(href)
        linkArray.append(hrefFinal)
    print(linkArray)
    return linkArray

URL = "https://justjoin.it/?tab=with-salary"
linkBox = extractLinks(URL)
