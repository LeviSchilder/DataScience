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


# Read and process data
data_hashed = pd.read_csv(f"{DATAPATH}/raw/data_hashed.csv", sep='±', engine='python')
data_hashed = data_hashed.set_index('starttijd_gesprek')
data_hashed["gespreksduur"].fillna("00:00:00", inplace=True)
data = data_hashed.drop(data_hashed[(data_hashed['gespreksduur'] <= '00:00:05') &
                                    (data_hashed['wachttijd'] <= '00:00:30')].index)

data['is_beantwoord'] = np.where((data['gespreksduur'] <= '00:00:05') & (data['wachttijd'] > '00:00:30'), False, True)

data = data.drop(['gebelde_gebruiker', 'ingangsnummer', 'nawerktijd_beller', 'nawerktijd_gebelde', 'nummer_gebelde',
                  'prompttijd', 'type_oproep', 'beantwoord'], axis=1)
data = data.sort_index()
data = data.reset_index()

data['gespreksduur'] = pd.to_timedelta(data['gespreksduur'])
data['wachttijd'] = pd.to_timedelta(data['wachttijd'])

aggregation_functions = {'starttijd_gesprek': 'first',
                         'gespreksduur': 'sum',
                         'nummer_beller': 'last',
                         'wachtrijnaam': 'last',
                         'wachttijd': 'sum',
                         'is_beantwoord': 'last'}
data = data.groupby(data['gespreks_id']).aggregate(aggregation_functions)

# egroup = (data["nummer_beller"] != data["nummer_beller"].shift()).cumsum()
# data["hoeveelste_call"] = egroup.groupby(data["nummer_beller"]).rank(method="dense")

data = data.sort_values(['nummer_beller', 'starttijd_gesprek'], ascending=[True, True])

data['starttijd_gesprek'] = pd.to_datetime(data['starttijd_gesprek'])
data = data.set_index('starttijd_gesprek')
#
# is_beantwoord = data.groupby("nummer_beller", group_keys=True)["is_beantwoord"]
#
# # When the call has never been answered in the previous 8
# # hours, it's a return call. Since we use closed="left", if
# # it's the first call in 8 hours, the window is empty, its
# # sum is NaN and hence not considered a return call.
# is_terugbeller = is_beantwoord.rolling("8H", closed="left").sum().eq(0)
#
# # Time difference since previous call
# geduld = is_beantwoord.apply(lambda w: w.index.to_series().diff())
#
# result = pd.concat(
#     [
#         is_beantwoord.rolling(1).sum().astype("bool"),
#         is_terugbeller.rename("is_terugbeller"),
#         # If it's not a return call, time_until_return = NA
#         geduld.where(is_terugbeller, None).rename("geduld"),
#     ],
#     axis=1,
# )
#
# result = result.reset_index()
# result = result.set_index('starttijd_gesprek').sort_index()
# result.to_csv(f"{DATAPATH}/interim/terugbellers.csv", sep='±')


"""Further processing to concatenate data and result"""
result = pd.read_csv(f"{DATAPATH}/interim/terugbellers.csv", sep='±', engine='python')

result = result.sort_values(['starttijd_gesprek', 'nummer_beller'], ascending=[True, True])
result = result.set_index('starttijd_gesprek')

data = data.reset_index().sort_values(['starttijd_gesprek', 'nummer_beller'], ascending=[True, True])
data = data.set_index('starttijd_gesprek')

result = result.reset_index()
data = data.reset_index()

result['gespreksduur'] = data['gespreksduur']
result['wachtrijnaam'] = data['wachtrijnaam']
result['wachttijd'] = data['wachttijd']

result.to_csv(f"{DATAPATH}/processed/terugbellers.csv", sep='±')


elapsed_time = datetime.now() - startTime
print(f"\nElapsed time: {elapsed_time}")