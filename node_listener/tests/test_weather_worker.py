#!/usr/bin/python3
#pylint: skip-file

__author__ = 'Bartosz Kościów'
from nose.tools import assert_equal, assert_true, assert_false
from nose.tools import assert_raises
from nose.tools import assert_not_in
from node_listener.worker.openweather_worker import OpenweatherWorker
from unittest.mock import MagicMock
from unittest import mock


class TestOpenweatherWorker(object):
    def setUp(self):
        self.api = 'apikey'
        self.cities = {123: 'ABC', 546: 'DEF'}
        self.worker = OpenweatherWorker(self.cities, self.api)

    def test_init(self):
        api = 'apikey'
        cities = {123: 'ABC'}
        w = OpenweatherWorker(cities, api)
        assert_equal(w.cities, cities)
        assert_equal(w.apikey, api)

    @mock.patch.object(OpenweatherWorker, '_current_weather')
    @mock.patch.object(OpenweatherWorker, '_forecast')
    def test_execute(self, mock1, mock2):
        self.worker.execute()
        mock1.assert_called()
        mock2.assert_called()

    def test_decode_weather(self):
        data = {'coord': {'lon': 19.05, 'lat': 49.82}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 14.92, 'pressure': 994, 'humidity': 71, 'temp_min': 11.67, 'temp_max': 18}, 'visibility': 10000, 'wind': {'speed': 3.1, 'deg': 90}, 'clouds': {'all': 50}, 'dt': 1572808097, 'sys': {'type': 1, 'id': 1701, 'country': 'PL', 'sunrise': 1572759328, 'sunset': 1572794350}, 'timezone': 3600, 'id': 3103402, 'name': 'Bielsko-Biala', 'cod': 200}
        out = {
            'clouds': 50,
            'humidity': 71,
            'pressure': 994,
            'temperature_current': 14.92,
            'update': 1572808097,
            'weather': 'scattered clouds',
            'weather_id': 802,
            'wind_deg': 90,
            'wind_speed': 3.1
        }
        assert_equal(out, self.worker._decode_weather(data))

    def test_decode_forecast(self):
        data = {'dt': 1572775200, 'sunrise': 1572759329, 'sunset': 1572794350, 'temp': {'day': 14.92, 'min': 14.26, 'max': 14.92, 'night': 14.26, 'eve': 14.92, 'morn': 14.92}, 'pressure': 994, 'humidity': 86, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'speed': 1.38, 'deg': 152, 'clouds': 50}
        out = {
            'clouds': 50,
             'humidity': 86,
             'pressure': 994,
             'temperature_max': 14.92,
             'temperature_min': 14.26,
             'weather': 'scattered clouds',
             'weather_id': 802,
             'wind_deg': 152,
             'wind_speed': 1.38
        }

        assert_equal(out, self.worker._decode_forecast(data))
