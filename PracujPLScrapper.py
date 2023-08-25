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
def getAdditionalData(link, levelSpec,technologies,optTechnologies):
    internalPage = requests.get(link)
    soup = BeautifulSoup(internalPage.content, "html.parser")
    levelSpecQ = soup.find("div", attrs={"data-scroll-id":"position-levels"})
    if levelSpecQ is not None:
        levelSpec = levelSpecQ.text
        print(levelSpec + "\n")

    #TODO: What if there is only optional tech?
    techBox = soup.find("div", attrs={"data-scroll-id": "technologies-1"})
    if techBox is not None:
        expectedTechSection = techBox.find("div", attrs={"data-scroll-id": "technologies-expected-1"})
        optionalTechSection = techBox.find("div", attrs={"data-scroll-id": "technologies-optional-1"})

        if expectedTechSection is not None:
            expectedTech = expectedTechSection.find_all("li", class_="offer-vieweKR6vg")
        else: expectedTech = []

        if optionalTechSection is not None:
            optionalTech = optionalTechSection.find_all("li", class_="offer-vieweKR6vg")
        else: optionalTech = []

        for tech in expectedTech:
            technologies.append(tech.text.strip())
        for optTech in optionalTech:
            optTechnologies.append(optTech.text.strip())
    print(technologies)
    print(optTechnologies)
def pageScrapper(rootLink,jobList):
    # Soup setup
    URL = rootLink
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # HTML search
    results = soup.find("div", attrs={"data-test": "section-offers"})
    jobOfferts = results.find_all("div", class_="listing_c1dc6in8")


    i = 0
    for job in jobOfferts:
        position = job.find("h2", attrs={"data-test": "offer-title"}).text.strip()
        company = job.find("h4", class_="listing_eiims5z size-caption listing_t1rst47b").text.strip()
        salary = job.find("span", attrs={"data-test": "offer-salary"})
        link = job.find("a", class_="listing_n194fgoq")
        levelSpec = str
        technologies = []
        optTechnologies = []

        linkURL = link["href"]
        if salary is None:
            salary = "No data about salary"
        else:
            salary = salary.text
            if salary.endswith("godz."):
                salary = makeSalaryUnify(salary)

        # collection additional data
        getAdditionalData(linkURL, levelSpec, technologies, optTechnologies)

        jobsList.append(Job(position, company, salary, levelSpec, technologies, optTechnologies))
        print(position + "\n" + company + "\n" + salary + "\n")
        i = i + 1
        if (i == 3): break

    for job in jobsList:
        print(job)

jobsList = []

#TODO: Multiple ideas to start and iterate pages!
for i in range(1,3):
    link = "https://www.pracuj.pl/praca?cc=5015%2C5016&pn=" + str(i)
    pageScrapper(link,jobsList)
CSVWritter.basicWrite(jobsList)