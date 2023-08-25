import csv

csv_filename = "jobData.csv"

def write(jobsList):
    with open(csv_filename, 'w',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["Position", "Company", "Salary", "Level", "Used Technologies"])

        for job in jobsList:
            csv_writer.writerow([job.position, job.company, job.salary, job.level, ', '.join(job.usedTechnologies)])

def basicWrite(jobsList):
    with open(csv_filename, 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["Position", "Used Technologies","Optional Technologies"])

        for job in jobsList:
            csv_writer.writerow([job.position,', '.join(job.usedTechnologies),', '.join(job.optionalTechnologies)])