from datetime import datetime


def weather_current(data):
    return f" Temperature:{data['current']['temperature_current']}°C, humidity: {data['current']['humidity']}%, {data['current']['pressure']} hPa pressure, wind {data['current']['wind_speed']} m/s from {data['current']['wind_deg']}°, {data['current']['weather']}, clouds: {data['current']['clouds']}% "


def weather_forecast(data):
    today = datetime.now().strftime('%Y-%m-%d')
    filtered_forecast = {date: forecast for date, forecast in data['forecast'].items() if date >= today}
    text = ""
    i = 0
    for d in filtered_forecast:
        weather = data['forecast'][d]
        if i == 0:
            text = text + " today (" + d + "): \n"
        else:
            text = text + d + ": \n"

        text += f"Maximum temperature: {weather['temperature_max']}°C, minimum temperature: {weather['temperature_min']}°C,"
        text += f"humidity: {weather['humidity']}%, pressure: {weather['pressure']} hPa, wind: {weather['wind_speed']} m/s  "
        text += f" from {weather['wind_deg']}, {weather['weather']}, clouds: {weather['clouds']}%"
        text = text + "\n"
        i += 1
    return text


def weather(data):
    text = ""
    for city_id in data:
        text += f"Weather for: {data[city_id]['city']}\n now: " + weather_current(data[city_id])+ "\n" + weather_forecast(data[city_id])

    return text

