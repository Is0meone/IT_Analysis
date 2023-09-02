import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from Analysis import Stat_Box

downloaded_Data = Stat_Box.pretify()
selected_Data = []
i = 0
for x in downloaded_Data:
    y = []
    x = x.split(",")
    for w in x:
        y.append(w)
    selected_Data.append(x)
    i = i+1

print(selected_Data)

te = TransactionEncoder()
te_ary = te.fit(selected_Data).transform(selected_Data)
df = pd.DataFrame(te_ary, columns=te.columns_)

print(df)

print(fpgrowth(df, min_support=0.05, use_colnames=True))
#sortData = Stat_Box.getStat(dataSet)
#print(sortData)

