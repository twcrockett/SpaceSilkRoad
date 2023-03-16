import pandas as pd
import matplotlib.pyplot as plt

sats_all = pd.read_excel("UCS-Satellite-Database-5-1-2022.xls", parse_dates=['Date of Launch'])

global_north_txt = open("global_north.txt", 'r')
global_north = global_north_txt.read()
country_list_txt = open("countries.txt", 'r')
country_list = country_list_txt.read()
c_list = []
c_dict = {}

# only keep necessary columns, create year of launch column
sats_all = sats_all[['Current Official Name of Satellite', 'Country of Operator/Owner',
                     'Country of Contractor', 'Date of Launch']]
sats_all['Year of Launch'] = sats_all['Date of Launch'].copy().dt.to_period('y')

# sort by date of launch
sats_all = sats_all.sort_values(by=['Date of Launch']).reset_index()

# listify countries in df, add to c_list, c_dict (country: first entry year)
for i, sat in enumerate(sats_all['Country of Operator/Owner']):
    ns = str(sat).strip().split('/')
    sats_all.at[i, 'Country of Operator/Owner'] = ns
    for n in ns:
        if n is 'US':
            n = 'United States'
        if n is 'UK':
            n = 'United Kingdom'
        if n not in c_list:
            c_list.append(n)
            c_dict[n] = sats_all.at[i, 'Year of Launch'].year

entries = pd.DataFrame.from_dict(c_dict, orient='index', columns=['Year'])
entries.index.name = "Country/Organization"

per_year = entries["Year"].value_counts().reset_index(name="New Entries").sort_values('index').set_index('index')
per_year.index.name = "Year"
per_year.plot(kind='bar')