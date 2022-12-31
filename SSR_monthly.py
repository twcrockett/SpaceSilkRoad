import pandas as pd
import matplotlib.pyplot as plt

sats_all = pd.read_excel("UCS-Satellite-Database-5-1-2022.xls", parse_dates=['Date of Launch'])

global_north_txt = open("global_north.txt", 'r')
global_north = global_north_txt.read()
country_list_txt = open("countries.txt", 'r')
country_list = country_list_txt.read()
c_list = []
c_dict = {}

# listify countries in df, add to c_list
for i, sat in enumerate(sats_all['Country of Contractor']):
    ns = str(sat).strip().split('/')
    sats_all.at[i, 'Country of Contractor'] = ns
    for n in ns:
        if n is 'US':
            n = 'United States'
        if n is 'UK':
            n = 'United Kingdom'
        if n not in c_list:
            c_list.append(n)
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

# categorize c_list countries in c_dict
for c in c_list:
    if c in global_north:
        c_dict[c] = 'N'
    elif c in country_list:
        c_dict[c] = 'S'
    else:
        c_dict[c] = 'o'


# only keep necessary columns, create month of launch column
sats_all = sats_all[['Current Official Name of Satellite', 'Country of Operator/Owner',
                     'Country of Contractor', 'Date of Launch']]
sats_all['Month of Launch'] = sats_all['Date of Launch'].copy().dt.to_period('m')
sats_all['Year of Launch'] = sats_all['Date of Launch'].copy().dt.to_period('y')

# create south involvement column
def region_check(row):
    north = 0
    south = 0
    other = 0
    country_count = 0
    for country in row:
        country_count += 1
        if c_dict[country] == 'N':
            north += 1
        elif c_dict[country] == 'S':
            south += 1
        else:
            other += 1
    npct = north/country_count
    spct = south/country_count
    opct = other/country_count
    return npct, spct, opct


sats_all['involvement'] = \
    sats_all.apply(lambda row: region_check(row['Country of Operator/Owner']), axis=1)

sats_all[['North Involvement', 'South Involvement', 'Other Involvement']] = pd.DataFrame(sats_all.involvement.tolist(),
                                                                                         index= sats_all.index)

# group by month or year, then sum involvement by region
month_group = sats_all.groupby(['Month of Launch']).sum()
year_group = sats_all.groupby(['Year of Launch']).sum()


# month_group.to_excel("month_group.xlsx")
# sats_all.to_excel("sats_all.xlsx")

# month_group[['North Involvement', 'South Involvement', 'Other Involvement']].plot(kind='bar', stacked=True)
year_group[['North Involvement', 'South Involvement', 'Other Involvement']].plot(kind='bar', stacked=True)
