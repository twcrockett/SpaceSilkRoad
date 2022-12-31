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

for i, sat in enumerate(sats_all['Country of Contractor']):
    c_list = str(sat).strip().split('/')
    sats_all.at[i, 'Country of Contractor'] = c_list

# print(sats_all['Country of Contractor'])

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

X = sats_ctr['Date of Launch']
y = sats_ctr['Percent Global North contractor']


# Let's look at average percent of Global North contractor by decade of launch.

df_1990 = sats_ctr[(sats_ctr['Date of Launch'].dt.year >= 1990) & (sats_ctr['Date of Launch'].dt.year < 2000)]
av_1990 = df_1990['Percent Global North contractor'].mean()

df_2000 = sats_ctr[(sats_ctr['Date of Launch'].dt.year >= 2000) & (sats_ctr['Date of Launch'].dt.year < 2010)]
av_2000 = df_2000['Percent Global North contractor'].mean()

df_2010 = sats_ctr[(sats_ctr['Date of Launch'].dt.year >= 2010) & (sats_ctr['Date of Launch'].dt.year < 2020)]
av_2010 = df_2010['Percent Global North contractor'].mean()

print(f'Around {av_1990.round(2):.0%} of contractors responsible for current satellites launched in the 1990s represent '
      f'the Global North, as compared to {av_2000.round(2):.0%} in the 2000s decade and {av_2010.round(2):.0%} in the '
      f'2010s.')


# Counting iterations of satellite involvement per country using contractors

contractor_ct = {}

for row in sats_ctr['Country of Contractor']:
    for country in row:
        if country not in contractor_ct.keys():
            contractor_ct[country] = 1
        else:
            contractor_ct[country] += 1

print(contractor_ct)


