import requests
from bs4 import BeautifulSoup

import CSVWritter
from Job import Job


def makeSalaryUnify(salaryForHour):
    coreSalary = salaryForHour.split(' ')[0]
    if "–" in coreSalary:
        lowerCase = coreSalary.split('–')[0]
        upperCase = coreSalary.split('–')[1]
        upperCase = upperCase[:-3]
        lowerCase = int(lowerCase)*160
        upperCase = int(upperCase)*160
        lowerCase = str(lowerCase) + "-"
    else:
        lowerCase = ""
        upperCase = upperCase[:-3]
        upperCase = int(upperCase)*160
    return lowerCase + str(upperCase)
def getAdditionalData(link,job):
    internalPage = requests.get(link)
    soup = BeautifulSoup(internalPage.content, "html.parser")
    levelSpec = soup.find("div", attrs={"data-scroll-id":"position-levels"}).text

    technologies = []
    techBox = soup.find("div", attrs={"data-scroll-id":"technologies-1"})
    expectedTech = techBox.find_all("li",class_="offer-viewjJiyAa offer-vieweKR6vg")
    for tech in expectedTech:
        technologies.append(tech.text.strip())

    job.addInfo(levelSpec,technologies)
    print(levelSpec + "\n")
    print(technologies)


URL = "https://www.pracuj.pl/praca/warszawa;wp?rd=0&cc=5015%2C5016"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("div", attrs={"data-test": "section-offers"})

quickPosition = results.find_all("h2",attrs={"data-test":"offer-title"}) # jest link!
jobOfferts =  results.find_all("div",class_ = "listing_c1dc6in8")

jobsList = []

for job in jobOfferts:
    position = job.find("h2",attrs={"data-test":"offer-title"}).text.strip()
    company = job.find("h4",class_="listing_eiims5z size-caption listing_t1rst47b").text.strip()
    salary = job.find("span", attrs={"data-test":"offer-salary"})
    link = job.find("a",class_="listing_n194fgoq")
    linkURL = link["href"]
    if salary is None:
        salary = "No data about salary"
    else:
        salary = salary.text
        if salary.endswith("godz."):
            salary = makeSalaryUnify(salary)

    jobsList.append(Job(position,company,salary,None,None))
    print(position +"\n"+ company +"\n"+ salary + "\n")
    print(linkURL)
    getAdditionalData(linkURL,job)

for job in jobsList:
    print(job)

CSVWritter.basicWrite(jobsList)