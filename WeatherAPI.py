import requests
import csv
from datetime import datetime, timedelta

api_key = "e43a76fb818e25e53b56e66ba7aa5684"
api_url = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    "q": "Beirut",
    "appid": api_key,
    #'cnt': 11, # number of timestamps, which will be returned in the API response
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

# Open the CSV file in write mode
with open("weather_data.csv", "w", newline="") as csvfile:
    mycsv = csv.writer(csvfile)
    mycsv.writerow(["Time", "temperature","feels_Like", "minimal_temp", "maximal_temp","speed_of_wind", "humidity","description_of_weather"])

    for forecast in forecast_data:
        # Convert the forecast timestamp to a datetime object
        forecast_date = datetime.fromtimestamp(forecast["dt"])
        
        # Filter the forecast for the next day only
        # we added one hour to obtain only the results of the next day fully
        if next_day_start +timedelta(hours=1) <= forecast_date <= next_day_end + timedelta(hours=1):
            time = forecast["dt_txt"]
            temperature = forecast["main"]["temp"]
            feels_like = forecast["main"]["feels_like"]
            temp_min = forecast["main"]["temp_min"]
            temp_max = forecast["main"]["temp_max"]
            humidity = forecast["main"]["humidity"]
            speed_of_wind = forecast["wind"]["speed"]
            weather_description = forecast["weather"][0]['description']
            

            mycsv.writerow([time, temperature, feels_like, temp_min, temp_max, speed_of_wind, humidity, weather_description])