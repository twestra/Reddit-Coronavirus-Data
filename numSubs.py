import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates


with open("reddit_corona_data.json") as reddata:
    dates = json.load(reddata)
 
alldates = []
numsubmissions = []
for date in dates:
    alldates.append(datetime.date.fromisoformat(date))
    numsubmissions.append(len(dates[date]))


alldates = list(reversed(alldates))
numsubmissions = list(reversed(numsubmissions))
df = pd.DataFrame({'Dates': alldates, '#Submissions': numsubmissions})
christmas = datetime.date(2019,12,25)

df = df[df['Dates'] >= christmas]


mindate = df.head(1)['Dates']
maxdate = df.tail(1)['Dates']
plt.bar(df['Dates'], df['#Submissions'], color = 'indianred')


ax = plt.gca()

ax.set_xlim(xmin = mindate, xmax = maxdate)
ax.set_ylabel('# Submissions')
ax.set_title('Number of Submissions to r/Coronavirus since 1/21')
ax.set_facecolor("whitesmoke")
ax.grid(True)
ax.set_axisbelow(True)
plt.xticks(rotation = 'vertical', fontsize = 'x-small')
plt.margins(.2)
plt.subplots_adjust(bottom=0.2)



importantdates = ["2020-01-21","2020-02-29", "2020-03-11"]

events = ['First COVID-19 Case on American Soil - (1/21)', 'First Death on American Soil - (2/29)', 'WHO Declares Novel Coronavirus to be a Pandemic - (3/11)']
# colors for the lines
colors = ['saddlebrown','forestgreen','darkslategray']

for xc,c,e in zip(importantdates,colors,events):
    plt.axvline(x=datetime.date.fromisoformat(xc), label='{}'.format(e), c=c, linewidth = 1)
plt.legend(fontsize = 'xx-small')
plt.show()


