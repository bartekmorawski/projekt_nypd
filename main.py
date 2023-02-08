import argparse
import os
import pandas as pd
import func
import warnings

# used if given start and end are not in common years for data sets
default_start = 1960
default_end = 2014


cwd = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("--file_NY", type=str, default=os.path.join(cwd, os.path.normpath(
    'API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv')),
                    help="Path to file with data")
parser.add_argument("--file_SP", type=str, default=os.path.join(cwd, os.path.normpath(
    'API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv')),
                    help="Path to file with data 2")
parser.add_argument("--file_co2", type=str, default=os.path.join(cwd, os.path.normpath(
    'co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv')), help="Path to file with co2 data")
parser.add_argument("--start", type=int, default=default_start, help="start year")
parser.add_argument("--end", type=int, default=default_end, help="end year")

args = parser.parse_args()

gdp = pd.read_csv(args.file_NY, skiprows=4)
population = pd.read_csv(args.file_SP, skiprows=4)
co2 = pd.read_csv(args.file_co2, skiprows=0)


# drop empty columns (in this data last ones)
gdp.dropna(how='all', axis=1, inplace=True)
population.dropna(how='all', axis=1, inplace=True)
non_year_colnames = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
common_years = set.intersection(set(co2['Year']), set(map(func.int_if_possible, gdp.columns)),
                                set(map(func.int_if_possible, population.columns)))

# without given year/given yrs not in common yrs/empty interval 1960/2014, if ok then given from parser
if args.start > args.end:
    warnings.warn('Year interval is empty, defaulted to 1960-2014')
    start = default_start
    end = default_end
else:
    start = func.yr_or_default(args.start, default_start, common_years)
    end = func.yr_or_default(args.end, default_end, common_years)

gdp_cy, population_cy, co2_cy = func.common_yrs_dfs(gdp, population, co2, non_year_colnames, common_years)
gdp_sy, population_sy, co2_sy = func.selected_yrs_dfs(start, end, gdp_cy, population_cy, co2_cy, non_year_colnames)


co2_5_yr = func.top_5_co2_by_year(co2_sy)
gdp_5_yr = func.gdp_top_5_by_year(func.gdp_pc_by_year(gdp_sy, population_sy, start, end), start, end)
co2_change = func.top_10_yr_co2_change(co2_sy, start, end)

# outputs to xlsx files
func.save_xlsx(co2_5_yr, 'top_co2.xlsx')
func.save_xlsx(gdp_5_yr, 'top_gdp.xlsx')
func.save_xlsx(co2_change, 'co2_10yr_change.xlsx')
