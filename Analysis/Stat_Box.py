import ast
from collections import Counter

from DataStore import CSVWritter

#TODO: Nie trawi " {" musi być "{"
def pretify():
    arrayOne = CSVWritter.easyRead(r"C:\Users\stkwi\PycharmProjects\IT_Analisis\DataStore\jobData.csv")
    statBox = []
    for job in arrayOne:
        techBox = job[4]
        if techBox.startswith('{'):
            technologies_dict = ast.literal_eval(techBox)
            techBox = ', '.join(technologies_dict.keys())
            statBox.append(techBox)
        elif techBox !='':
            statBox.append(techBox)
   # print(statBox)

    return statBox
def getStat(technologies):
    all_technologies = ', '.join(technologies)
    individual_technologies = all_technologies.split(', ')
    technology_counter = Counter(individual_technologies)
    most_common_technologies = technology_counter.most_common()

    print(str(len(technology_counter))+"\n"+"Na "+ str(len(technologies))+ " ogłoszen o pracodawca wymagał znajomosci:")
    for technology, count in most_common_technologies:
        print(f"{technology}: {count} razy")
    return most_common_technologies

if __name__ == "__main__":
    techArray = pretify()
    getStat(techArray)
