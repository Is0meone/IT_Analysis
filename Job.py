class Job:
    def __init__(self, position, company, salary,level,usedTechnologies):
        self.position = position
        self.company = company
        self.salary = salary
        self.level = level if level is not None else []
        self.usedTechnologies = usedTechnologies if usedTechnologies is not None else []

    def addInfo(self,level,usedTechnologies):
        self.level = level if level is not None else []
        self.usedTechnologies = usedTechnologies if usedTechnologies is not None else []

    def __str__(self):
        return f"Position: {self.position}\nCompany: {self.company}\nSalary: {self.salary}\nLevel Spec: {self.level}\nTechnologies: {', '.join(self.usedTechnologies)}"
