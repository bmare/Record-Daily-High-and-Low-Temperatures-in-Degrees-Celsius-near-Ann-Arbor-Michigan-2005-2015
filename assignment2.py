#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('2004_2015_Ann_Arbor_weather.csv')

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Filter leap days
df = df[~((df.Date.dt.month == 2) & (df.Date.dt.day == 29))]

# Unpack Datetimes into Three Columns to Ease Grouping
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
df['day'] = df['Date'].dt.day

# Separate ten year period and 2015
mask = (df['Date'] < '2015-01-01')
ten_year = df.loc[mask]
p_2015 = df.loc[~mask]

# Group max and min values for periods by day
ten_year_max = pd.DataFrame(ten_year.groupby(['month','day'])['Data_Value'].max())
ten_year_max['365'] = range(1, len(ten_year_max)+1)

ten_year_min = pd.DataFrame(ten_year.groupby(['month','day'])['Data_Value'].min())
ten_year_min['365'] = range(1, len(ten_year_min)+1)

max_2015 = pd.DataFrame(p_2015.groupby(['month','day'])['Data_Value'].max())
max_2015['365'] = range(1, len(max_2015)+1)

min_2015 = pd.DataFrame(p_2015.groupby(['month','day'])['Data_Value'].min())
min_2015['365'] = range(1, len(min_2015)+1)

#Get 2015 Record Breaking Max and Mins
max_break = max_2015.loc[max_2015['Data_Value'] > ten_year_max['Data_Value']]
min_break = min_2015.loc[min_2015['Data_Value'] < ten_year_min['Data_Value']]

fig = plt.figure()
plt.title('Record Daily High and Low Temperatures in Degrees Celsius near Ann Arbor, Michigan, 2005-2015')

plt.margins(x=0)

# 2015 Record Highs and Lows
high_2015 = plt.scatter(max_break['365'], max_break['Data_Value'], \
                        color='darkred', label='2015 Record Breaking High')
low_2015 = plt.scatter(min_break['365'], min_break['Data_Value'], \
                       color='steelblue', label='2015 Record Breaking Low')

# 2005-2014 Record Highs and Lows
high_ten_year = plt.plot(ten_year_max['365'], ten_year_max['Data_Value'], \
                         color='lightcoral', label='2005-14 Record High', alpha=0.75)
low_ten_year = plt.plot(ten_year_min['365'], ten_year_min['Data_Value'], \
                        color='paleturquoise', label='2005-14 Record Low',alpha=0.75)

ax = plt.gca()


plt.fill_between(ten_year_max['365'], ten_year_max['Data_Value'], ten_year_min['Data_Value'], color='gainsboro', alpha=0.4)

#Adjust xticks and labels to months
month_start_365 = [1,32,61,92,122,153,183,214,245,275,306,336]
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec'] 
ax.set_xticks(month_start_365)
ax.set_xticklabels(month_names)

# Set y labels to intervals of 10, remove ticks
ax.set_yticks([-300, -200, -100, 0, 100, 200, 300, 400])
ax.set_yticklabels([-30, -20, -10, 0, 10, 20, 30, 40])

plt.tick_params(top='off', bottom='on', left='off', right='off')

for spine in ['right', 'top']:
    ax.spines[spine].set_visible(False)
    
    
plt.legend(bbox_to_anchor=(1.1,.65))
plt.savefig('Assignment2.png')
plt.show()

