import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Settings
startTime = datetime.now()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Get env variables
load_dotenv(find_dotenv())
NAME = os.environ.get("NAME")
PASSWORD = os.environ.get("PASSWORD")
DATAPATH = os.environ.get("DATAPATH")


# Read the processed data and analyze
result = pd.read_csv(f"{DATAPATH}/processed/terugbellers.csv", sep='±', engine='python')
result['geduld'] = pd.to_timedelta(result['geduld'])

gem_geduld = result['geduld'].mean()
terugbellers = result['is_terugbeller'].value_counts()
percentage_terugbellers = (terugbellers[1] / result.shape[0]) * 100

print(f"\nVan de {result.shape[0]} gesprekken valt {terugbellers[1]} onder terugbelverkeer. Dit komt neer op {percentage_terugbellers:.2f}% van alle gesprekken.")
print(f"\nHet duurt gemiddeld {gem_geduld} voordat een ophanger terugbelt.")

# result_per_uur = result[['is_terugbeller', 'geduld']].copy()
# result_per_uur = result_per_uur.resample('H').agg({'is_terugbeller': 'count', 'geduld': 'mean'})
# print(result_per_uur.head(20))

# # Plot forecast vs actual value
# ax = result_per_uur[['is_terugbeller']].plot(figsize=(10, 5))
# plt.legend(['is_terugbeller'])
# ax.set_title('is_terugbeller')
#
# plt.show()


elapsed_time = datetime.now() - startTime
print(f"\nElapsed time: {elapsed_time}")