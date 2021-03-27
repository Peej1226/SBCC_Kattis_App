import numpy as np
import pandas as pd
import os
from _datetime import datetime
import requests
from bs4 import BeautifulSoup

cwd = os.getcwd()
cwdParent = os.path.abspath('..')
cwdGParent = os.path.abspath('../..')

filename1 = os.path.join(cwdParent, 'Rank_Data.csv')
filename2 = os.path.join(cwdParent, 'Score_Data.csv')

df_rank = pd.read_csv(filename1)
df_score = pd.read_csv(filename2)

print(df_rank.iloc[0:10, 0:10])
print(df_score.iloc[0:10, 0:10])

dateTimeObj = datetime.now()
stamp = dateTimeObj.strftime('%m/%d/%y %H:%M')

page = requests.get('https://open.kattis.com/universities/sbcc.edu')
soup = BeautifulSoup(page.content, 'html.parser')
page_tables = soup.find_all('table')
for table in page_tables:
    table_rows = table.find_all('tr')

# name row[1], score row[3], rank row[0]
score_list = []
rank_list = []
top50 = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    if row:  # first row is blank so "it is falsy"
        rank_list.append(int(row[0]))
        score_list.append(row[3])
        top50.append(row[1])

for name in top50:
    if name not in df_rank.columns:
        df_rank[name] = np.nan
        # df_score[name] = np.nan

df_rank = df_rank.append(dict(zip(['Date']+top50, [stamp]+rank_list)), ignore_index=True)
df_score = df_score.append(dict(zip(['Date']+top50, [stamp]+score_list)), ignore_index=True)

df_rank.to_csv(filename1, index = False)
df_score.to_csv(filename2, index = False)
