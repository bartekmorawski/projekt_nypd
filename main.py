import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_NY", default="API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv",help="Path to file with data")
parser.add_argument("file_SP", default="API_SP.POP.TOTL_DS2_en_csv_v2_4751604/API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv",help="Path to file with data 2")
parser.add_argument("file_co2", default="co2-fossil-by-nation_zip/data/fossil-fuel-co2-emissions-by-nation_csv.csv", help="Path to file with co2 data")
parser.add_argument("-start", type=int, default=1960, help="Shift in Caesar cipher (If Morse code was chosen this parameter is ignored)")
parser.add_argument("-end", type=int, default=2021, help="Shift in Caesar cipher (If Morse code was chosen this parameter is ignored)")
#parser.add_argument("-n", type=int, default=3, help="Shift in Caesar cipher (If Morse code was chosen this parameter is ignored)")

args = parser.parse_args()