def selectData(lookedFor,dataSet):
    selected_Data = []
    for x in dataSet:
        for tech in lookedFor:
            if tech in x:
                selected_Data.append(x)
    return selected_Data

lookedFor = ['C', 'DevOps', 'Python']
dataSet = [['C', ' C++', ' Linux', ' SVN', ' Yocto', ' Qt'], ['Microsoft Azure', ' Python', ' DevOps', ' CI/CD', ' GitHub'], ['.Net'], ['C#', ' VB.Net', ' Java', ' VBA']]
