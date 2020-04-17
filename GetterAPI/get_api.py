#>cd E:\PROJECTS\PythonProjects\MyWeatherBot\MyWeatherBot\GetterAPI>
import requests
import json
appid = "09f2551c5cf86a1131a05a2bcb397626"
city_id = "463829"
res=[]

try:
    res.append(requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={appid}&units=metric"))
    res.append(requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={appid}&units=metric"))
    weather = res[0].json()
    forecast = res[1].json()

    with open(r"E:\PROJECTS\PythonProjects\MyWeatherBot\MyWeatherBot\BOT\data_cur_weather.json",'w',encoding='utf-8') as file:
#        file.write("WEATHER: \n")
#        for item in weather.items():
#            file.write("\n" +str(item))
        json.dump(weather,file)
        file.close()

    with open(r"E:\PROJECTS\PythonProjects\MyWeatherBot\MyWeatherBot\BOT\data_weather.txt",'w') as file:
        file.write("FORECAST: \n")
        for time in forecast["list"]:
            file.write("\n\n")
            for item in time.items():
                file.write("\n" +str(item))
        file.close()

    print("Upload to file was successful!")

except Exception as e:
    print("Exception: ", e)
    pass
