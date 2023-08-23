SELECT MAX(temperature) AS maximal_temperature,
MIN(temperature) AS minimal_temperature,
AVG(temperature) AS average_temperature,
AVG(speed_of_wind) AS average_speed_of_wind,
AVG(humidity) AS average_humidity

FROM dbo.next_day_weather

