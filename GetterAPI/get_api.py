#>cd E:\PROJECTS\PythonProjects\MyWeatherBot\MyWeatherBot\GetterAPI>
import json
import OpenWeatherAPI
city_id = "463829"
try:
    weather,forecast = OpenWeatherAPI.get_data(city_id)
    with open(r"E:\PROJECTS\PythonProjects\MyWeatherBot\MyWeatherBot\BOT\data_cur_weather.json",'w',encoding='utf-8') as file:
#        file.write("WEATHER: \n")
#        for item in weather.items():
#            file.write("\n" +str(item)
        json.dump(weather,file)
        file.close()

#    with open(r"E:\PROJECTS\PythonProjects\MyWeatherBot\MyWeatherBot\BOT\data_weather.txt",'w') as file:
#        file.write("FORECAST: \n")
#        for time in forecast["list"]:
#            file.write("\n\n")
#            for item in time.items():
#                file.write("\n" +str(item))
#        file.close()

    print("Upload to file was successful!")

except Exception as e:
    print("Exception: ", e)
    pass
