from collections import Counter
def HotEnd(downloaded_Data):
    helper =[]
    for x in downloaded_Data:
        y = []
        x = x.split(",")
        for w in x:
            y.append(w)
        helper.append(x)
    return helper
def count_sort(dataSet,minSupport):
    # Inicjalizujemy licznik słów
    word_counter = Counter()

    # Przechodzimy przez listy i zliczamy słowa
    for list in dataSet:
        for word in list:
            word_counter[word.strip()] += 1

    sorted_dataSet = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
    result = []
    for data in sorted_dataSet:
        if(data[1] >= minSupport):
           result.append(data)
    return result
def proper_ordered_data_set(dataSet,helper_Data):
    #TODO: Optimalise this
    for list in dataSet:
        for counterX, x in enumerate(helper_Data,start=0):
            for counterWord,word in enumerate(list,start=0):
                print(str(counterX) +""+ str(counterWord))


dataSet = ["Edk, Kak, Mon, Niva, Odo ,Yka","Dik, Edk, Kak, Niva, Odo, Yka", "Abw, Edk, Kak, Mon", "Chj, Kak, Mon, Ubk, Yka","Chj, Edk, Ichj, Kak, Odo ,Odo"]
datatwo = ["C# 11, .NET 7, PostgreSQL, Redis, Kafka, Elasticsearch, Visual Studio, Microservices, Swagger, Resharper, Rider","Linux, Docker","JavaScript, HTML, SQL, Rider","JavaScript, Node.js, React, HTML 5, CSS 3, Spring, Spring Boot, SQL, JPA","Bitbucket, Cloud, Docker, OpenShift"]
dataSet = HotEnd(dataSet)
helper_Data = count_sort(dataSet,3)
print(helper_Data)

proper_ordered_data_set(dataSet,helper_Data)
