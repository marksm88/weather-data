import requests
import pandas as pd

API_KEY = '11c7ca0993386fad25c48ce434f2ca94'

# science garden, quezon city, ph
lat = 14.6448
lon = 121.0445 
url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'lat': lat,
    'lon': lon,
    'appid': API_KEY,
    'units': 'metric'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    time_of_data_calculation_utc = pd.to_datetime(data.get('dt'), unit='s')
    time_of_data_calculation_pht = time_of_data_calculation_utc + pd.Timedelta(hours=8)
    record = {
        'datetime': time_of_data_calculation_pht,
        'city_name': data.get('name'),
        'country_code': data.get('sys', {}).get('country'),
        'longitude (degrees)': data.get('coord', {}).get('lon'),
        'latitude (degrees)': data.get('coord', {}).get('lat'),
        'weather_main': data.get('weather', [{}])[0].get('main'),
        'weather_description': data.get('weather', [{}])[0].get('description'),
        'temperature (C)': data.get('main', {}).get('temp'),
        'feels_like_temperature (C)': data.get('main', {}).get('feels_like'),
        'pressure (hPa)': data.get('main', {}).get('pressure'),
        'humidity (%)': data.get('main', {}).get('humidity'),
        'temp_min (C)': data.get('main', {}).get('temp_min'),
        'temp_max (C)': data.get('main', {}).get('temp_max'),
        'sea_level_pressure (hPa)': data.get('main', {}).get('sea_level'),
        'ground_level_pressure (hPa)': data.get('main', {}).get('grnd_level'),
        'visibility (m)': data.get('visibility'),
        'wind_speed (m/s)': data.get('wind', {}).get('speed'),
        'wind_deg (degrees)': data.get('wind', {}).get('deg'),
        'wind_gust (m/s)': data.get('wind', {}).get('gust'),
        'cloudiness (%)': data.get('clouds', {}).get('all'),
        'rain_last_1h (mm)': data.get('rain', {}).get('1h'),
        'rain_last_3h (mm)': data.get('rain', {}).get('3h'),

    }
    

    df = pd.DataFrame([record])
    
    df.to_csv('Weather Data - Current.csv', index=False)
else:
    print(f"Failed to retrieve data: {response.status_code}, {response.text}")


#--------------------
weather_prelim = pd.read_csv('Weather Data - Prelim.csv')
weather_current = pd.read_csv('Weather Data - Current.csv')

combined = pd.concat([weather_prelim, weather_current], ignore_index=True).drop_duplicates()

combined.to_csv('Weather Data - Prelim.csv', index=False)
