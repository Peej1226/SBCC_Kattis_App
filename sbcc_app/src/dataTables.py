import numpy as np
import pandas as pd
import os
import datetime

cwd = os.getcwd()
cwdParent = os.path.abspath('..')
cwdGParent = os.path.abspath('../..')

rank_Data_filename = os.path.join(cwdParent, 'Rank_Data.csv')
score_Data_filename = os.path.join(cwdParent, 'Score_Data.csv')

rankDF = pd.read_csv(rank_Data_filename, index_col='Date', parse_dates=True)
# I cannot get .round() to work if I've already converted some of the DF series to Int64
rankDF2 = rankDF.resample('W').mean().round()
for col_name, item in rankDF.iteritems():
    rankDF[col_name] = rankDF[col_name].astype('Int64')
rankDF3 = rankDF.iloc[[0, -1]].fillna(51)


scoreDF = pd.read_csv(score_Data_filename, index_col='Date', parse_dates=True)
scoreDF2 = scoreDF.resample('W').mean().round()
scoreDF3 = scoreDF.iloc[[0, -1]].fillna(0)


# https://towardsdatascience.com/pretty-displaying-tricks-for-columnar-data-in-python-2fe3b3ed9b83
pd.options.display.max_columns = None
pd.options.display.width = None

# all data
print(rankDF)
print(scoreDF)

# weekly averages
print(rankDF2)
print(scoreDF2)

# top and bottom
# print(rankDF3)
# print(scoreDF3)


def getTopFive(df, choice):
    diffTopBottom_list = [round(x, 1) for x in df.diff().values.tolist()[1]]
    diffsSubDF = pd.Series(diffTopBottom_list, index=list(df.columns))
    if choice == "Rank":
        top5Change = list(diffsSubDF.nsmallest().keys())
    else:
        top5Change = list(diffsSubDF.nlargest().keys())
    return top5Change


top5scoreChange = getTopFive(scoreDF3, "Score")
top5rankChange = getTopFive(rankDF3, "Rank")


# print(scoreDF3.diff().iloc[[-1]])
# print()
# print(list(scoreDF3.columns))
# print([round(x, 1) for x in scoreDF3.diff().values.tolist()[1]])

print(rankDF.max().max())
print('score ', top5scoreChange)
print('rank ', top5rankChange)

