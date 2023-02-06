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


def int_if_possible(input_str):
    try:
        return int(input_str)
    except ValueError:
        return None


gdp.dropna(how='all', axis=1, inplace=True)
population.dropna(how='all', axis=1, inplace=True)
non_year_colnames = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
common_years = set.intersection(set(co2['Year']), set(map(int_if_possible, gdp.columns)),
                                set(map(int_if_possible, population.columns)))

start = 1970
end = 2000


# common_years = list(map(str, common_years))
# print(gdp[non_year_colnames + list(map(str, common_years))])
# print(population[non_year_colnames + list(map(str, common_years))])
# print(co2.loc[co2['Year'].isin(common_years)])

# Common Years dataframes
def common_yrs_dfs(gdp, population, co2):
    gdp_cy = gdp[non_year_colnames + list(map(str, common_years))]
    population_cy = population[non_year_colnames + list(map(str, common_years))]
    co2_cy = co2.loc[co2['Year'].isin(common_years)]
    return gdp_cy, population_cy, co2_cy


gdp_cy, population_cy, co2_cy = common_yrs_dfs(gdp, population, co2)


# common and Selected Years dataframes
def selected_yrs_dfs(start, end, gdp, population, co2):
    gdp_sy = gdp[non_year_colnames + list(map(str, range(start, end + 1)))]
    population_sy = population[non_year_colnames + list(map(str, range(start, end + 1)))]
    co2_sy = co2.loc[co2['Year'].isin(range(start, end + 1))]
    return gdp_sy, population_sy, co2_sy


gdp_sy, population_sy, co2_sy = selected_yrs_dfs(start, end, gdp_cy, population_cy, co2_cy)


def is_top(year, pc, idx_most):
    if pc >= idx_most.at[year, 'fifth_max']:
        return 1
    else:
        return 0


def fifth_max(x):
    return x.nlargest(5).min()


def top_5_co2_by_year(co2):
    pc_5_value_by_year = co2.groupby(['Year']).agg({'Per Capita': [fifth_max]})
    pc_5_value_by_year.columns = pc_5_value_by_year.columns.droplevel(0)
    idx_top5 = [is_top(year, pc, pc_5_value_by_year) for year, pc in zip(co2['Year'], co2['Per Capita'])]
    top5_by_year = co2[np.array(idx_top5, dtype=bool)][['Year', 'Country', 'Per Capita', 'Total']] \
        .reset_index(drop=True)
    return top5_by_year


x = top_5_co2_by_year(co2_sy)


# print(x)


def gdp_by_year(gdp, population, start, end):
    str_years = list(map(str, list(range(start, end + 1)))) # list of strings of considered years
    a = pd.merge(gdp, population, on='Country Name') # gdp and population with columns _x with gdp, _y with population
    year_merge_cols = ['Country Name'] + [yr + '_x' for yr in str_years] + [yr + '_y' for yr in str_years]
    gdp_pop = a[year_merge_cols] # selected columns
    for yr in str_years: # adds new columns with gdp per capita for each year
        gdp_pop2 = gdp_pop.copy()
        gdp_pop2[yr + '_pc'] = gdp_pop[yr + '_x'] / gdp_pop[yr + '_y']
        gdp_pop = gdp_pop2
    year_pc_cols = ['Country Name'] + [yr + '_x' for yr in str_years] + [yr + '_pc' for yr in str_years]
    gdp_top_5 = pd.DataFrame(columns = ['Year', 'Country Name', 'gdp_pc', 'gdp']) # empty df with expected columns
    for yr in str_years:
        gdp_top_year = gdp_pop[year_pc_cols].nlargest(5, yr + '_pc') # 5 rows with top5 gdp per capita for year yr
        gdp_top_year['Year'] = yr # new column
        gdp_to_add = gdp_top_year[['Year', 'Country Name', yr + '_pc', yr + '_x']]. \
            rename(columns = {yr + '_pc': 'gdp_pc', yr + '_x': 'gdp' }, inplace = False) # select and rename columns
        gdp_top_5 = pd.concat([gdp_top_5, gdp_to_add]) # add results for year yr
    return gdp_top_5


# print(a)
# _x - gdp, _y - population

# col_triples = [[yr, yr + '_x', yr + '_y'] for yr in str_years]



b = gdp_by_year(gdp_sy, population_sy, 1970, 2000)
print("ok")
