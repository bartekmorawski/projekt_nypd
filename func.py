import pandas as pd
import numpy as np
import os

cwd=os.getcwd()

file_NY=os.path.join(cwd, os.path.normpath('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'))
file_SP=os.path.join(cwd, os.path.normpath('API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'))
file_co2=os.path.join(cwd, os.path.normpath('co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv'))

gdp = pd.read_csv(file_NY, skiprows=3)
population = pd.read_csv(file_SP, skiprows=3)
co2 = pd.read_csv(file_co2)

def int_if_possible(input_str):
    try:
        return int(input_str)
    except ValueError:
        return None

gdp.dropna(how='all', axis=1, inplace=True)
population.dropna(how='all', axis=1, inplace=True)

common_years = set(np.unique(co2.Year)) & set(map(int_if_possible, gdp.columns)) & set(map(int_if_possible, population.columns))




