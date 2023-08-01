from sqlalchemy import create_engine
import pandas as pd


##ip addresses to try
ip1= '172.20.112.1' #IPv4 Address of Ethernet adapter vEthernet (WSL)
ip2 = '192.168.0.104' #IPv4 Address of Wireless LAN adapter Wi-Fi
ip3 ='172.20.112.1'

## drivers to try
driver1 = '{ODBC Driver 17 for SQL Server}'
driver2 = '/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.9.so.1.1'




host = '172.20.112.1,1433' # to specify an alternate port
db = 'testdb' 
user = 'sa' 
password = 'password123'


def mssql_engine(user, password, host, db):
    engine = create_engine(
        f"mssql+pyodbc://{user}:{password}@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
    return engine
engine = mssql_engine(user, password, host, db)


df = pd.read_sql(con=engine,sql = 'select * from dbo.names')
print(df)