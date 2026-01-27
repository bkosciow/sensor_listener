from datetime import datetime


city_id = "3103402"


def weather_current(data):
    data = data[city_id]
    return f" 🌡️{data['current']['temperature_current']}°C, 💦{data['current']['humidity']}%, {data['current']['pressure']} hPa pressure, 🌀{data['current']['wind_speed']} m/s 🧭{data['current']['wind_deg']}°, {data['current']['weather']}, ☁️{data['current']['clouds']}% "


def weather_forecast(data):
    data = data[city_id]
    today = datetime.now().strftime('%Y-%m-%d')
    filtered_forecast = {date: forecast for date, forecast in data['forecast'].items() if date >= today}

    text = ""
    for d in filtered_forecast:
        weather = data['forecast'][d]
        text = text + " 📆 __" + d + "__ \n"
        text = text + f" 🌡️{weather['temperature_max']}/{weather['temperature_min']}°C | 💦{weather['humidity']}% | {weather['pressure']} hPa | "
        text = text + f" 🌀{weather['wind_speed']} m/s 🧭{weather['wind_deg']} | {weather['weather']} | ☁️{weather['clouds']}% "
        text = text + "\n"
    return text


def weather(data):
    return f"Weather for: {data[city_id]['city']}\n __now__ :" + weather_current(data)+ "\n" + weather_forecast(data)
