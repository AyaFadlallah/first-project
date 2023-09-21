import requests
from datetime import datetime, timedelta
import pandas as pd
import os
import sys
home = os.environ['FORECAST_PROJECT_HOME']
sys.path.append(home)

def fetch_data():
    #import airflow variable
    from airflow.models import Variable
    my_api_key = Variable.get('my_api_key')

    api_key = my_api_key
    api_url = "https://api.openweathermap.org/data/2.5/forecast"

    parameters = {
        "q": "Beirut",
        "appid": api_key,
        'units': 'metric'
    }

    response = requests.get(api_url, params=parameters)
    data = response.json()
    forecast_data = data["list"]

    # Get the current date and the next day
    current_date = datetime.now().date()
    next_day = current_date + timedelta(days=1)

    # to specify the start and end of the next day
    next_day_start = datetime.combine(next_day, datetime.min.time())
    next_day_end = datetime.combine(next_day, datetime.max.time())

    # create empty lists
    TIME=[ ]
    TEMP=[]
    FL=[]
    MIN =[]
    MAX=[]
    H=[]
    SW=[]
    WD=[]

    for forecast in forecast_data:
        # Convert the forecast timestamp to a datetime object
        forecast_date = datetime.fromtimestamp(forecast["dt"])
            
        # Filter the forecast for the next day only
        # we added one hour to obtain only the results of the next day fully
        if next_day_start +timedelta(hours=1) <= forecast_date <= next_day_end + timedelta(hours=1):
            # extract needed data
            time = forecast["dt_txt"]
            temperature = forecast["main"]["temp"]
            feels_like = forecast["main"]["feels_like"]
            temp_min = forecast["main"]["temp_min"]
            temp_max = forecast["main"]["temp_max"]
            humidity = forecast["main"]["humidity"]
            speed_of_wind = forecast["wind"]["speed"]
            weather_description = forecast["weather"][0]['description']
            # append data
            TIME.append(time)
            TEMP.append(temperature)
            FL.append(feels_like)
            MIN.append(temp_min)
            MAX.append(temp_max)
            H.append(humidity)
            SW.append(speed_of_wind)
            WD.append(weather_description)

    # dictionary of lists 
    dictio={'time':TIME,
            'temperature':TEMP,
            'feels_like': FL, 
            'temp_min':MIN,
            'temp_max': MAX, 
            'speed_of_wind': SW, 
            'humidity':H,
            'weather_description':WD}

    df = pd.DataFrame(dictio)
    print(df)
    df.to_csv('weather_data.csv', index=False)
    return 
