import numpy as np
import pandas as pd
import os

cwd = os.getcwd()
cwdParent = os.path.abspath('..')
cwdGParent = os.path.abspath('../..')

rank_Data_filename = os.path.join(cwdParent, 'Rank_Data.csv')
score_Data_filename = os.path.join(cwdParent, 'Score_Data.csv')

rankDF = pd.read_csv(rank_Data_filename, index_col='Date', parse_dates=True)
for col_name, item in rankDF.iteritems():
    rankDF[col_name] = rankDF[col_name].astype('Int64')
        # rankDF[col_name] = rankDF[col_name].astype('Int64')

scoreDF = pd.read_csv(score_Data_filename, index_col='Date', parse_dates=True)

# https://towardsdatascience.com/pretty-displaying-tricks-for-columnar-data-in-python-2fe3b3ed9b83
pd.options.display.max_columns = None
pd.options.display.width=None
print(rankDF)
print(scoreDF)
# print(rankDF.iloc[0:10, 0:10])
# print(scoreDF.iloc[0:10, 0:10])


