import pandas as pd
import pyodbc

data = pd.read_csv ('weather_data.csv')   
df = pd.DataFrame(data)

