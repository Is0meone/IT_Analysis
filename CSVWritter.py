import csv

csv_filename = "jobData.csv"

def write(jobsList):
    with open(csv_filename, 'a',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        if not checkHeader():
            csv_writer.writerow(["Position","Company","Experience","Salary", "Used Technologies", "Optional Technologies"])

        for job in jobsList:
            csv_writer.writerow([job.position, job.company, job.level,job.salary,', '.join(job.usedTechnologies),', '.join(job.optionalTechnologies)])
def basicWrite(jobsList):
    with open(csv_filename, 'a', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["Position","Level", "Used Technologies","Optional Technologies"])

        for job in jobsList:
            csv_writer.writerow([job.position,job.level,', '.join(job.usedTechnologies),', '.join(job.optionalTechnologies)])
def justITWritter(jobsList):
    with open(csv_filename, 'a', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        if not checkHeader():
            csv_writer.writerow(["Position","Company","Experience","Salary", "Used Technologies", "Optional Technologies"])

        for job in jobsList:
            csv_writer.writerow(
                [job[0], job[1],job[2],job[3],job[4],job[5]])
def checkHeader():
    expected_header = "Position,Company,Experience,Salary,Used Technologies,Optional Technologies\n"

    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        actual_header = csv_file.readline()

    return actual_header == expected_header
