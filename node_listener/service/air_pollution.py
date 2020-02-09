
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
        {'to': 3000},
        {'to': 7000},
        {'to': 11000},
        {'to': 15000},
        {'to': 21000},
        {'to': 99999999}
    ],
    'o3':  [
        {'to': 70},
        {'to': 120},
        {'to': 150},
        {'to': 180},
        {'to': 240},
        {'to': 99999999}
    ],
    'no2':  [
        {'to': 40},
        {'to': 100},
        {'to': 150},
        {'to': 200},
        {'to': 400},
        {'to': 99999999}
    ],
    'so2':  [
        {'to': 50},
        {'to': 100},
        {'to': 200},
        {'to': 350},
        {'to': 500},
        {'to': 99999999}
    ],
    'bc':  [
        {'to': 6},
        {'to': 11},
        {'to': 16},
        {'to': 21},
        {'to': 51},
        {'to': 99999999}
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


def air_index_o3(value):
    return _calculate(value, INDEXES['o3'])


def air_index_no2(value):
    return _calculate(value, INDEXES['no2'])


def air_index_so2(value):
    return _calculate(value, INDEXES['so2'])


def air_index_bc(value):
    return _calculate(value, INDEXES['bc'])
