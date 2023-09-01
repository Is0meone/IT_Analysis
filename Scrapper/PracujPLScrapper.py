import requests
from bs4 import BeautifulSoup
from DataStore import CSVWritter
from Job import Job


def makeSalaryUnify(salaryForHour):
    coreSalary = salaryForHour.split(' ')[0]
    if "–" in coreSalary:
        lowerCase = coreSalary.split('–')[0]
        upperCase = coreSalary.split('–')[1]
        upperCase = upperCase[:-3]
        lowerCase = int(lowerCase)*160
        upperCase = int(upperCase)*160
        lowerCase = str(lowerCase) + " "
    else:
        lowerCase = ""
        upperCase = coreSalary
        upperCase = upperCase[:-3]
        upperCase = int(upperCase)*160
    return lowerCase + str(upperCase)
def getAdditionalData(link, levelSpec,technologies,optTechnologies):
    internalPage = requests.get(link)
    soup = BeautifulSoup(internalPage.content, "html.parser")
    levelSpecQ = soup.find("div", attrs={"data-scroll-id":"position-levels"})
    if levelSpecQ is not None:
        # TODO: Make it realize that it is the same levelSpec and do not return its value by func
        levelSpec = levelSpecQ.text
        if "Mid" in levelSpec:
            levelSpec = "Mid"
        elif "Senior" in levelSpec:
            levelSpec = "Senior"
        elif "Junior" in levelSpec:
            levelSpec = "Junior"


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
    return levelSpec
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
        levelSpec = ""
        technologies = []
        optTechnologies = []

        linkURL = link["href"]
        if salary is None:
            salaryFinal = "-"
        else:
            salary = salary.text
            if salary.endswith("godz."):
                print(linkURL)
                salaryFinal = makeSalaryUnify(salary)
            else:
                salaryFinal = ''.join(salary.split(' ')[0:3]).replace("–"," ")
                print("Kurwa salaarty hest "+ salary+"\n")

        # collection additional data very primitive return of levelSpec!!!
        levelSpec = getAdditionalData(linkURL, levelSpec, technologies, optTechnologies)

        jobsList.append(Job(position, company, salaryFinal, levelSpec, technologies, optTechnologies))
        print(position + "\n" + company + "\n" + salaryFinal + "\n")
        i = i + 1
        #Here to scrape whole page
        #if (i == 3): break

    for job in jobsList:
        print(job)

jobsList = []

#TODO: Multiple ideas to start and iterate pages! For now just couple pages
for i in range(1,6):
    link = "https://www.pracuj.pl/praca?cc=5015%2C5016&pn=" + str(i)
    pageScrapper(link,jobsList)
CSVWritter.write(jobsList)