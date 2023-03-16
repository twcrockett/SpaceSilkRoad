import pandas as pd

# import sats dataframe
sats_all = pd.read_excel("UCS-Satellite-Database-5-1-2022.xls", parse_dates=['Date of Launch'])

# create empty list, dict
c_list = []
# c_dict = {}
#
# listify countries in dataframe, add to c_list
# this first 'for' loop 'enumerates', assigning an index value to each row
# goal is to make sure we have a list of every country that appears
# we have to do this in case some countries are typos so they are still accounted for
for i, sat in enumerate(sats_all['Country of Contractor']):
    # separating values by slash
    ns = str(sat).strip().split('/')
    # reallocating separated countries into country column
    sats_all.at[i, 'Country of Contractor'] = ns
    # renaming abbreviated countries for clarity
    for n in ns:
        if n is 'US':
            n = 'United States'
        if n is 'UK':
            n = 'United Kingdom'
        # this adds new countries into the total country list
        if n not in c_list:
            c_list.append(n)
# redo operation for owners
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


# only keep necessary columns
sats_all = sats_all[['Country of Operator/Owner',
                     'Country of Contractor']]

print(c_list)


# create dictionary, keeps track of number of country appearances
# keys are created from c_list
count_dict = dict.fromkeys(c_list, 0)
count_dict_owner = dict.fromkeys(c_list, 0)
count_dict_contract = dict.fromkeys(c_list, 0)

# simple count process using for loop
for i, row in sats_all.iterrows():
    count_dict_add_list = []
    for country in row['Country of Operator/Owner']:
        count_dict_add_list.append(country)
        count_dict_owner[country] += 1
    for country in row['Country of Contractor']:
        if country not in count_dict_add_list:
            count_dict_add_list.append(country)
        count_dict_contract[country] += 1
    for country in count_dict_add_list:
        count_dict[country] += 1

# now we can search the dict we made!
# country_searched = 'Pakistan'
# print(count_dict[country_searched])
# print(count_dict_contract[country_searched])

count_df = pd.DataFrame.from_dict(count_dict, orient='index').sort_index()
pd.set_option('display.max_rows', None)
print(count_df)
