import pandas as pd
import os

cwd=os.getcwd()

file_NY=os.path.join(cwd, os.path.normpath('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv'))
file_SP=os.path.join(cwd, os.path.normpath('API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv'))
file_co2=os.path.join(cwd, os.path.normpath('co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv'))

gdp = pd.read_csv(file_NY, skiprows=3)
populacja = pd.read_csv(file_SP, skiprows=3)
co2 = pd.read_csv(file_co2, skiprows=0)




