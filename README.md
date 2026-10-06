# hotel_weather_app

Aim of this app/data excercise is to: 
1) Read hotel and weather data
2) Check hotel dataset - for any missing/null values map the Latitude and Longitude columns from the OpenCage Geocoding API
3) Generate a new Geohash column (by latitude and longitude columnn e.g., pygeohash)
4) The hash from point 3 will be used to perform a left join on hotels and weather data
5) Encrypt sensitive data
6) Store enriched data

How to run:
While being in hotel_weather_app directory:
"python3 -m src.hotel_weather.main"

Data:
Used dataset was to large to be posted on github. Example of data will be attached for download.