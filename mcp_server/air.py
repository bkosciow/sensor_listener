
def air_quality(data):
    result = {
        'PM25': None,
        'PM10': None,
        'CO': None,
        'O3': None,
    }

    max_value = 0
    for item in data:
        for key in data[item]:
            if key in result:
                if data[item][key] is not None and (result[key] is None or result[key] < data[item][key]):
                    result[key] = data[item][key]['index']
                    if data[item][key]['index'] > max_value:
                        max_value = data[item][key]['index']

    txt = (", ".join(f"__{k}__: {v}" for k, v in result.items()))

    return txt
