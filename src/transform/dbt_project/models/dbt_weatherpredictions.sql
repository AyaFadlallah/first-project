SELECT *
FROM {{ source('dbo','next_day_weather')}}