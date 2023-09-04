import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
from Analysis import Stat_Box

def HotEnd(downloaded_Data):
    helper =[]
    for x in downloaded_Data:
        y = []
        x = x.split(",")
        for w in x:
            y.append(w)
        helper.append(x)
    return helper
def selectData(lookedFor,dataSet):
    selected_Data = []
    for x in dataSet:
        for tech in lookedFor:
            if tech in x:
                selected_Data.append(x)
    return selected_Data

selected_Data = []
dataSet =[]
downloaded_Data = Stat_Box.pretify()
dataSet = HotEnd(downloaded_Data)

lookedFor = ['.NET', 'Android', 'Git', 'REST API','SQL']
selected_Data = selectData(lookedFor,dataSet)

print(selected_Data)


te = TransactionEncoder()
te_ary = te.fit(selected_Data).transform(selected_Data)
df = pd.DataFrame(te_ary, columns=te.columns_)

print(df)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

frequent_items = fpgrowth(df, min_support=0.05, use_colnames=True)
print(frequent_items)
association_rules_df=association_rules(frequent_items, metric="confidence", min_threshold=.10)

print("The association rules are:")
print(association_rules_df.head())