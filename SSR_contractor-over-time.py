import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
# from fastai.tabular.all import *
from datetime import datetime as dt
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression as LinReg

sats_all = pd.read_excel("UCS-Satellite-Database-5-1-2022.xls", parse_dates=['Date of Launch'])

global_north_txt = open("global_north.txt", 'r')
global_north = global_north_txt.read()

# listify countries in df
for i, sat in enumerate(sats_all['Country of Contractor']):
    c_list = str(sat).strip().split('/')
    sats_all.at[i, 'Country of Contractor'] = c_list

sats_ctr = sats_all[['Current Official Name of Satellite', 'Date of Launch', 'Country of Contractor']]

cols = ['Current Official Name of Satellite', 'Date of Launch', 'Country of Contractor']


def global_north_check(row):
    total = len(row)
    n_count = 0
    for country in row:
        if country in global_north:
            n_count += 1
    prop = n_count / total
    if "International" in row:
        prop = 0.5
    return prop


sats_ctr['Percent Global North contractor'] = \
    sats_ctr.apply(lambda row: global_north_check(row['Country of Contractor']), axis=1)

sats_ctr.plot.scatter(x='Date of Launch', y='Percent Global North contractor')

# X = sats_ctr['Date of Launch']
# y = sats_ctr['Percent Global North contractor']

# Let's look at average percent of Global North contractor by decade of launch.

df_c1990 = sats_ctr[(sats_ctr['Date of Launch'].dt.year >= 1990) & (sats_ctr['Date of Launch'].dt.year < 2000)]
av_c1990 = df_c1990['Percent Global North contractor'].mean()

df_c2000 = sats_ctr[(sats_ctr['Date of Launch'].dt.year >= 2000) & (sats_ctr['Date of Launch'].dt.year < 2010)]
av_c2000 = df_c2000['Percent Global North contractor'].mean()

df_c2010 = sats_ctr[(sats_ctr['Date of Launch'].dt.year >= 2010) & (sats_ctr['Date of Launch'].dt.year < 2020)]
av_c2010 = df_c2010['Percent Global North contractor'].mean()

print(
    f'Around {av_c1990.round(2):.0%} of contractors responsible for current satellites launched in the 1990s represent '
    f'the Global North, as compared to {av_c2000.round(2):.0%} in the 2000s decade and {av_c2010.round(2):.0%} in the '
    f'2010s.')

# Counting total iterations of satellite involvement per country using contractors

contractor_ct = {}

for row in sats_ctr['Country of Contractor']:
    for country in row:
        if country not in contractor_ct.keys():
            contractor_ct[country] = 1
        else:
            contractor_ct[country] += 1

# print(contractor_ct)

tot_ctr = pd.DataFrame.from_dict(contractor_ct, orient='index').sort_values(by=0, ascending=False) \
    .rename(columns={0: 'Number of contracted satellites'})
print(tot_ctr)

# tot_ctr.head(10).plot.bar(y='Number of contracted satellites', use_index=True)

#
# Now repeat with country operators

for i, sat in enumerate(sats_all['Country of Operator/Owner']):
    c_list = str(sat).strip().split('/')
    sats_all.at[i, 'Country of Operator/Owner'] = c_list

sats_op = sats_all[['Current Official Name of Satellite', 'Date of Launch', 'Country of Operator/Owner']]

cols = ['Current Official Name of Satellite', 'Date of Launch', 'Country of Operator/Owner']

sats_op['Percent Global North operator'] = \
    sats_op.apply(lambda row: global_north_check(row['Country of Operator/Owner']), axis=1)

sats_op.plot.scatter(x='Date of Launch', y='Percent Global North operator')

df_o1990 = sats_op[(sats_op['Date of Launch'].dt.year >= 1990) & (sats_op['Date of Launch'].dt.year < 2000)]
av_o1990 = df_o1990['Percent Global North operator'].mean()

df_o2000 = sats_op[(sats_op['Date of Launch'].dt.year >= 2000) & (sats_op['Date of Launch'].dt.year < 2010)]
av_o2000 = df_o2000['Percent Global North operator'].mean()

df_o2010 = sats_op[(sats_op['Date of Launch'].dt.year >= 2010) & (sats_op['Date of Launch'].dt.year < 2020)]
av_o2010 = df_o2010['Percent Global North operator'].mean()

print(
    f'Around {av_o1990.round(2):.0%} of operators responsible for current satellites launched in the 1990s represent '
    f'the Global North, as compared to {av_o2000.round(2):.0%} in the 2000s decade and {av_o2010.round(2):.0%} in the '
    f'2010s.')

# Counting total iterations of satellite involvement per country using operators

operator_ct = {}

for row in sats_op['Country of Operator/Owner']:
    for country in row:
        if country not in operator_ct.keys():
            operator_ct[country] = 1
        else:
            operator_ct[country] += 1

#
# This time, we can look at operators and contractors together

tot_op = pd.DataFrame.from_dict(operator_ct, orient='index').rename(columns={0: 'Number of operated satellites'})
tot = pd.DataFrame.join(tot_ctr, tot_op)
tot['Mean iterations'] = \
    tot.apply(lambda row: (row['Number of contracted satellites'] + row['Number of operated satellites'])/2, axis=1)
tot.sort_values(by='Mean iterations', ascending=False)

tot.head(5).plot.bar(y=['Number of contracted satellites', 'Number of operated satellites'],use_index=True)
tot.iloc[5:15].plot.bar(y=['Number of contracted satellites', 'Number of operated satellites'],use_index=True)

# double bar chart with north south stacked over time
# aggregate by month
# event count model
# poisson distribution (prevalence of zeroes in each month)
# *** not normally distributed
# negative binomial o\also an option
# aggregate by month then test models

# duration model: check disance between each launch
# check for landmarks (shifts) in data over time (e.g. Xi, Obama admins)
