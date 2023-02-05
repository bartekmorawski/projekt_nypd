import argparse
import os
import pandas as pd
import func

# def file_path(path):
#     if os.path.isfile(path):
#         return path
#     else:
#         raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid path")

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
parser.add_argument("--start", type=int, default=1960, help="start year")
parser.add_argument("--end", type=int, default=2021, help="end year")

args = parser.parse_args()

gdp = pd.read_csv(args.file_NY, skiprows=3)
populacja = pd.read_csv(args.file_SP, skiprows=3)
co2 = pd.read_csv(args.file_co2, skiprows=0)
