import requests

appid = "09f2551c5cf86a1131a05a2bcb397626"
city_id = "463829"
res=[]

try:
    res.append(requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={appid}&units=metric"))
    res.append(requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={appid}&units=metric"))
    weather = res[0].json()
    forecast = res[1].json()

    with open("data_cur_weather.txt",'w') as file:
        file.write("WEATHER: \n")
        for item in weather.items():
            file.write("\n" +str(item))

    with open("data_weather.txt",'w') as file:
        file.write("FORECAST: \n")
        for time in forecast["list"]:
            file.write("\n\n")
            for item in time.items():
                file.write("\n" +str(item))

    print("Upload to file was successful!")

except Exception as e:
    print("Exception: ", e)
    pass
