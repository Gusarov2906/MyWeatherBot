import requests
import json

appid = "xxx"
city_id = "463829"

def get_weather_data(city_id):
    weather=(requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={appid}&units=metric&lang=ru")).json()
    return weather

def get_forecast_data(city_id):

    forecast=(requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={appid}&units=metric&lang=ru")).json()
    return forecast

def get_current_weather():
    try:
        weather = get_weather_data(city_id)

        with open(r"CurrentWeather.json",'w',encoding='utf-8') as file:
            json.dump(weather,file)
            file.close()
            print("Upload to file was successful!")
    except Exception as e:
        print("!!!Exception: ", e)
        with open("error.txt",'a',encoding='utf-8') as file:
                    file.write("!!!Exception: "+str(e))
        pass

def get_forecast_weather():
    try:
        forecast = get_forecast_data(city_id)

        with open(r"ForecastWeather.json",'w',encoding='utf-8') as file:
            json.dump(forecast,file)
            file.close()

        print("Upload to file was successful!")

    except Exception as e:
        print("!!!Exception: ", e)
        with open("error.txt",'a',encoding='utf-8') as file:
                    file.write("!!!Exception: "+str(e))
        pass

if __name__ == '__main__':
    get_current_weather()
    get_forecast_weather()
