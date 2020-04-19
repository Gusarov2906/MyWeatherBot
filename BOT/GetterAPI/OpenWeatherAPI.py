import requests
def get_data(city_id):
    res=[]
    appid = "XXX"
    res.append(requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={appid}&units=metric&lang=ru"))
    res.append(requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={appid}&units=metric&lang=ru"))
    weather = res[0].json()
    forecast = res[1].json()
    return weather,forecast
