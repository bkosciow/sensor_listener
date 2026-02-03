city = "Bielsko-Biała"


def air_quality(data):
    result = {
        'PM25': None,
        'PM10': None,
        'CO': None,
        'O3': None,
        'NO2': None
    }
    icon = [
        '✅', '✅', '⚠️', '☠️', '☠️', '⚰️'
    ]
    max_value = 0
    if data is None or city not in data:
        return "I have no data"

    data = data[city]

    for item in data:
        if item in result:
            if data[item] is not None:
                result[item] = data[item]["index"]
                if data[item]['index'] > max_value:
                    max_value = data[item]['index']

    txt = " __" + city + "__\n" + icon[max_value] + " " + ("  |  ".join(f"__{k}__: {v}" for k, v in result.items()))

    return txt
