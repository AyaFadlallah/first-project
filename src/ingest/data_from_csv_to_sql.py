from sqlalchemy import create_engine
import pandas as pd
import os
import sys
home = os.environ['FORECAST_PROJECT_HOME']
sys.path.append(home)
from config import ip, database_name, my_password

def ingest_data():
    host = ip
    db = database_name
    user = 'sa' 
    password = my_password

    def mssql_engine(user, password, host, db):
        engine = create_engine(
            f"mssql+pyodbc://{user}:{password}@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
        return engine
    
    engine = mssql_engine(user, password, host, db)

    # import the csv file into a data frame:
    data = pd.read_csv('weather_data.csv')   
    df = pd.DataFrame(data)

    # to sql
    df.to_sql('weather_predictions', con=engine, if_exists='append', index= False)
    return