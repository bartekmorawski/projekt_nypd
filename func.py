import pandas as pd
import os
import numpy as np

cwd = os.getcwd()

file_NY = os.path.join(cwd, os.path.normpath(
    'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'))
file_SP = os.path.join(cwd, os.path.normpath(
    'API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'))
file_co2 = os.path.join(cwd, os.path.normpath(
    'co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv'))

gdp = pd.read_csv(file_NY, skiprows=4)
population = pd.read_csv(file_SP, skiprows=4)
co2 = pd.read_csv(file_co2)

# auxiliary function to make int from strings if they are numbers
def int_if_possible(input_str):
    try:
        return int(input_str)
    except ValueError:
        return None

# drop empty columns (last), define non-year colnames for gdp and population dfs, fins years in all 3 dfs
# gdp.dropna(how='all', axis=1, inplace=True)
# population.dropna(how='all', axis=1, inplace=True)
# non_year_colnames = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
# common_years = set.intersection(set(co2['Year']), set(map(int_if_possible, gdp.columns)),
#                                 set(map(int_if_possible, population.columns)))

# default_start = 1960
# default_end = 2014
# begin = 1970
# finish = 2000

def yr_or_default(year, default, common_yrs):
    if year in common_yrs:
        return year
    else:
        return default

# start = yr_or_default(begin, default_start, common_years)
# end = yr_or_default(finish, default_end, common_years)

def save_xlsx(df, name):
    with pd.ExcelWriter(name) as writer:
        df.to_excel(writer, sheet_name=name)


# common_years = list(map(str, common_years))
# print(gdp[non_year_colnames + list(map(str, common_years))])
# print(population[non_year_colnames + list(map(str, common_years))])
# print(co2.loc[co2['Year'].isin(common_years)])

# Common Years dataframes
def common_yrs_dfs(gdp, population, co2, non_year_colnames, common_years):
    gdp_cy = gdp[non_year_colnames + list(map(str, common_years))]
    population_cy = population[non_year_colnames + list(map(str, common_years))]
    co2_cy = co2.loc[co2['Year'].isin(common_years)]
    return gdp_cy, population_cy, co2_cy


# gdp_cy, population_cy, co2_cy = common_yrs_dfs(gdp, population, co2)


# common and Selected Years dataframes
def selected_yrs_dfs(start, end, gdp, population, co2, non_year_colnames):
    gdp_sy = gdp[non_year_colnames + list(map(str, range(start, end + 1)))]
    population_sy = population[non_year_colnames + list(map(str, range(start, end + 1)))]
    co2_sy = co2.loc[co2['Year'].isin(range(start, end + 1))]
    return gdp_sy, population_sy, co2_sy


# gdp_sy, population_sy, co2_sy = selected_yrs_dfs(start, end, gdp_cy, population_cy, co2_cy)

# auxiliary function
def is_top(year, pc, idx_most):
    if pc >= idx_most.at[year, 'fifth_max']:
        return 1
    else:
        return 0

# auxiliary function
def fifth_max(x):
    return x.nlargest(5).min()


def top_5_co2_by_year(co2):
    pc_5_value_by_year = co2.groupby(['Year']).agg({'Per Capita': [fifth_max]}) # 5th value of co2 emission pc for yr
    pc_5_value_by_year.columns = pc_5_value_by_year.columns.droplevel(0)
    idx_top5 = [is_top(year, pc, pc_5_value_by_year) for year, pc in zip(co2['Year'], co2['Per Capita'])] # indexes
    top5_by_year = co2[np.array(idx_top5, dtype=bool)][['Year', 'Country', 'Per Capita', 'Total']] \
        .reset_index(drop=True) # select columns by names and rows with indexes
    return top5_by_year


# x = top_5_co2_by_year(co2_sy)

# df with added columns with gdp per capita for each year
def gdp_pc_by_year(gdp, population, start, end):
    str_years = list(map(str, list(range(start, end + 1)))) # list of strings of considered years
    a = pd.merge(gdp, population, on='Country Name') # gdp and population with columns _x with gdp, _y with population
    year_merge_cols = ['Country Name'] + [yr + '_x' for yr in str_years] + [yr + '_y' for yr in str_years]
    gdp_pop = a[year_merge_cols] # selected columns
    for yr in str_years: # adds new columns with gdp per capita for each year
        gdp_pop2 = gdp_pop.copy()
        gdp_pop2[yr + '_pc'] = gdp_pop[yr + '_x'] / gdp_pop[yr + '_y']
        gdp_pop = gdp_pop2
    return gdp_pop


# given df (returned by gdp_pc_by_year) find top5 for each year with expected columns
def gdp_top_5_by_year(gdp_pop, start, end):
    str_years = list(map(str, list(range(start, end + 1))))  # list of strings of considered years
    year_pc_cols = ['Country Name'] + [yr + '_x' for yr in str_years] + [yr + '_pc' for yr in str_years]
    gdp_top_5 = pd.DataFrame(columns=['Year', 'Country Name', 'gdp_pc', 'gdp'])  # empty df with expected columns
    for yr in str_years:
        gdp_top_year = gdp_pop[year_pc_cols].nlargest(5, yr + '_pc')  # 5 rows with top5 gdp per capita for year yr
        gdp_top_year['Year'] = yr  # new column
        gdp_to_add = gdp_top_year[['Year', 'Country Name', yr + '_pc', yr + '_x']]. \
            rename(columns={yr + '_pc': 'gdp_pc', yr + '_x': 'gdp'}, inplace=False)  # select and rename columns
        gdp_top_5 = pd.concat([gdp_top_5, gdp_to_add])  # add results for year yr
    return gdp_top_5

# b = gdp_top_5_by_year(gdp_pc_by_year(gdp_sy, population_sy, start, end), start, end)

# return two countires: in-/decreased co2 per capita the most (or increased the least/decreased the least)
# meant to be called with co2 with selected years
# if end < start + 10 then compare earliest possible year and end year
# start - EARLIEST YEAR of co2 (start given by parser), end - desired end year
def top_10_yr_co2_change(co2, start, end):
    start_yr = max(start, end-10)
    co2_border_yrs = co2.loc[co2['Year'].isin([start_yr, end])]
    co2_border_yrs.loc[(co2_border_yrs['Year'] == start_yr), 'Per Capita'] = -co2_border_yrs['Per Capita']
    data_num_yrs = co2_border_yrs.groupby(['Country']).size().reset_index(name='counts')
    co2_act = co2_border_yrs[co2_border_yrs['Country'].isin(list(data_num_yrs[data_num_yrs['counts'] == 2]['Country']))]
    co2_pc_change = co2_act.groupby(['Country']).agg('sum').reset_index() # absurd, but per capita column is ok
    co2_2_countries = pd.concat([co2_pc_change[co2_pc_change['Per Capita'] == co2_pc_change['Per Capita'].max()],
                                 co2_pc_change[co2_pc_change['Per Capita'] == co2_pc_change['Per Capita'].min()]])
    co2_2_renamed = co2_2_countries[['Country', 'Per Capita']]. \
            rename(columns={'Per Capita': 'co2 per capita change'}, inplace=False)
    return co2_2_renamed