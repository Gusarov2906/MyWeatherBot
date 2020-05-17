import requests
appid = "XXX"

def get_weather_data(city_id):
    weather=(requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={appid}&units=metric&lang=ru")).json()
    return weather

def get_forecast_data(city_id):

    forecast=(requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={appid}&units=metric&lang=ru")).json()
    return forecast
