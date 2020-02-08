
INDEXES = {
    'pm10': [
        {'to': 20},
        {'to': 50},
        {'to': 80},
        {'to': 110},
        {'to': 150},
        {'to': 9999}
    ],
    'pm25': [
        {'to': 13},
        {'to': 35},
        {'to': 55},
        {'to': 75},
        {'to': 110},
        {'to': 9999}
    ],
    'co':  [
        {'to': 3},
        {'to': 7},
        {'to': 11},
        {'to': 15},
        {'to': 21},
        {'to': 9999}
    ],
}


def _calculate(value, values):
    index = 0
    for idx in values:
        if value <= idx['to']:
            return index
        index = index + 1


def air_index_pm10(value):
    return _calculate(value,  INDEXES['pm10'])


def air_index_pm25(value):
    return _calculate(value, INDEXES['pm25'])


def air_index_co(value):
    return _calculate(value, INDEXES['co'])
