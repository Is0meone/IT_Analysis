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
def getAdditionalData(link, levelSpec,technologies):
    internalPage = requests.get(link)
    soup = BeautifulSoup(internalPage.content, "html.parser")
    levelSpecQ = soup.find("div", attrs={"data-scroll-id":"position-levels"})
    if levelSpecQ is not None:
        levelSpec = levelSpecQ.text
        print(levelSpec + "\n")

    techBox = soup.find("div", attrs={"data-scroll-id":"technologies-1"})
    if techBox is not None:
        expectedTech = techBox.find_all("li",class_="offer-viewjJiyAa offer-vieweKR6vg")
        for tech in expectedTech:
            technologies.append(tech.text.strip())
    print(technologies)
#Soup setup
URL = "https://www.pracuj.pl/praca/warszawa;wp?rd=0&cc=5015%2C5016"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#HTML search
results = soup.find("div", attrs={"data-test": "section-offers"})
jobOfferts =  results.find_all("div",class_ = "listing_c1dc6in8")

jobsList = []
i =0
for job in jobOfferts:
    position = job.find("h2",attrs={"data-test":"offer-title"}).text.strip()
    company = job.find("h4",class_="listing_eiims5z size-caption listing_t1rst47b").text.strip()
    salary = job.find("span", attrs={"data-test":"offer-salary"})
    link = job.find("a",class_="listing_n194fgoq")
    levelSpec = str
    technologies = []
    linkURL = link["href"]
    if salary is None:
        salary = "No data about salary"
    else:
        salary = salary.text
        if salary.endswith("godz."):
            salary = makeSalaryUnify(salary)

    #collection additional data
    getAdditionalData(linkURL,levelSpec, technologies)

    jobsList.append(Job(position, company, salary, levelSpec, technologies))
    print(position + "\n" + company + "\n" + salary + "\n")
    i = i+1
    if(i==3):break

for job in jobsList:
    print(job)

CSVWritter.basicWrite(jobsList)