from collections import Counter


class first_Step:
    def __int__(self):
        self.key_to_sort = {}
    def HotEnd(self,downloaded_Data):
        helper = []
        for x in downloaded_Data:
            x = x.split(",")
            x = [word.strip() for word in x]
            x = sorted(x)
            helper.append(x)
        return helper
    def count_sort(self,dataSet,minSupport):
        # Inicjalizujemy licznik słów
        word_counter = Counter()

        # Przechodzimy przez listy i zliczamy słowa
        for list in dataSet:
            for word in list:
                word_counter[word.strip()] += 1

        sorted_dataSet = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)
        result = {}
        for data in sorted_dataSet:
            if(data[1] >= minSupport):
               result[data[0]]= data[1]
        return result
    def proper_ordered_data_set(self,dataSet,helper_Data):
        #TODO: Jesli ta sama czestotliwosc to trzeba ustalic alfabetycznie
        z = []
        for sublist in dataSet:
            filteredSubList = []
            for x in sublist:
                if x in helper_Data: filteredSubList.append(x)
            z.append(sorted(filteredSubList, key=lambda letter: -helper_Data.get(letter, 0)))
        return z
    def prepareData(self,dataSet):
        dataSet = self.HotEnd(dataSet)
        helper_Data = self.count_sort(dataSet, 3)
        self.key_to_sort = helper_Data
        return self.proper_ordered_data_set(dataSet, helper_Data)

    dataSet = ["Edk, Kak, Mon, Niva, Odo ,Yka","Dik, Edk, Kak, Niva, Odo, Yka", "Abw, Edk, Kak, Mon", "Chj, Kak, Mon, Ubk, Yka","Chj, Edk, Ichj, Kak, Odo ,Odo"]
