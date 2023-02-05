import pandas as pd
import numpy as np
import os

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
common_years = set.intersection(set(np.unique(co2['Year'])), set(map(int_if_possible, gdp.columns)),
                                set(map(int_if_possible, population.columns)))

# common_years = list(map(str, common_years))
# print(gdp[non_year_colnames + list(map(str, common_years))])
# print(population[non_year_colnames + list(map(str, common_years))])
# print(co2.loc[co2['Year'].isin(common_years)])

# Common Years dataframes
gdp_cy = gdp[non_year_colnames + list(map(str, common_years))]
population_cy = population[non_year_colnames + list(map(str, common_years))]
co2_cy = co2.loc[co2['Year'].isin(common_years)]


# common and Selected Years dataframes
def selected_yrs_dfs(start, end):
    gdp_sy = gdp_cy[non_year_colnames + list(map(str, range(start, end + 1)))]
    population_sy = population_cy[non_year_colnames + list(map(str, range(start, end + 1)))]
    co2_sy = co2_cy.loc[co2_cy['Year'].isin(range(start, end + 1))]
    return gdp_sy, population_sy, co2_sy


gdp_sy, population_sy, co2_sy = selected_yrs_dfs(1970, 2000)
