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


# # Extract data from DB and save to csv

# feestdagen = pd.read_sql(query_feestdag, dbConnection)
# feestdagen.to_csv(f"{filepath}/raw/feestdagen.csv", index=False)

# data = pd.read_sql(query_telefonie, dbConnection)
# data.to_csv(f"{filepath}/raw/data.csv")

# wachttijd = pd.read_sql(query_wachttijd, dbConnection)
# wachttijd.to_csv(f"{filepath}/raw/wachttijd.csv", index=False)