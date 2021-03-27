# https://www.codementor.io/@dankhan/web-scrapping-using-python-and-beautifulsoup-o3hxadit4

import os
from _datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.dates import DateFormatter
import seaborn as sns
import pandas as pd


# TODO lots of stuff
cwd = os.getcwd()
cwdParent = os.path.abspath('..')
cwdGParent = os.path.abspath('../..')


# https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
dateTimeObj = datetime.now()
stamp = str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day)
imagestamp = str(dateTimeObj.year) + str(dateTimeObj.month) + str(dateTimeObj.day)
data_filename = os.path.join(cwdParent, 'Rank_Data.csv')
img_filename = os.path.join(cwdParent, 'graphimages', 'rank' + imagestamp + '.png')

df = pd.read_csv(data_filename, index_col='Date', parse_dates=True)
print(df.tail())
# print(df)
ax = df.plot()
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
# plt.ylim(0, 51)
# myFmt = DateFormatter("%m")
# ax.xaxis.set_major_formatter(myFmt)
# TODO I need to dynamically identify the top ten players and add those.
plt.legend(['Alex Kohanim', 'Jacob Lee', 'Trevor Dolin', 'Gina McCaffrey', 'Austin Keil', 'Cardiac Mangoes', 'Patrick J Maher', 'AO', 'Juan Estrada', 'Selah Argent'])
plt.gca().invert_yaxis()
plt.title("Ranks as of " + stamp)
plt.savefig(img_filename)
plt.show()


