from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv


# Get env variables
load_dotenv(find_dotenv())
NAME = os.environ.get("NAME")
PASSWORD = os.environ.get("PASSWORD")
DATAPATH = os.environ.get("DATAPATH")


# # Connect to database

engine = create_engine(
    f"postgresql+psycopg2://{NAME}:{PASSWORD}@hap-pg.postgres.database.azure.com/HAP")
dbConnection = engine.connect()


# All queries
query_feestdag = text("""
SELECT *
FROM levi_experimenten.feestdag
""")

query_telefonie = text("""
SELECT *
FROM onze_huisartsen.telefonie_op_uurbasis
""")

query_wachttijd = text("""
SELECT *
FROM onze_huisartsen.telefonie_historie
WHERE wachtrij = 'PATIENTEN'
	OR wachtrij = 'SPOED'
""")

query_weer = text("""
SELECT *
FROM open_meteo.weerdata_per_uur
ORDER BY datum_tijd ASC
""")

query_historie= text("""
SELECT date_trunc('hour', answer_time) AS datetime
     , count(*) 																					AS calls
	 , count(*) 			FILTER (WHERE gesprekstijd <= '00:00:05' and wachttijd > '00:00:30') 	AS ophangers
	 , count(*) 			FILTER (WHERE gesprekstijd <= '00:00:05' and wachttijd <= '00:00:30') 	AS verkeerd_bellers
	 , AVG(gesprekstijd) 	FILTER (WHERE gesprekstijd > '00:00:05') 								AS gemiddelde_gesprekstijd
	 , AVG(wachttijd) 		FILTER (WHERE gesprekstijd > '00:00:05') 								AS gemiddelde_wachttijd
FROM   onze_huisartsen.telefonie_historie
WHERE wachtrij = 'PATIENTEN'
GROUP  BY 1
ORDER BY datetime ASC
""")

query_hashed = text("""
SELECT * FROM onze_huisartsen.telefonie_gehashed
""")


# # Extract data from DB and save to csv

# feestdagen = pd.read_sql(query_feestdag, dbConnection)
# feestdagen.to_csv(f"{filepath}/raw/feestdagen.csv", index=False)

# data = pd.read_sql(query_telefonie, dbConnection)
# data.to_csv(f"{filepath}/raw/data.csv")

# wachttijd = pd.read_sql(query_wachttijd, dbConnection)
# wachttijd.to_csv(f"{filepath}/raw/wachttijd.csv", index=False)

# data_hashed = pd.read_sql(query_hashed, dbConnection)
# data_hashed.to_csv(f"{DATAPATH}/raw/data_hashed.csv", sep='±', index=False)


# Absolute path of a file
old_name = "C:/Topicus/Repos/DataScience/src/models/terugbellers.py"
new_name = "C:/Topicus/Repos/DataScience/src/models/process_terugbellers.py"

# Renaming the file
os.rename(old_name, new_name)