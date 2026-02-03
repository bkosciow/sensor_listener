
def air_quality(data):
    data_set = {
        'PM25': None,
        'PM10': None,
        'CO': None,
        'O3': None,
        'NO2': None
    }
    result = {}
    txt = "Air quality, null or none value means no data\n"
    for city in data:
        result[city] = data_set.copy()
        for item in data[city]:
            if item in data_set:
                if data[city][item] is not None:
                    result[city][item] = data[city][item]["index"]

    txt += (", ".join(f"__{k}__: {v}" for k, v in result.items()))

    return txt
